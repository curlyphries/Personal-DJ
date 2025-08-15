#!/usr/bin/env python3

"""
check_setup.py: A diagnostic tool to verify the environment for the Personal DJ.

This script checks for necessary dependencies, configuration files, and environment variables.
"""

import os
import sys
import shutil
from pathlib import Path
from dotenv import load_dotenv

# --- Configuration --- #
# A sensible default for the music directory, adjust if needed.
DEFAULT_MUSIC_DIR = Path.home() / "Music"
# This should match the path in agents/dj_agent.py
MUSIC_DIR = Path(os.getenv("MUSIC_DIR", DEFAULT_MUSIC_DIR))

# --- Helper Functions --- #

def check_command(command: str) -> bool:
    """Check if a command-line tool is available in the system's PATH."""
    if shutil.which(command):
        print(f"[OK] Found command: {command}")
        return True
    else:
        print(f"[FAIL] Command not found: {command}")
        return False

def check_env_file() -> bool:
    """Check if the .env file exists."""
    if Path(".env").exists():
        print("[OK] .env file found.")
        return True
    else:
        print("[FAIL] .env file not found. Please create it by copying from .env.example.")
        return False

def check_api_key() -> bool:
    """Check if the ElevenLabs API key is set, warn if not."""
    load_dotenv()
    if os.getenv("ELEVEN_API_KEY"):
        print("[OK] ELEVEN_API_KEY is set.")
    else:
        print("[WARN] ELEVEN_API_KEY is not set. App will use local TTS fallback.")
    return True  # Always return True as this is not a fatal error

def check_music_directory() -> bool:
    """Check if the music directory exists."""
    if MUSIC_DIR.exists() and MUSIC_DIR.is_dir():
        print(f"[OK] Music directory found at: {MUSIC_DIR}")
        return True
    else:
        print(f"[FAIL] Music directory not found at: {MUSIC_DIR}")
        print("       Please set the MUSIC_DIR environment variable or update the path in 'check_setup.py'.")
        return False

def check_local_tts() -> bool:
    """Check if the local TTS engine and its dependencies are set up correctly."""
    print("--- Checking Local TTS Engine ---")
    try:
        import pyttsx3
        # On Linux, pyttsx3 requires espeak-ng
        if sys.platform == "linux":
            if not check_command("espeak-ng"):
                print("[FAIL] `espeak-ng` is required for local TTS on Linux.")
                print("       Please install it using your package manager (e.g., `sudo apt install espeak-ng`).")
                return False

        engine = pyttsx3.init()
        print("[OK] Local TTS engine initialized successfully.")
        del engine
        return True
    except ImportError:
        print("[FAIL] `pyttsx3` is not installed. Please run `pip install -r requirements.txt`.")
        return False
    except Exception as e:
        print(f"[FAIL] Failed to initialize local TTS engine: {e}")
        return False

def check_music_player() -> bool:
    """Check for at least one supported music player."""
    players = ["mpv", "ffplay", "vlc"]
    for player in players:
        if shutil.which(player):
            print(f"[OK] Found music player: {player}")
            return True
    print(f"[FAIL] No supported music player found. Please install one of {players}.")
    return False

# --- Main Execution --- #

def main():
    """Run all diagnostic checks."""
    print("--- Running Personal DJ Environment Check ---")
    checks = {
        "Ollama Command": check_command("ollama"),
        "Music Player": check_music_player(),
        ".env File": check_env_file(),
        "ElevenLabs API Key": check_api_key(),
        "Local TTS Engine": check_local_tts(),
        "Music Directory": check_music_directory(),
    }

    print("\n--- Summary ---")
    if all(checks.values()):
        print("\n[SUCCESS] Your environment is configured correctly. You're ready to go!")
    else:
        print("\n[FAILURE] Some checks failed. Please review the messages above and consult the README.")

if __name__ == "__main__":
    main()
