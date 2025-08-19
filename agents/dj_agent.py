import os
import subprocess
from dotenv import load_dotenv
import platform

# libsonic is not available on Windows, so we'll guard the import.
try:
    import libsonic
except ImportError:
    libsonic = None

from core.user_profile import UserProfile

# Load environment variables from .env file
load_dotenv()

class DJAgent:
    """The DJ agent, responsible for generating commentary and selecting tracks from Navidrome."""
    MODEL = "gemma3:4b"  # keep small; swap later

    def __init__(self, logger, profile_name: str = "default"):
        """Initializes the DJ agent and connects to Navidrome."""
        self.logger = logger
        self.navidrome_client = None
        self.user_profile = UserProfile(profile_name)
        self._connect_to_navidrome()

    def _connect_to_navidrome(self):
        if not libsonic:
            self.logger.warning(
                "'libsonic' library not found, Navidrome connection is disabled. "
                "This is expected on Windows."
            )
            self.navidrome_client = None
            return

        self.logger.info("Attempting to connect to Navidrome...")
        try:
            url = os.getenv("NAVIDROME_URL")
            user = os.getenv("NAVIDROME_USER")
            password = os.getenv("NAVIDROME_PASS")

            if not all([url, user, password]):
                self.logger.error("Navidrome credentials not found in .env file.")
                return

            self.navidrome_client = libsonic.Connection(
                baseUrl=url, username=user, password=password, appName="PersonalDJ"
            )
            self.navidrome_client.ping()
            self.logger.info("Successfully connected to Navidrome.")
        except Exception as e:
            self.logger.error(f"Failed to connect to Navidrome: {e}")
            self.navidrome_client = None

    def _ollama_chat(self, prompt: str) -> str:
        self.logger.info("Generating commentary with Ollama...")
        try:
            result = subprocess.run(
                ["ollama", "run", self.MODEL, prompt],
                text=True, capture_output=True, check=True, timeout=30
            )
            response = result.stdout.strip()
            self.logger.info(f"Ollama response: '{response}'")
            return response
        except Exception as e:
            self.logger.error(f"An unexpected error occurred with Ollama: {e}", exc_info=True)
            return "Let's get right to the music."

    def _get_now_playing(self) -> tuple[str | None, str | None]:
        """Returns the currently playing track in Navidrome, if any."""
        if not self.navidrome_client:
            self.logger.error("Cannot check now playing: Not connected to Navidrome.")
            return None, None

        self.logger.info("Checking Navidrome for currently playing track...")
        try:
            now_playing = self.navidrome_client.getNowPlaying()
            entries = now_playing.get("nowPlaying", {}).get("entry")
            if not entries:
                self.logger.info("No active sessions found in Navidrome.")
                return None, None

            # API may return a list or a single dict
            entry = entries[0] if isinstance(entries, list) else entries
            song_title = f"{entry['artist']} - {entry['title']}"
            self.logger.info(f"Detected currently playing track: '{song_title}'")
            return song_title, None
        except Exception as e:
            self.logger.error(f"Failed to fetch now playing track from Navidrome: {e}")
            return None, None

    def _get_track_from_navidrome(self) -> tuple[str | None, str | None]:
        """Fetches a random track from Navidrome and returns its title and stream URL."""
        if not self.navidrome_client:
            self.logger.error("Cannot get track: Not connected to Navidrome.")
            return None, None

        self.logger.info("Fetching a random track from Navidrome...")
        try:
            random_songs = self.navidrome_client.getRandomSongs(size=1)
            if not random_songs or 'song' not in random_songs['randomSongs']:
                self.logger.warning("Navidrome returned no random songs.")
                return None, None

            song = random_songs['randomSongs']['song'][0]
            song_id = song['id']
            song_title = f"{song['artist']} - {song['title']}"
            self.logger.info(f"Selected track: '{song_title}' (ID: {song_id})")

            # Get the stream URL for the selected song
            stream_url = self.navidrome_client.getStreamUrl(sid=song_id)
            return song_title, stream_url
        except Exception as e:
            self.logger.error(f"Failed to fetch track from Navidrome: {e}")
            return None, None

    def respond(self, user_msg: str) -> tuple[str, str | None, str | None]:
        self.logger.info(f"DJ Agent responding to: '{user_msg}'")
        
        # Get personalized context from user profile
        personalized_context = self.user_profile.get_personalized_prompt_context()
        
        # Record this interaction
        self.user_profile.record_interaction("user_request", {"message": user_msg, "timestamp": self.user_profile.last_updated})
        
        # Create personalized prompt
        prompt = (
            f"{personalized_context} "
            f"User said: {user_msg}\n"
            "Reply with one-sentence commentary that reflects your personality and what you know about the user. "
            "Do NOT mention the track path or title."
        )
        
        commentary = self._ollama_chat(prompt)
        track_title, track_url = self._get_track_from_navidrome()
        return commentary, track_title, track_url
