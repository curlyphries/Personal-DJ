# syntax=docker/dockerfile:1

# Base OS with apt package manager
FROM ubuntu:22.04

# ----------------------------
# 1️⃣  Install system packages
# ----------------------------
# • python3 / pip  → run the app
# • mpv           → play audio
# • curl          → fetch Ollama installer (if needed)
# • espeak-ng     → local TTS engine for Linux
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 python3-pip mpv curl espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Allow skipping Ollama install if using host's Ollama
ARG INSTALL_OLLAMA=true

# ----------------------------
# 2️⃣  Install Ollama CLI (optional)
# ----------------------------
# Only install if INSTALL_OLLAMA=true (default)
RUN if [ "$INSTALL_OLLAMA" = "true" ]; then \
        curl -fsSL https://ollama.com/install.sh | bash; \
    else \
        echo "Skipping Ollama installation (using host's Ollama)"; \
    fi

# ----------------------------
# 3️⃣  Set up project
# ----------------------------
WORKDIR /app

# Copy & install python deps first to leverage Docker layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the rest of the source
COPY . .

# Allow caller to override music dir; default matches agents.dj_agent.MUSIC_DIR
ENV MUSIC_DIR=/opt/navidrome/music

# ----------------------------
# 4️⃣  Runtime
# ----------------------------
# Interactive CLI by default; `docker run -it ai-dj` drops you straight in.
CMD ["python3", "run.py", "--cli"]
