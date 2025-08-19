# Personal DJ - Installation Guide

Welcome to Personal DJ! This guide provides a general overview of the installation process. For detailed, step-by-step instructions tailored to your operating system (Windows, macOS, or Linux), please see the main [**README.md**](../README.md#installation).

## 🪟 Windows – one-click installer

1. Download **AI-DJ-Setup.exe** from the Releases page.
2. Double-click and follow the wizard – it will:
   • Copy `ai-dj.exe` (bundled Python runtime)
   • Silently install required tools (mpv, Ollama) if missing
3. Leave “Run AI-DJ” checked on finish and enjoy!

<details>
<summary>What the installer does under the hood</summary>

| Component | Action |
|-----------|--------|
| **Python** | Embedded via PyInstaller – no separate install |
| **mpv** | Installed via `winget` if not found |
| **Ollama** | Downloaded & silent install for local LLM |

You can uninstall everything from *Add/Remove Programs* like any other app.

</details>

---

## General Steps

1.  **Install Prerequisites**:
    -   You will need **Python 3.10+**, a command-line music player like **mpv**, and **Git**.
    -   The main `README.md` provides specific commands for installing these on your OS.

2.  **Clone the Repository**:
    -   Download the project code using Git.

3.  **Install Python Dependencies**:
    -   Set up a virtual environment and install the required packages from `requirements.txt`.

4.  **Configure Environment Variables**:
    -   Create a `.env` file to store your `ELEVEN_API_KEY` (optional) and `MUSIC_DIR`.

5.  **Run the Application**:
    -   Launch the app from your terminal using `python run.py`.

For detailed commands and platform-specific notes, please refer to the [**README.md**](../README.md#installation).
