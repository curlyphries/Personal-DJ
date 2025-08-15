#!/usr/bin/env python3
"""
Entry-point for the local AI-DJ MVP.

This script can launch the application in either GUI or CLI mode.

Flow:
1. Ask user for a vibe / command.
2. DJAgent generates commentary + track choice.
3. VoiceAgent converts commentary to speech.
4. MusicAgent plays commentary audio, then the chosen song.
"""

import sys
from PySide6.QtWidgets import QApplication

from core.log_setup import setup_logging
from core.dispatcher import Dispatcher
from gui.main_window import MainWindow

# Set up logging at the application's entry point
logger = setup_logging()

def run_gui():
    """Initializes and runs the GUI for the Personal DJ application."""
    logger.info("--- Starting Personal DJ GUI ---")
    try:
        app = QApplication(sys.argv)
        window = MainWindow(logger)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logger.critical(f"An unexpected error occurred while launching the GUI: {e}", exc_info=True)
    finally:
        logger.info("--- Personal DJ GUI has shut down ---")

def run_cli():
    """Runs the Personal DJ application in command-line interface mode."""
    logger.info("--- Starting Personal DJ CLI ---")
    dispatcher = Dispatcher(logger)
    print("🎧  Local AI-DJ ready. Type 'stop' to halt playback, or 'quit' to exit.")

    try:
        while True:
            user_msg = input("You > ").strip()
            if user_msg.lower() in {"quit", "exit"}:
                logger.info("Exiting CLI mode.")
                break
            elif user_msg.lower() == "stop":
                logger.info("Stopping music playback.")
                dispatcher.music_agent.stop()
                print("Playback stopped.")
                continue

            commentary, track_title, track_url = dispatcher.dj_agent.respond(user_msg)
            print(f"\nDJ Echo: {commentary}")

            commentary_audio_path = dispatcher.voice_agent.speak(commentary)
            if commentary_audio_path:
                dispatcher.music_agent.play_track(commentary_audio_path)

            if track_url:
                print(f"Now Playing: {track_title}")
                dispatcher.music_agent.play_track(track_url)
            else:
                print("No music track was selected.")

    except KeyboardInterrupt:
        logger.info("CLI interrupted by user.")
    except Exception as e:
        logger.critical(f"An unexpected error occurred in the CLI: {e}", exc_info=True)
    finally:
        dispatcher.music_agent.stop()  # Ensure music is stopped on exit
        logger.info("--- Personal DJ CLI has shut down ---")

def main():
    """Parses command-line arguments to run the app in GUI or CLI mode."""
    if '--cli' in sys.argv:
        run_cli()
    else:
        run_gui()

if __name__ == "__main__":
    main()
