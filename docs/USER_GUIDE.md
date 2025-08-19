# Personal DJ - Complete User Guide

Welcome to Personal DJ! Your AI-powered music companion that learns your preferences and provides a personalized music experience.

## 🎵 What is Personal DJ?

Personal DJ is an intelligent music application that combines AI agents to create a unique listening experience:

- **DJ Agent**: Generates personalized commentary and selects tracks
- **Music Agent**: Handles playback with full control features
- **Voice Agent**: Converts commentary to speech
- **Profile System**: Remembers your preferences and personalizes interactions

## 🚀 Quick Start

### Installation

1. **Install Prerequisites** (Windows):
   ```powershell
   # Install Python 3.10+ from Microsoft Store or python.org
   # Install Git from git-scm.com
   # Install MPV media player
   winget install mpv
   ```

2. **Get the Code**:
   ```powershell
   git clone https://github.com/curlyphries/personal-dj.git
   cd personal-dj
   ```

3. **Set Up Environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements-win.txt
   ```

4. **Configure Settings**:
   ```powershell
   copy .env.example .env
   # Edit .env with your settings (see Configuration section)
   ```

### First Run

**Create Your Profile**:
```powershell
python -m core.profile_manager create "YourName"
```

**Launch the Application**:
```powershell
# GUI Mode (Recommended)
python run.py

# CLI Mode
python run.py --cli
```

## 🎛️ Music Controls

### GUI Controls

The GUI provides a comprehensive music control panel with:

- **▶ Play/⏸ Pause/⏹ Stop** buttons
- **⏭ Skip** to next track
- **Volume slider** (0-100%)
- **Progress bar** with time display
- **Current track** and **source information**

### CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `pause` | Pause current track | `pause` |
| `resume` | Resume paused track | `resume` |
| `stop` | Stop current track | `stop` |
| `skip` | Skip current track | `skip` |
| `volume <0-100>` | Set volume level | `volume 75` |
| `status` | Show playback status | `status` |
| `quit` | Exit application | `quit` |

## 🎵 Music Sources

Personal DJ automatically detects and displays information about your music sources:

### Supported Sources

| Source Type | Icon | Description | Example |
|-------------|------|-------------|---------|
| **Navidrome Server** | 🎵 | Self-hosted music streaming | `🎵 Navidrome Server via 🎬 MPV Media Player` |
| **Local Files** | 🎵 | Files on your computer | `🎵 Personal Music Library via 🎬 MPV Media Player` |
| **Streaming URLs** | 🌐 | Online streams | `🌐 Stream (example.com) via 🎬 MPV Media Player` |
| **YouTube** | 📺 | YouTube videos/music | `📺 YouTube via 🎬 MPV Media Player` |
| **Spotify** | 🎧 | Spotify streams | `🎧 Spotify via 🎬 MPV Media Player` |
| **Radio Streams** | 📻 | Internet radio | `📻 Radio Stream via 🎬 MPV Media Player` |

### Media Players

Personal DJ supports multiple media players:

| Player | Icon | Description | Features |
|--------|------|-------------|----------|
| **MPV** | 🎬 | Free, open source media player | Hardware acceleration, extensive format support |
| **VLC** | 🔶 | Popular cross-platform player | Universal codec support, streaming capabilities |
| **FFplay** | ⚡ | Lightweight FFmpeg player | Minimal, command-line based |

## 👤 User Profiles

### Creating Profiles

```powershell
# Interactive profile creation
python -m core.profile_manager create "ProfileName"

# List all profiles
python -m core.profile_manager list

# Edit existing profile
python -m core.profile_manager edit "ProfileName"
```

### Profile Features

**Music Preferences**:
- Favorite genres (rock, jazz, electronic, etc.)
- Energy levels (chill, moderate, high, intense)
- Preferred decades (80s, 90s, 2000s, etc.)
- Volume preferences
- Language preferences

**DJ Personality**:
- DJ name (DJ Echo, DJ Midnight, etc.)
- Style (casual, professional, quirky, mysterious)
- Chattiness level (minimal, moderate, chatty)
- Voice tone (friendly, cool, energetic, smooth)
- Custom catchphrases

**Personal Memories**:
- Music memories (concerts, favorite songs)
- Life events (important moments)
- Personal preferences (likes/dislikes)
- Custom notes with importance ratings (1-5)

### Sharing Profiles

**Export Profile**:
```powershell
python -m core.profile_manager export "ProfileName" --output "my_dj_profile.json"
```

**Import Profile**:
```powershell
# Import as new profile
python -m core.profile_manager import "profile_file.json" --name "NewName"

