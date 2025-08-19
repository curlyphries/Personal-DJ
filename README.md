# Personal DJ: Your AI-Powered Music Companion!

Welcome to Personal DJ! This awesome project brings the power of AI to your music experience. Imagine having a smart DJ that can understand your music taste, chat with you, and play the perfect songs for any mood. That's what Personal DJ is all about!

## What is Personal DJ?

Personal DJ is a smart application that uses different AI "agents" to create a unique music experience:

- **DJ Agent**: The main brain of the operation, coordinating everything.
- **Music Agent**: Your personal music expert, ready to find and play your favorite tunes.
- **Voice Agent**: Allows you to interact with your DJ using your voice, just like talking to a friend.

## Setup and Installation

Follow these steps to get your Personal DJ up and running.

### 1. Prerequisites

First, ensure you have the necessary software for your operating system.

<details>
<summary><strong>Windows</strong></summary>

- **Git**: Download and install from the [official Git website](https://git-scm.com/downloads/).
- **Python 3.10+**: Install from the [Microsoft Store](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5) or [python.org](https://www.python.org/downloads/).
- **mpv Media Player**: A powerful, free media player. Install it with a package manager like [Winget](https://winstall.app/apps/9P98F7M3T08F) or [Chocolatey](https://community.chocolatey.org/packages/mpv).
  powershell
  winget install mpv
  
</details>

<details>
<summary><strong>macOS</strong></summary>

- You'll need [Homebrew](https://brew.sh/), the package manager for macOS.
- Install prerequisites with this command:
  bash
  brew install python git mpv
  
</details>

<details>
<summary><strong>Linux (Debian/Ubuntu)</strong></summary>

- Install prerequisites using `apt`:
  bash
  sudo apt update && sudo apt install python3 python3-venv git mpv espeak-ng
  - *Note: `espeak-ng` is required for the local TTS fallback if you don't use the ElevenLabs API.*

</details>

### 2. Clone the Repository

Open a terminal and run this command to download the project:

bash
git clone https://github.com/curlyphries/personal-dj.git
cd personal-dj

### 3. Set Up a Virtual Environment

This creates an isolated Python environment for the project.

- **Windows**: `python -m venv .venv && .\.venv\Scripts\activate`
- **macOS/Linux**: `python3 -m venv .venv && source .venv/bin/activate`

### 4. Install Dependencies

With the virtual environment activated, install the required packages.

- **Windows**: `pip install -r requirements-win.txt`
- **macOS/Linux**: `pip install -r requirements-unix.txt`

### 5. Set Up Your Navidrome Server 

This application acts as a **client** to a [Navidrome](https://www.navidrome.org/) music streaming server. You must have your own Navidrome instance running. You can run Navidrome via its native binary; see the Navidrome docs for installation instructions relevant to your OS.

1.  Download the latest Navidrome release for your platform and unzip it.
2.  Create a configuration file pointing `musicFolder` to your music directory and set a data directory for Navidrome’s database.


3.  **Start Navidrome**: Run the `navidrome` binary and monitor its console for "HTTP server listening on".
4.  **Create a User**: Open `http://localhost:4533` in your browser and create your administrator account.

### 6. Configure the Application

Create a `.env` file by copying the example (`cp .env.example .env` or `copy .env.example .env`) and fill in the following details:

- `NAVIDROME_URL`: The URL of your Navidrome server (e.g., `http://localhost:4533`).
- `NAVIDROME_USER`: The username you created in Navidrome.
- `NAVIDROME_PASS`: The password for your Navidrome user.
- `ELEVEN_API_KEY`: Your API key for ElevenLabs. If you leave this blank, the app will fall back to a local TTS engine (requires `espeak-ng` on Linux/macOS).

### 7. Run the App

You can run the application in two modes:

- **GUI Mode (Default)**: `python run.py`
- **CLI Mode**: `python run.py --cli`

### 8. Troubleshooting

-   **`RuntimeError: No supported music player found`**: The app requires `mpv`, `ffplay`, or `vlc`. Install one, for example: `sudo apt install mpv`.
-   **`RuntimeError: Local TTS fallback requires 'espeak-ng'`**: Occurs on Linux/macOS if the `ELEVEN_API_KEY` is missing and `espeak-ng` is not installed. Fix by providing the API key or installing the engine: `sudo apt install espeak-ng`.
-   **`ModuleNotFoundError` or other Python errors**: Ensure your virtual environment is active and you've installed the correct `requirements` file for your OS.

---


---

## Development scripts
• `scripts/run_simple.ps1` – quick Powershell runner for Windows.  
• `scripts/interactive_run.ps1` – launches with live-reload via `watchdog`.

---

## Packaging
The `installer/` folder contains an *Inno Setup* script (`installer.iss`) and a already-compiled `AI-DJ-Setup.exe` for a native Windows installer.  
Run `compile_installer.ps1` after updating version / icon assets.

---

## Contributing
PRs are welcome!  If you add a new capability, consider keeping it in its own `agents/` module and wiring it up through `core/dispatcher.py`.

---

## License
MIT © 2025 David


A minimal AI disc-jockey that:
1. Takes a text vibe prompt
2. Generates commentary with a local Ollama LLM
3. Converts commentary → speech via ElevenLabs
4. Plays speech and a music track

## Notes
* `MUSIC_DIR` must point to your music folder when running the application.
* Ollama models download on first use; ensure the application has internet access on first run or pre-download models via the Ollama CLI.
