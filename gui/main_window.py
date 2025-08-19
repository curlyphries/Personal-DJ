import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QSplitter
)
from PySide6.QtCore import Qt, QThread
from gui.worker import Worker
from gui.music_controls import MusicControlWidget

class MainWindow(QMainWindow):
    """The main window for the Personal DJ application."""

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.thread = None
        self.worker = None
        self.music_controls = None

        self.setWindowTitle("Personal DJ")
        self.setGeometry(100, 100, 600, 500)

        # --- Main Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create splitter for main content and music controls
        splitter = QSplitter(Qt.Vertical)
        
        # --- Top Section (DJ Interface) ---
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        
        # --- Vibe Input ---
        self.vibe_input = QLineEdit()
        self.vibe_input.setPlaceholderText("Enter a vibe (e.g., 'late-night synthwave')")
        top_layout.addWidget(self.vibe_input)

        # --- Status Label ---
        self.status_label = QLabel("Welcome to your Personal DJ. Enter a vibe to begin.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        top_layout.addWidget(self.status_label)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start DJ")
        self.stop_button = QPushButton("Stop Session")
        self.quit_button = QPushButton("Quit")
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.quit_button)
        top_layout.addLayout(button_layout)
        
        splitter.addWidget(top_widget)
        
        # --- Music Controls Section ---
        self.music_controls = MusicControlWidget()
        self.music_controls.setMinimumHeight(200)
        splitter.addWidget(self.music_controls)
        
        # Set splitter proportions
        splitter.setSizes([200, 300])
        main_layout.addWidget(splitter)
        
        # Remove the old now playing label as it's now in music controls

        # --- Connections ---
        self.start_button.clicked.connect(self.start_dj_session)
        self.stop_button.clicked.connect(self.stop_dj_session)
        self.quit_button.clicked.connect(self.close)
        
        # Connect music control signals
        self.music_controls.play_requested.connect(self.on_play_requested)
        self.music_controls.pause_requested.connect(self.on_pause_requested)
        self.music_controls.stop_requested.connect(self.on_stop_requested)
        self.music_controls.skip_requested.connect(self.on_skip_requested)
        self.music_controls.volume_changed.connect(self.on_volume_changed)
        self.music_controls.seek_requested.connect(self.on_seek_requested)

    def start_dj_session(self):
        """Starts the background worker to handle the DJ logic."""
        vibe = self.vibe_input.text()
        if not vibe:
            self.status_label.setText("Please enter a vibe first.")
            return

        self.start_button.setEnabled(False)
        self.status_label.setText("Starting session...")

        # --- Set up the worker thread ---
        self.thread = QThread()
        self.worker = Worker(self.logger)
        self.worker.moveToThread(self.thread)

        # --- Connect signals and slots ---
        self.thread.started.connect(lambda: self.worker.run(vibe))
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.status_updated.connect(self.update_status)
        self.worker.now_playing_updated.connect(self.update_now_playing)
        self.worker.error_occurred.connect(self.handle_error)
        self.worker.music_status_updated.connect(self.music_controls.update_status)

        # --- Start the thread ---
        self.thread.start()

    def stop_dj_session(self):
        """Stops the background worker."""
        if self.worker:
            self.worker.stop()
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        self.status_label.setText("Session stopped. Ready for a new vibe.")
        self.start_button.setEnabled(True)

    def update_status(self, message: str):
        """Updates the status label with a message from the worker."""
        self.status_label.setText(message)
        self.logger.info(f"UI Status: {message}")
        if message == "Ready for a new vibe." or "An error occurred" in message or "Session stopped" in message:
            self.start_button.setEnabled(True)

    def update_now_playing(self, track_name: str):
        """Updates the 'Now Playing' display."""
        self.music_controls.update_status("playing", track_name)

    def handle_error(self, error_message: str):
        """Displays an error message in the status label."""
        self.status_label.setText(f"An error occurred: {error_message}")
        self.start_button.setEnabled(True)

    def closeEvent(self, event):
        """Handle the window close event."""
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait() # Wait for the thread to finish
        QApplication.quit()
    
    def on_play_requested(self):
        """Handle play request from music controls."""
        if self.worker:
            self.worker.resume_music()
    
    def on_pause_requested(self):
        """Handle pause request from music controls."""
        if self.worker:
            self.worker.pause_music()
    
    def on_stop_requested(self):
        """Handle stop request from music controls."""
        if self.worker:
            self.worker.stop_music()
    
    def on_skip_requested(self):
        """Handle skip request from music controls."""
        if self.worker:
            self.worker.skip_track()
    
    def on_volume_changed(self, volume):
        """Handle volume change from music controls."""
        if self.worker:
            self.worker.set_volume(volume)
    
    def on_seek_requested(self, position):
        """Handle seek request from music controls."""
        if self.worker:
            self.worker.seek_to(position)