# Merge with existing profile
python -m core.profile_manager import "profile_file.json" --merge
```

## ⚙️ Configuration

### Environment Variables (.env file)

```env
# Navidrome Configuration (if using)
NAVIDROME_URL=http://localhost:4533
NAVIDROME_USER=your_username
NAVIDROME_PASS=your_password

# ElevenLabs TTS (optional)
ELEVEN_API_KEY=your_elevenlabs_api_key

# Music Directory (for local files)
MUSIC_DIR=C:\Users\YourName\Music
```

### Navidrome Setup (Optional)

If you want to use Navidrome as your music source:

1. **Download Navidrome** from [navidrome.org](https://www.navidrome.org/)
2. **Create Configuration** (`navidrome.toml`):
   ```toml
   MusicFolder = 'C:\Path\To\Your\Music'
   DataFolder = 'C:\Navidrome\data'
   ```
3. **Start Navidrome**: Run the executable
4. **Create User**: Visit `http://localhost:4533` and create an account
5. **Update .env**: Add your Navidrome credentials

## 🎯 Usage Examples

### Basic Usage

1. **Start the application**: `python run.py`
2. **Enter a vibe**: "Play some upbeat synthwave"
3. **Use controls**: Pause, adjust volume, skip tracks as needed
4. **Check source**: See where your music is coming from in the display

### Advanced Features

**Personalized Requests**:
- "Play something that matches my mood from yesterday"
- "I'm feeling nostalgic, play some 90s music"
- "Something energetic for my workout"

**Profile Management**:
- Add memories: "Remember that I love acoustic versions"
- Update preferences: Change favorite genres over time
- Share profiles: Export your profile to share with family

**Source Information**:
- View current source in GUI or CLI
- See detailed information about media player
- Track music source statistics

## 🔧 Troubleshooting

### Common Issues

**"No supported music player found"**:
- Install MPV: `winget install mpv`
- Or install VLC or FFmpeg

**"ModuleNotFoundError"**:
- Ensure virtual environment is activated: `.\.venv\Scripts\activate`
- Install dependencies: `pip install -r requirements-win.txt`

**No audio output**:
- Check Windows volume settings
- Ensure audio device is not muted
- Test with: `mpv some_audio_file.mp3`

**Navidrome connection failed**:
- Verify Navidrome is running: `http://localhost:4533`
- Check credentials in `.env` file
- Ensure network connectivity

### Getting Help

**View Logs**:
- Check `logs/personal_dj.log` for detailed information
- Enable debug logging for more details

**Status Information**:
- CLI: Type `status` to see current state
- GUI: Check the music control panel

**Profile Issues**:
- List profiles: `python -m core.profile_manager list`
- Recreate profile if corrupted

## 🎨 Customization

### DJ Personality

Customize your DJ's personality through profiles:
- **Casual**: "Hey there! Ready for some great tunes?"
- **Professional**: "Good evening. Let's explore some exceptional music."
- **Quirky**: "Buckle up, buttercup! Time for some sonic adventures!"
- **Mysterious**: "The shadows whisper of perfect melodies..."

### Music Preferences

Fine-tune your experience:
- **Genres**: Rock, Jazz, Electronic, Classical, Hip-Hop, etc.
- **Moods**: Happy, Melancholy, Energetic, Romantic, Chill
- **Energy**: Chill background music to intense workout tracks
- **Eras**: Focus on specific decades or time periods

### Memory System

Build a relationship with your DJ:
- **Important memories** (rated 4-5): Always considered in responses
- **Music memories**: Concert experiences, meaningful songs
- **Life events**: Context for music selection
- **Preferences**: Ongoing likes and dislikes

## 🔄 Updates and Maintenance

### Keeping Updated

```powershell
# Update the application
git pull origin main
pip install -r requirements-win.txt --upgrade

# Backup your profiles
python -m core.profile_manager export "YourProfile" --output "backup.json"
```

### Profile Maintenance

- **Regular exports**: Backup your profiles periodically
- **Clean up memories**: Remove outdated or irrelevant memories
- **Update preferences**: Adjust as your taste evolves
- **Share discoveries**: Export profiles to share with friends

## 🎵 Enjoy Your Personal DJ!

Your Personal DJ learns and grows with you, creating a unique musical experience that's truly yours. The more you interact with it, the better it becomes at understanding your preferences and providing the perfect soundtrack to your life.

**Happy listening!** 🎧
