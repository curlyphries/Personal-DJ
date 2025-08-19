from PySide6.QtCore import QObject, Signal
from core.dispatcher import Dispatcher

class Worker(QObject):
    """A worker object that runs the DJ logic in a separate thread."""
    
    # --- Signals ---
    # These signals will be emitted from the worker thread and connected to the main UI thread.
    status_updated = Signal(str)  # To send status messages to the UI
    now_playing_updated = Signal(str) # To send the current track name
    error_occurred = Signal(str) # To send specific error messages
    finished = Signal()           # To signal that the task is complete
    music_status_updated = Signal(str, str)  # To send music status updates (status, track_title)

    def __init__(self, logger):
        super().__init__()
        self.logger = logger
        self.dispatcher = None
        self._is_running = False
        self._music_agent = None

    def run(self, vibe: str):
        self._is_running = True
        """The main method that will be executed in the background thread."""
        try:
            self.status_updated.emit("Initializing agents...")
            if not self.dispatcher:
                self.dispatcher = Dispatcher(self.logger)
                self._music_agent = self.dispatcher.music_agent
                # Set up music status callback
                self._music_agent.set_status_callback(self._on_music_status_changed)

            # --- Run the core DJ logic ---
            self.status_updated.emit(f"Vibe received: '{vibe}'. Engaging agents...")
            
            # 1. DJ Agent
            self.status_updated.emit("DJ Agent: Generating commentary and selecting track...")
            commentary, track_title, track_url = self.dispatcher.dj_agent.respond(vibe)
            
            # 2. Voice Agent
            self.status_updated.emit("Voice Agent: Generating commentary audio...")
            commentary_audio_path = self.dispatcher.voice_agent.speak(commentary)

            # 3. Music Agent
            if commentary_audio_path:
                self.status_updated.emit(f"Playing commentary...")
                self.dispatcher.music_agent.play_track(commentary_audio_path)
            
            if track_url:
                display_title = track_title if track_title else "Unknown Track"
                self.now_playing_updated.emit(display_title)
                self.status_updated.emit(f"Playing music: {display_title}")
                self.dispatcher.music_agent.play_track(track_url, display_title)
            else:
                self.status_updated.emit("No music track was selected.")
                self.now_playing_updated.emit("None")

            self.status_updated.emit("Ready for a new vibe.")

        except Exception as e:
            self.logger.error(f"An error occurred in the worker thread: {e}", exc_info=True)
            self.error_occurred.emit(str(e))
        finally:
            self._is_running = False
            self.finished.emit() # Signal that the work is done

    def stop(self):
        """Stops the music playback and the worker."""
        if self._is_running:
            self.status_updated.emit("Stopping...")
            if self.dispatcher and self.dispatcher.music_agent:
                self.dispatcher.music_agent.stop()
            self._is_running = False
            self.now_playing_updated.emit("None")
    
    def _on_music_status_changed(self, status, data):
        """Handle music status changes from the music agent."""
        # Get additional source info if available
        source_info = ""
        if self._music_agent and hasattr(self._music_agent, 'get_source_info'):
            source_info = self._music_agent.get_source_info()
        
        self.music_status_updated.emit(status, source_info if source_info != "No active source" else data or "")
    
    def pause_music(self):
        """Pause the currently playing music."""
        if self._music_agent:
            self._music_agent.pause()
    
    def resume_music(self):
        """Resume paused music."""
        if self._music_agent:
            self._music_agent.resume()
    
    def stop_music(self):
        """Stop the currently playing music."""
        if self._music_agent:
            self._music_agent.stop()
    
    def skip_track(self):
        """Skip to the next track (for now, just stop current)."""
        if self._music_agent:
            self._music_agent.stop()
            self.status_updated.emit("Track skipped. Ready for a new vibe.")
    
    def set_volume(self, volume):
        """Set the music volume."""
        if self._music_agent:
            self._music_agent.set_volume(volume)
    
    def seek_to(self, position):
        """Seek to a specific position in the track."""
        # For now, this is a placeholder as seeking requires more complex implementation
        self.logger.info(f"Seek requested to position: {position}s")
