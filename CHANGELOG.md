# Changelog

All notable changes to **Personal DJ** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [0.7.0] - 2025-08-15
### Added
- **Feat: Cross-Platform Support**: The application is now fully compatible with Windows, macOS, and Linux.

### Changed
- **Docs: OS-Specific Instructions**: The `README.md` and `INSTALL.md` have been rewritten to provide detailed, platform-specific installation guides.
- **Feat: Platform-Aware Setup**: The `check_setup.py` script now performs OS-specific diagnostics, including checks for `espeak-ng` on Linux.
- **Build: Dockerfile Enhancements**: The `Dockerfile` now installs `espeak-ng` to support local TTS in the container.
- **Build: Conditional Dependencies**: `requirements.txt` now only installs `pywin32` on Windows.

### Fixed
- **Docs: Repository URL**: Updated the repository URL in the documentation to the correct username.
- **Docs: Installation Guide**: Corrected the main installation guide in `README.md` to include virtual environment setup, preventing `externally-managed-environment` errors.
- **Build: Cross-Platform Dependencies**: Made the `libsonic-d` package a Windows-only dependency in `requirements.txt` to fix installation errors on Linux and macOS.

## [0.6.0] - 2025-08-15
### Added
- **Feat: Local TTS Fallback**: The application now includes a local, offline text-to-speech engine (`pyttsx3`) as a fallback for when the ElevenLabs API is not configured. This allows the application to provide spoken commentary without an internet connection.

### Changed
- **Refactor: Voice Agent**: The `VoiceAgent` has been updated to seamlessly switch between the ElevenLabs API and the local TTS engine.
- **Docs: Updated Documentation**: The `README.md` and `INSTALL.md` files have been updated to reflect the new local TTS functionality.
- **Feat: Improved Setup Script**: The `check_setup.py` script now verifies the local TTS installation and treats the ElevenLabs API key as optional.

## [0.5.0] - 2025-08-15
### Added
- **Feat: GUI Playback Controls**: Added "Stop" button to the GUI to allow users to stop music playback at any time.
- **Feat: Now Playing Display**: The GUI now displays the title of the currently playing song.
- **Feat: Enhanced CLI Mode**: The command-line interface now supports a "stop" command and displays the currently playing song.

### Changed
- **Fix: Improved GUI Error Handling**: The GUI now provides more specific feedback when errors occur during the DJ session.
- **Refactor: Music Agent**: The `MusicAgent` has been updated to allow for immediate interruption of music playback.

## [0.4.0] - 2025-08-15
### Added
- **Feat: GUI Implementation**: Replaced the command-line interface with a graphical user interface (GUI) built with PySide6.
- **Feat: Navidrome Integration**: The DJAgent now connects to Navidrome via the Subsonic API to select and stream music tracks.
- **Feat: Asynchronous Backend**: The core application logic now runs in a background thread to keep the UI responsive.
- **Feat: Configuration Update**: Added `.env.example` with settings for Navidrome credentials.
- **Fix: Music Playback**: The MusicAgent can now handle both local file paths and remote streaming URLs.

## [0.3.0] - 2025-08-15
### Added
- **Robust Logging & Error Handling**: Replaced all `print` statements with a centralized `logging` system that outputs to both the console and a `personal_dj.log` file.
- **Improved Error Resilience**: Enhanced error handling in all agents and the dispatcher to make the application more resilient to API failures and other runtime issues.
- **Diagnostic Script**: Created a `check_setup.py` script to help users verify their environment and troubleshoot common setup problems.
- **Troubleshooting Documentation**: Added a new "Troubleshooting" section to the `README.md` to guide users on how to diagnose and solve issues.

## [0.2.0] - 2025-08-15
### Added
- **Core Application Logic**: Implemented the full end-to-end logic for the Personal DJ. The application now takes a user's 'vibe' as input, uses the `DJAgent` to generate commentary and select a track, uses the `VoiceAgent` to generate audio for the commentary, and then uses the `MusicAgent` to play the commentary followed by the music track.

### Changed
- Refactored all agents (`DJAgent`, `VoiceAgent`, `MusicAgent`) to integrate with the core `Dispatcher`.
- Updated `launch-ai-dj.bat` to correctly run the application via `run.py`.

## [0.1.1] - 2025-06-15
### Added
- Expanded `README.md` to include full project overview, architecture, setup instructions, and contribution guidelines.

## [0.1.0] - 2025-06-01 (approx.)
### Added
- **Project Documentation**: Overhauled the `README.md` to provide a comprehensive, beginner-friendly guide to the project. The new `README.md` now includes a project description, prerequisites, and step-by-step instructions for installation and running the application.
- Initial project scaffolding with `run.py`, core dispatcher, and three minimal agents (`dj_agent`, `voice_agent`, `music_agent`).
- Dockerfile, example env, Windows installer script, and helper PowerShell scripts.
