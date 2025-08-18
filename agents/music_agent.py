import shutil
import subprocess

class MusicAgent:
    """The Music Agent, responsible for playing local audio files and remote streams."""

    def __init__(self, logger):
        """Initializes the Music Agent and finds a suitable player."""
        self.logger = logger
        self.player_executable = self._find_player()
        self.process = None  # To keep track of the music player process
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

    def play_track(self, track_path: str):
        """Plays the given audio track, which can be a local file path or a URL."""
        if self.process and self.process.poll() is None:
            self.logger.warning("Another track is already playing. Stopping it first.")
            self.stop()

        if not self.player_executable:
            self.logger.error("Cannot play track: No music player available.")
            return
        
        if not track_path:
            self.logger.warning("No track path or URL provided to play.")
            return

        log_message = (
            f"Streaming from URL: {track_path}" 
            if track_path.startswith(("http://", "https://")) 
            else f"Playing local file: {track_path}"
        )
        self.logger.info(log_message)

        try:
            self.process = subprocess.Popen(
                [self.player_executable, track_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception as e:
            self.logger.error(f"Failed to play '{track_path}': {e}", exc_info=True)

    def stop(self):
        """Stops the currently playing track."""
        if self.process and self.process.poll() is None: # Check if process is running
            self.logger.info("Stopping music player...")
            self.process.terminate()
            self.process.wait() # Wait for the process to terminate
            self.logger.info("Music player stopped.")
            self.process = None
        else:
            self.logger.info("No music is currently playing.")
