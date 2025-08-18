from agents.dj_agent import DJAgent
from agents.music_agent import MusicAgent
from agents.voice_agent import VoiceAgent

class Dispatcher:
    """Coordinates the AI agents to create the Personal DJ experience."""

    def __init__(self, logger):
        """Initializes all the AI agents."""
        self.logger = logger
        self.logger.info("Dispatcher: Initializing agents...")
        # Pass the logger to each agent
        self.dj_agent = DJAgent(self.logger)
        self.music_agent = MusicAgent(self.logger)
        self.voice_agent = VoiceAgent(self.logger)

    def start(self):
        """Starts the main application loop."""
        self.logger.info("Personal DJ is ready. Type a vibe or 'quit' to exit.")
        while True:
            try:
                vibe = input("\nEnter a vibe (e.g., 'late-night synthwave'): ")

                if vibe.lower() == 'quit':
                    break

                self.logger.info(f"Vibe received: '{vibe}'. Engaging agents...")
                
                # 1. DJ Agent generates commentary and selects a music track.
                commentary, track_title, track_url = self.dj_agent.respond(vibe)
                
                # 2. Voice Agent turns the commentary into speech.
                commentary_audio_path = self.voice_agent.speak(commentary)

                # 3. Music Agent plays the commentary, then the music.
                if commentary_audio_path:
                    self.music_agent.play_track(commentary_audio_path)
                
                if track_url:
                    self.music_agent.play_track(track_url)
                else:
                    self.logger.warning("No music track was selected by the DJ Agent.")

            except Exception as e:
                self.logger.error(f"An error occurred in the main loop: {e}", exc_info=True)
                # The loop continues, making the app more resilient.

        self.logger.info("Dispatcher loop ended.")
