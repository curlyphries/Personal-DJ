# Personal DJ: Your AI-Powered Music Companion!

Welcome to Personal DJ! This awesome project brings the power of AI to your music experience. Imagine having a smart DJ that can understand your music taste, chat with you, and play the perfect songs for any mood. That's what Personal DJ is all about!

## What is Personal DJ?

Personal DJ is a smart application that uses different AI "agents" to create a unique music experience:

- **DJ Agent**: The main brain of the operation, coordinating everything.
- **Music Agent**: Your personal music expert, ready to find and play your favorite tunes.
- **Voice Agent**: Allows you to interact with your DJ using your voice, just like talking to a friend.

## Installation

Follow these steps to get your Personal DJ up and running. First, choose your operating system for specific prerequisite commands.

### 1. Prerequisites

<details>
<summary><strong>Windows</strong></summary>

- **Git**: Download and install from the [official Git website](https://git-scm.com/downloads/).
- **Python 3.10+**: Install from the [Microsoft Store](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5) or [python.org](https://www.python.org/downloads/).
- **mpv Media Player**: A powerful, free media player. Install it with a package manager like [Winget](https://winstall.app/apps/9P98F7M3T08F) or [Chocolatey](https://community.chocolatey.org/packages/mpv).
  ```powershell
  winget install mpv
  ```

</details>

<details>
<summary><strong>macOS</strong></summary>

- You'll need [Homebrew](https://brew.sh/), the package manager for macOS.
- Install prerequisites with this command:
  ```bash
  brew install python git mpv
  ```

</details>

<details>
<summary><strong>Linux (Debian/Ubuntu)</strong></summary>

- Install prerequisites using `apt`:
  ```bash
  sudo apt update && sudo apt install python3 python3-venv git mpv espeak-ng
  ```
- *Note: `espeak-ng` is required for the local TTS fallback.*

</details>

### 2. Download the Code

Open a terminal (like Command Prompt, PowerShell, or Terminal) and run this command to download the project:

```bash
git clone https://github.com/curlyphries/personal-dj.git
cd personal-dj
```

### 3. Set Up a Virtual Environment

This step creates an isolated environment for the project's Python packages. Run these commands from the `personal-dj` directory.

- **On Windows**:
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  ```

- **On macOS and Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 4. Install Dependencies

With your virtual environment activated, install the required packages for your operating system.

- **On Windows**:
  ```powershell
  pip install -r requirements-win.txt
  ```

- **On macOS and Linux**:
  ```bash
  pip install -r requirements-unix.txt
  ```

### Environment Setup

Create a `.env` file in the project root (you can copy `config/example.env`) and set the following:

-   `ELEVEN_API_KEY`: Your ElevenLabs key. If omitted, the app will use a local, offline TTS engine.
-   `MUSIC_DIR`: Path to your music library (e.g., `C:/Users/YourUser/Music`). Defaults to `~/Music`.

### Running the App

Once installed, run the app from the project's root directory:

```bash
python run.py --cli
```

---

## Docker Quick Start ⚡

1.  **Build the Docker Image**:
    ```bash
    docker build -t ai-dj .
    ```

2.  **Run the Container**:
    Mount your music library and provide your environment variables. The entrypoint is the CLI mode.
    ```bash
    docker run -it --rm \
      -e ELEVEN_API_KEY="YOUR_KEY" \
      -v "/path/to/your/music:/music:ro" \
      ai-dj
    ```
    -   `--rm`: Cleans up the container after exit.
    -   `-v`: Mounts your local music directory into the container (read-only).
Inside the container you’ll see the prompt:
```
🎧  Local AI-DJ ready. Type 'quit' to exit.
You >
```
Type a vibe and enjoy!

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

## Quick start

```bash
# build
docker build -t ai-dj .

# run (interactive CLI)
docker run -it \
  -e ELEVEN_API_KEY=YOUR_KEY \
  -e ELEVEN_VOICE_ID=eleven_monolingual_v1 \
  -e MUSIC_DIR=/music \
  -v /host/path/to/mp3s:/music:ro \
  ai-dj
```

Inside the container you’ll see:
```
🎧  Local AI-DJ ready. Type 'quit' to exit.
You >
```

Type a vibe and the DJ will speak & play a track.

## Notes
* `MUSIC_DIR` defaults to `/opt/navidrome/music` but can be overridden.
* The image installs `mpv`; feel free to modify `MusicAgent.PLAYER` if you prefer `ffplay`.
* Ollama models are downloaded at first run; ensure the container has internet access or pre-pull models into `/root/.ollama`.
