import os
import subprocess
from dotenv import load_dotenv
import libsonic

# Load environment variables from .env file
load_dotenv()

class DJAgent:
    """The DJ agent, responsible for generating commentary and selecting tracks from Navidrome."""
    MODEL = "gemma3:4b"  # keep small; swap later

    def __init__(self, logger):
        """Initializes the DJ agent and connects to Navidrome."""
        self.logger = logger
        self.navidrome_client = None
        self._connect_to_navidrome()

    def _connect_to_navidrome(self):
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
        prompt = (
            "You are DJ-Echo, a cool late-night radio host. "
            f"User said: {user_msg}\n"
            "Reply with one-sentence commentary. Do NOT mention the track path or title."
        )
        commentary = self._ollama_chat(prompt)
        track_title, track_url = self._get_track_from_navidrome()
        return commentary, track_title, track_url
