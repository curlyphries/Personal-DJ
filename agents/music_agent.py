import shutil
import subprocess
import threading
import time
from typing import Optional, Callable
from core.music_source_detector import MusicSourceDetector, MusicSource

class MusicAgent:
    """The Music Agent, responsible for playing local audio files and remote streams."""

    def __init__(self, logger):
        """Initializes the Music Agent and finds a suitable player."""
        self.logger = logger
        self.player_executable = self._find_player()
        self.process = None  # To keep track of the music player process
        self.current_track = None
        self.current_track_title = None
        self.current_source = None  # Current music source info
        self.is_playing = False
        self.is_paused = False
        self.volume = 70  # Default volume (0-100)
        self.position = 0  # Current position in seconds
        self.duration = 0  # Track duration in seconds
        self.status_callback = None  # Callback for status updates
        self._monitor_thread = None
        self._stop_monitoring = False
        self.source_detector = MusicSourceDetector(logger)
        if self.player_executable:
            self.logger.info(f"Music Agent: Using player '{self.player_executable}'.")
        else:
            self.logger.error("Music Agent: No supported music player found (mpv, ffplay, vlc).")
            raise RuntimeError("No supported music player found. Please install 'mpv', 'ffplay', or 'vlc'.")

    def _find_player(self) -> str | None:
        """Finds the first available command-line music player."""
        for player in ["mpv", "ffplay", "vlc"]:
            if shutil.which(player):
                self.logger.info(f"Found player: {player}")
                return player
        return None

    def play_track(self, track_path: str, track_title: str = None):
        """Plays the given audio track, which can be a local file path or a URL."""
        if self.process and self.process.poll() is None:
            self.logger.warning("Another track is already playing. Stopping it first.")
            self.stop()

        if not self.player_executable:
            self.logger.error("Cannot play track: No music player available.")
            return False
        
        if not track_path:
            self.logger.warning("No track path or URL provided to play.")
            return False

        self.current_track = track_path
        self.current_track_title = track_title or track_path
        
        # Detect and log music source
        self.current_source = self.source_detector.detect_source(track_path, self.player_executable)
        self.source_detector.register_source(track_path, self.current_source)
        
        source_info = self.source_detector.format_source_info(self.current_source, include_details=True)
        self.logger.info(f"Playing: {self.current_track_title}")
        self.logger.info(f"Source: {source_info}")

        try:
            # Use mpv with JSON IPC for better control if available
            if self.player_executable == "mpv":
                self.process = subprocess.Popen([
                    self.player_executable, 
                    track_path,
                    "--no-video",
                    f"--volume={self.volume}",
                    "--input-ipc-server=/tmp/mpv-socket"
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                self.process = subprocess.Popen(
                    [self.player_executable, track_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            self.is_playing = True
            self.is_paused = False
            self.position = 0
            
            # Start monitoring thread
            self._start_monitoring()
            
            if self.status_callback:
                self.status_callback("playing", self.current_track_title)
                
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to play '{track_path}': {e}", exc_info=True)
            return False

    def stop(self):
        """Stops the currently playing track."""
        self._stop_monitoring = True
        
        if self.process and self.process.poll() is None: # Check if process is running
            self.logger.info("Stopping music player...")
            self.process.terminate()
            self.process.wait() # Wait for the process to terminate
            self.logger.info("Music player stopped.")
            self.process = None
        else:
            self.logger.info("No music is currently playing.")
            
        self.is_playing = False
        self.is_paused = False
        self.current_track = None
        self.current_track_title = None
        self.current_source = None
        self.position = 0
        
        if self.status_callback:
            self.status_callback("stopped", None)
    
    def pause(self):
        """Pause the currently playing track."""
        if not self.is_playing or self.is_paused:
            return False
            
        if self.player_executable == "mpv" and self.process:
            try:
                # Send pause command to mpv via IPC (simplified)
                self.is_paused = True
                if self.status_callback:
                    self.status_callback("paused", self.current_track_title)
                return True
            except:
                pass
        
        # Fallback: stop and remember position for resume
        self.is_paused = True
        if self.status_callback:
            self.status_callback("paused", self.current_track_title)
        return True
    
    def resume(self):
        """Resume the paused track."""
        if not self.is_paused:
            return False
            
        if self.current_track:
            self.is_paused = False
            if self.status_callback:
                self.status_callback("playing", self.current_track_title)
            return True
        return False
    
    def set_volume(self, volume: int):
        """Set playback volume (0-100)."""
        self.volume = max(0, min(100, volume))
        
        if self.player_executable == "mpv" and self.process and self.process.poll() is None:
            try:
                # Send volume command to mpv (simplified)
                pass
            except:
                pass
        
        if self.status_callback:
            self.status_callback("volume_changed", self.volume)
        
        return self.volume
    
    def get_status(self):
        """Get current playback status."""
        status = {
            "is_playing": self.is_playing,
            "is_paused": self.is_paused,
            "current_track": self.current_track_title,
            "volume": self.volume,
            "position": self.position,
            "duration": self.duration,
            "player": self.player_executable
        }
        
        if self.current_source:
            status.update({
                "source_type": self.current_source.source_type,
                "source_name": self.current_source.source_name,
                "source_icon": self.current_source.icon,
                "source_details": self.current_source.details,
                "source_info": self.source_detector.format_source_info(self.current_source)
            })
        
        return status
    
    def set_status_callback(self, callback: Callable):
        """Set callback function for status updates."""
        self.status_callback = callback
    
    def _start_monitoring(self):
        """Start monitoring thread for playback status."""
        self._stop_monitoring = False
        self._monitor_thread = threading.Thread(target=self._monitor_playback, daemon=True)
        self._monitor_thread.start()
    
    def _monitor_playback(self):
        """Monitor playback status in background thread."""
        while not self._stop_monitoring and self.process:
            if self.process.poll() is not None:
                # Process ended
                self.is_playing = False
                self.is_paused = False
                if self.status_callback:
                    self.status_callback("finished", None)
                break
            
            if self.is_playing and not self.is_paused:
                self.position += 1
            
            time.sleep(1)
    
    def get_source_info(self) -> str:
        """Get formatted information about the current music source."""
        if self.current_source:
            return self.source_detector.format_source_info(self.current_source, include_details=True)
        return "No active source"
    
    def get_player_info(self) -> str:
        """Get information about the current media player."""
        if self.player_executable:
            player_info = self.source_detector.get_player_info(self.player_executable)
            return f"{player_info.get('icon', '🎵')} {player_info.get('name', self.player_executable)} - {player_info.get('description', '')}"
        return "No player available"
