"""
Music Control Widget for Personal DJ GUI

This module provides a comprehensive music control interface including:
- Play/Pause/Stop/Skip buttons
- Volume control slider
- Progress bar with position display
- Current track information
- Playlist controls
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, 
    QLabel, QProgressBar, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QPalette


class MusicControlWidget(QWidget):
    """Comprehensive music control widget."""
    
    # Signals for communication with main window
    play_requested = Signal()
    pause_requested = Signal()
    stop_requested = Signal()
    skip_requested = Signal()
    volume_changed = Signal(int)
    seek_requested = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_track = "No track loaded"
        self.is_playing = False
        self.is_paused = False
        self.position = 0
        self.duration = 0
        self.volume = 70
        
        self.setup_ui()
        self.setup_timer()
        
    def setup_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Track info section
        self.setup_track_info(layout)
        
        # Progress section
        self.setup_progress_section(layout)
        
        # Control buttons section
        self.setup_control_buttons(layout)
        
        # Volume section
        self.setup_volume_section(layout)
        
        # Apply styling
        self.apply_styling()
        
    def setup_track_info(self, layout):
        """Set up track information display."""
        track_frame = QFrame()
        track_frame.setFrameStyle(QFrame.StyledPanel)
        track_layout = QVBoxLayout(track_frame)
        
        # Current track label
        self.track_label = QLabel(self.current_track)
        self.track_label.setAlignment(Qt.AlignCenter)
        self.track_label.setWordWrap(True)
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        self.track_label.setFont(font)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(9)
        self.status_label.setFont(font)
        
        # Source info label
        self.source_label = QLabel("No source")
        self.source_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(8)
        font.setItalic(True)
        self.source_label.setFont(font)
        self.source_label.setStyleSheet("color: #666;")
        
        track_layout.addWidget(self.track_label)
        track_layout.addWidget(self.status_label)
        track_layout.addWidget(self.source_label)
        layout.addWidget(track_frame)
        
    def setup_progress_section(self, layout):
        """Set up progress bar and time display."""
        progress_frame = QFrame()
        progress_layout = QVBoxLayout(progress_frame)
        
        # Time labels
        time_layout = QHBoxLayout()
        self.current_time_label = QLabel("0:00")
        self.total_time_label = QLabel("0:00")
        
        # Progress bar
        self.progress_bar = QSlider(Qt.Horizontal)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.sliderPressed.connect(self.on_progress_pressed)
        self.progress_bar.sliderReleased.connect(self.on_progress_released)
        
        time_layout.addWidget(self.current_time_label)
        time_layout.addStretch()
        time_layout.addWidget(self.total_time_label)
        
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addLayout(time_layout)
        layout.addWidget(progress_frame)
        
    def setup_control_buttons(self, layout):
        """Set up playback control buttons."""
        controls_frame = QFrame()
        controls_layout = QHBoxLayout(controls_frame)
        controls_layout.setSpacing(15)
        
        # Play/Pause button
        self.play_pause_btn = QPushButton("▶ Play")
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        self.play_pause_btn.setMinimumHeight(40)
        
        # Stop button
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.clicked.connect(self.on_stop_clicked)
        self.stop_btn.setMinimumHeight(40)
        
        # Skip button
        self.skip_btn = QPushButton("⏭ Skip")
        self.skip_btn.clicked.connect(self.on_skip_clicked)
        self.skip_btn.setMinimumHeight(40)
        
        controls_layout.addStretch()
        controls_layout.addWidget(self.play_pause_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.skip_btn)
        controls_layout.addStretch()
        
        layout.addWidget(controls_frame)
        
    def setup_volume_section(self, layout):
        """Set up volume control."""
        volume_frame = QFrame()
        volume_layout = QHBoxLayout(volume_frame)
        
        # Volume label
        volume_label = QLabel("🔊 Volume:")
        
        # Volume slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(self.volume)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        
        # Volume value label
        self.volume_value_label = QLabel(f"{self.volume}%")
        self.volume_value_label.setMinimumWidth(40)
        
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_value_label)
        
        layout.addWidget(volume_frame)
        
    def setup_timer(self):
        """Set up timer for updating progress."""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_progress)
        self.update_timer.start(1000)  # Update every second
        
    def apply_styling(self):
        """Apply custom styling to the widget."""
        self.setStyleSheet("""
            QFrame {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                border-radius: 5px;
                padding: 5px;
                margin: 2px;
            }
            
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #45a049;
            }
            
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            
            QSlider::groove:horizontal {
                border: 1px solid #bbb;
                background: white;
                height: 10px;
                border-radius: 4px;
            }
            
            QSlider::sub-page:horizontal {
                background: #4CAF50;
                border: 1px solid #777;
                height: 10px;
                border-radius: 4px;
            }
            
            QSlider::add-page:horizontal {
                background: #fff;
                border: 1px solid #777;
                height: 10px;
                border-radius: 4px;
            }
            
            QSlider::handle:horizontal {
                background: #4CAF50;
                border: 1px solid #5c5c5c;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
            
            QLabel {
                color: #333;
            }
        """)
        
    def toggle_play_pause(self):
        """Handle play/pause button click."""
        if self.is_playing and not self.is_paused:
            self.pause_requested.emit()
        elif self.is_paused:
            self.play_requested.emit()
        else:
            self.play_requested.emit()
            
    def on_stop_clicked(self):
        """Handle stop button click."""
        self.stop_requested.emit()
        
    def on_skip_clicked(self):
        """Handle skip button click."""
        self.skip_requested.emit()
        
    def on_volume_changed(self, value):
        """Handle volume slider change."""
        self.volume = value
        self.volume_value_label.setText(f"{value}%")
        self.volume_changed.emit(value)
        
    def on_progress_pressed(self):
        """Handle progress bar press."""
        self.update_timer.stop()
        
    def on_progress_released(self):
        """Handle progress bar release."""
        if self.duration > 0:
            seek_position = (self.progress_bar.value() / 100) * self.duration
            self.seek_requested.emit(int(seek_position))
        self.update_timer.start()
        
    def update_status(self, status, track_title=None, source_info=None):
        """Update the control widget status."""
        if status == "playing":
            self.is_playing = True
            self.is_paused = False
            self.play_pause_btn.setText("⏸ Pause")
            self.status_label.setText("Playing")
            if track_title:
                self.current_track = track_title
                self.track_label.setText(track_title)
            if source_info:
                self.source_label.setText(source_info)
                
        elif status == "paused":
            self.is_paused = True
            self.play_pause_btn.setText("▶ Resume")
            self.status_label.setText("Paused")
            
        elif status == "stopped":
            self.is_playing = False
            self.is_paused = False
            self.play_pause_btn.setText("▶ Play")
            self.status_label.setText("Stopped")
            self.source_label.setText("No source")
            self.position = 0
            self.progress_bar.setValue(0)
            self.current_time_label.setText("0:00")
            
        elif status == "finished":
            self.is_playing = False
            self.is_paused = False
            self.play_pause_btn.setText("▶ Play")
            self.status_label.setText("Ready")
            self.source_label.setText("No source")
            self.position = 0
            self.progress_bar.setValue(0)
            self.current_time_label.setText("0:00")
            
        elif status == "volume_changed":
            if track_title is not None:  # track_title contains volume value
                self.volume = track_title
                self.volume_slider.setValue(self.volume)
                self.volume_value_label.setText(f"{self.volume}%")
                
    def update_progress(self):
        """Update progress bar and time display."""
        if self.is_playing and not self.is_paused:
            self.position += 1
            
        if self.duration > 0:
            progress = (self.position / self.duration) * 100
            self.progress_bar.setValue(int(progress))
            
        self.current_time_label.setText(self.format_time(self.position))
        self.total_time_label.setText(self.format_time(self.duration))
        
    def set_duration(self, duration):
        """Set track duration."""
        self.duration = duration
        self.total_time_label.setText(self.format_time(duration))
        
    def set_position(self, position):
        """Set current position."""
        self.position = position
        if self.duration > 0:
            progress = (position / self.duration) * 100
            self.progress_bar.setValue(int(progress))
        self.current_time_label.setText(self.format_time(position))
        
    def format_time(self, seconds):
        """Format time in MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02d}"
        
    def enable_controls(self, enabled=True):
        """Enable or disable all controls."""
        self.play_pause_btn.setEnabled(enabled)
        self.stop_btn.setEnabled(enabled)
        self.skip_btn.setEnabled(enabled)
        self.volume_slider.setEnabled(enabled)
        self.progress_bar.setEnabled(enabled)
