# Personal DJ: Your AI-Powered Music Companion!

Welcome to Personal DJ! This awesome project brings the power of AI to your music experience. Imagine having a smart DJ that can understand your music taste, chat with you, and play the perfect songs for any mood. That's what Personal DJ is all about!

## What is Personal DJ?

Personal DJ is a smart application that uses different AI "agents" to create a unique music experience:

- **DJ Agent**: The main brain of the operation, coordinating everything.
- **Music Agent**: Your personal music expert, ready to find and play your favorite tunes.
- **Voice Agent**: Allows you to interact with your DJ using your voice, just like talking to a friend.


## Running Your Personal DJ

Now for the fun part! To start your Personal DJ, simply run the `launch-ai-dj.bat` file. You can do this by double-clicking it in your file explorer or by running this command in your terminal:

```bash
./launch-ai-dj.bat
```

### A Note on API Keys

This project uses a `.env` file to manage secret information, like API keys for music or voice services. You'll need to create a file named `.env` in the main project folder and add your keys there. It might look something like this:

```
# .env file
VOICE_API_KEY=your_secret_voice_api_key
MUSIC_API_KEY=your_secret_music_api_key
```

And that's it! You're all set to enjoy your very own AI-powered Personal DJ. Have fun!

Personal DJ is a lightweight, fully‐local AI disc-jockey.  
It turns a short text *vibe* ("late-night synthwave", "sunset lo-fi", …) into spoken commentary followed by a matching track from your music library.

Key features:
1. **Local LLM** via [Ollama](https://ollama.ai/) – no external OpenAI calls.
2. **Text-to-speech** with [ElevenLabs](https://elevenlabs.io/), with a local offline TTS fallback.
3. **Gap-less playback** through `mpv` (change to `ffplay` or `vlc` if you prefer).
4. **Tiny footprint** – <50 lines per agent, single-file CLI entry-point, container image ≤ 1 GB.

---

## Project layout
```
├─ run.py                 # CLI entry-point
├─ core/                  # Shared orchestration code
│  └─ dispatcher.py       # Routes user input through the three agents
├─ agents/                # Each capability lives in a tiny self-contained agent
│  ├─ dj_agent.py         # Calls Ollama LLM and picks a random track
│  ├─ voice_agent.py      # Converts commentary to speech via ElevenLabs or a local TTS engine
│  └─ music_agent.py      # Plays mp3 files with mpv
├─ config/                # Example .env (API keys, paths)
├─ scripts/               # Windows / Powershell helpers for local dev
├─ installer/             # Inno Setup output for a Windows desktop build
├─ Dockerfile             # Container build (see below)
├─ requirements.txt       # Python dependencies
└─ README.md              # You are here 👋
```

### Core flow
```
User → run.py → Dispatcher → [DJAgent → VoiceAgent → MusicAgent] → Speakers
```
1. **DJAgent** takes the text *vibe*, chats with the local LLM, and selects a random `.mp3` under `MUSIC_DIR`.
2. **VoiceAgent** converts the commentary to speech (uses a local offline TTS engine if `ELEVEN_API_KEY` is missing).
3. **MusicAgent** plays the spoken mp3 first, then the selected track.

## Troubleshooting

If you run into issues, here are a few steps to diagnose the problem:

1.  **Run the Environment Checker**: The first thing you should do is run the diagnostic script to check your setup. From the project's root directory, run:

    ```bash
    python check_setup.py
    ```

    This script will verify that all necessary tools (`ollama`, `mpv`, etc.) are installed, your `.env` file is configured correctly, and your music directory is accessible.

2.  **Check the Log File**: The application writes detailed logs to `personal_dj.log`. This file is created in the project's root directory when you run the app. It contains step-by-step information about what the application is doing and any errors it encounters. This is the best place to look for specific error messages.

3.  **Common Issues**:
    *   **"Ollama command not found"**: Make sure you have installed [Ollama](https://ollama.ai/) and that it's accessible from your terminal. The `check_setup.py` script can verify this.
    *   **"No supported music player found"**: You need to have `mpv`, `ffplay`, or `vlc` installed and available in your system's PATH.
    *   **Voice Agent Fallback**: If your `ELEVEN_API_KEY` is missing from your `.env` file, the application will automatically use a local, offline text-to-speech engine. The voice quality may be lower than ElevenLabs, but it allows the application to run without an internet connection or API key.
    *   **"Music directory not found"**: The path to your music library is hardcoded in `agents/dj_agent.py` and `check_setup.py`. You'll need to edit this path to point to your local music folder.

---

## Installation

Choose your environment:

- [Windows](#windows)
- [macOS](#macos)
- [Linux](#linux)
- [Docker](#docker-quick-start-⚡)

### Windows

1.  **Install Prerequisites**:
    - **Python 3.10+**: Install from the [Microsoft Store](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5) or [python.org](https://www.python.org/downloads/).
    - **mpv**: A powerful, free media player. Install it with a package manager like [Winget](https://winstall.app/apps/9P98F7M3T08F) or [Chocolatey](https://community.chocolatey.org/packages/mpv):
      ```powershell
      winget install mpv
      ```

2.  **Clone the Repository**:
    ```powershell
    git clone https://github.com/curlyphries/personal-dj.git
    cd personal-dj
    ```

3.  **Set Up a Virtual Environment and Install Dependencies**:
    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```

### macOS

1.  **Install Prerequisites** (using [Homebrew](https://brew.sh/)):
    ```bash
    brew install python mpv
    ```

2.  **Clone the Repository**:
    ```bash
    git clone https://github.com/curlyphries/personal-dj.git
    cd personal-dj
    ```

3.  **Set Up a Virtual Environment and Install Dependencies**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

### Linux

1.  **Install Prerequisites** (using `apt` for Debian/Ubuntu):
    ```bash
    sudo apt update && sudo apt install python3 python3-venv mpv espeak-ng
    ```
    *Note: `espeak-ng` is required for the local TTS fallback.* 

2.  **Clone the Repository**:
    ```bash
    git clone https://github.com/curlyphries/personal-dj.git
    cd personal-dj
    ```

3.  **Set Up a Virtual Environment and Install Dependencies**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
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
