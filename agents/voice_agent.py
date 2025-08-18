"""
VoiceAgent: sends text to ElevenLabs TTS and returns a local mp3 path.
If the API key is missing, it falls back to printing the text to the console.
"""
import os
import platform
import requests
import shutil
import uuid
import tempfile
import pyttsx3

from dotenv import load_dotenv
load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
RACHEL_VOICE_ID = os.getenv("ELEVEN_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default voice is 'Rachel' from ElevenLabs

ENDPOINT = f"https://api.elevenlabs.io/v1/text-to-speech/{RACHEL_VOICE_ID}"

class VoiceAgent:
    """The Voice agent, responsible for text-to-speech."""

    def __init__(self, logger):
        """Initializes the Voice agent."""
        self.logger = logger
        self.tts_engine = None
        if not ELEVEN_API_KEY:
            self.logger.warning("ElevenLabs API key not found. Attempting to initialize local TTS fallback.")
            try:
                # On non-Windows systems, espeak-ng is required for pyttsx3 to work.
                if platform.system() != "Windows" and not shutil.which("espeak-ng"):
                    raise RuntimeError("Local TTS fallback requires 'espeak-ng'. Please install it (e.g., 'sudo apt install espeak-ng').")
                self.tts_engine = pyttsx3.init()
                self.logger.info("Local TTS engine initialized successfully.")
            except Exception as e:
                self.logger.error(f"Failed to initialize local TTS engine: {e}")
                self.tts_engine = None
        else:
            self.logger.info("Voice Agent: Initialized with ElevenLabs API.")

    def speak(self, text: str) -> str | None:
        """
        Generates audio from text using the ElevenLabs API and returns the audio file path.
        If the API key is missing, it prints the commentary to the console and returns an empty string.
        """
        if not ELEVEN_API_KEY:
            if self.tts_engine:
                return self._speak_local(text)
            else:
                self.logger.error("Local TTS engine not available. Falling back to console output.")
                print(f"\n--- DJ Commentary ---\n{text}\n---------------------")
                return None

        try:
            payload = {
                "text": text,
                "model_id": "eleven_multilingual_v2"
            }
            headers = {
                "xi-api-key": ELEVEN_API_KEY,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            }
            self.logger.info(f"Requesting TTS for: '{text}'")
            response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=30)
            response.raise_for_status()

            # Save the audio to a temporary file
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp3")
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            print(f"Voice Agent: Commentary saved to {output_path}")
            return output_path
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error calling ElevenLabs API: {e}")
            self.logger.info("Falling back to local TTS.")
            return self._speak_local(text)

    def _speak_local(self, text: str) -> str | None:
        """Generates audio from text using the local TTS engine."""
        try:
            self.logger.info(f"Generating local TTS for: '{text}'")
            temp_dir = tempfile.gettempdir()
            output_path = os.path.join(temp_dir, f"{uuid.uuid4()}.mp3")
            self.tts_engine.save_to_file(text, output_path)
            self.tts_engine.runAndWait()
            self.logger.info(f"Local TTS audio saved to {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Failed to generate local TTS audio: {e}")
            return None
