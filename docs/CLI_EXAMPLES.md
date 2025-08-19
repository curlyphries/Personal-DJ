# Personal DJ - CLI Usage Examples

This guide provides comprehensive examples of using Personal DJ in command-line interface mode.

## 🚀 Getting Started

### Starting CLI Mode

```powershell
# Navigate to your Personal DJ directory
cd C:\Users\David\CascadeProjects\Personal-DJ

# Activate virtual environment
.\.venv\Scripts\activate

# Start CLI mode
python run.py --cli
```

**Expected Output:**
```
🎧  Local AI-DJ ready. Available commands:
  • Enter a vibe to start music
  • 'pause' - pause current track
  • 'resume' - resume paused track
  • 'stop' - stop current track
  • 'skip' - skip current track
  • 'volume <0-100>' - set volume
  • 'status' - show current status
  • 'quit' - exit

You > 
```

## 🎵 Basic Music Playback Examples

### Starting Music with Vibes

```powershell
You > play some chill lo-fi beats
```
**Response:**
```
DJ Echo: Perfect for a relaxed evening - let's dive into some smooth lo-fi vibes.

Now Playing: Chillhop Essentials - Lofi Hip Hop
```

```powershell
You > I need energetic workout music
```
**Response:**
```
DJ Echo: Time to pump up the energy! Here's something to get your heart racing.

Now Playing: High Energy Workout Mix - Electronic Beats
```

```powershell
You > something nostalgic from the 90s
```
**Response:**
```
DJ Echo: Taking you back to the golden decade! Here's a classic that'll bring back memories.

Now Playing: Nirvana - Smells Like Teen Spirit
```

## 🎛️ Music Control Examples

### Playback Controls

```powershell
# Pause current track
You > pause
Music paused.

# Resume playback
You > resume
Music resumed.

# Stop completely
You > stop
Playback stopped.

# Skip to next (stops current for new vibe)
You > skip
Track skipped. Ready for a new vibe.
```

### Volume Control

```powershell
# Set volume to 50%
You > volume 50
Volume set to 50%

# Set volume to maximum
You > volume 100
Volume set to 100%

# Set volume very low
You > volume 10
Volume set to 10%

# Invalid volume (shows usage)
You > volume 150
Usage: volume <0-100>
```

## 📊 Status Information Examples

### Basic Status Check

```powershell
You > status
```
**Response:**
```
Status: Playing
Track: Chillhop Essentials - Lofi Hip Hop
Volume: 75%
Position: 45s
Source: 🎵 Navidrome Server via 🎬 MPV Media Player (Server: localhost, API: Subsonic API)
```

### Status When Stopped

```powershell
You > status
```
**Response:**
```
Status: Stopped
Track: None
Volume: 75%
Position: 0s
Player: 🎬 MPV Media Player - Free, open source, and cross-platform media player
```

### Status When Paused

```powershell
You > status
```
**Response:**
```
Status: Paused
Track: Jazz Classics - Miles Davis
Volume: 60%
Position: 120s
Source: 🎵 Personal Music Library via 🎬 MPV Media Player (Location: Music, Type: Audio)
```

## 🎯 Real-World Usage Scenarios

### Scenario 1: Morning Routine

```powershell
You > good morning, play something upbeat to start my day
DJ Echo: Good morning! Let's kick off your day with some energizing tunes.

Now Playing: Feel Good Inc. - Gorillaz

You > volume 40
Volume set to 40%

You > status
Status: Playing
Track: Feel Good Inc. - Gorillaz
Volume: 40%
Position: 30s
Source: 🎵 Navidrome Server via 🎬 MPV Media Player

# Later...
You > stop
Playback stopped.
```

### Scenario 2: Work Focus Session

```powershell
You > I need instrumental music for deep focus work
DJ Echo: Creating the perfect atmosphere for concentration with some ambient instrumentals.

Now Playing: Brian Eno - Music for Airports

You > volume 25
Volume set to 25%

# After some time, check what's playing
You > status
Status: Playing
Track: Brian Eno - Music for Airports
Volume: 25%
Position: 480s
Source: 📺 YouTube via 🎬 MPV Media Player (Host: youtube.com)

# Pause for a meeting
You > pause
Music paused.

# Resume after meeting
You > resume
Music resumed.
```

### Scenario 3: Evening Wind-Down

```powershell
You > play something relaxing for bedtime
DJ Echo: Time to unwind with some soothing melodies perfect for relaxation.

Now Playing: Ludovico Einaudi - Nuvole Bianche

You > volume 20
Volume set to 20%

# Check source
You > status
Status: Playing
Track: Ludovico Einaudi - Nuvole Bianche
Volume: 20%
Position: 90s
Source: 🎵 Personal Music Library via 🎬 MPV Media Player (Location: Classical, Type: Audio)

# Stop before sleep
You > stop
Playback stopped.

You > quit
```

### Scenario 4: Party Playlist Management

```powershell
You > pump up the party with some dance hits
DJ Echo: Let's get this party started with some infectious dance beats!

Now Playing: Daft Punk - One More Time

You > volume 85
Volume set to 85%

# Someone doesn't like this song
You > skip
Track skipped. Ready for a new vibe.

You > more electronic dance music
DJ Echo: Keeping the energy high with another electronic banger!

Now Playing: Calvin Harris - Feel So Close

# Check what's playing
You > status
Status: Playing
Track: Calvin Harris - Feel So Close
Volume: 85%
Position: 60s
Source: 🎧 Spotify via 🎬 MPV Media Player (Host: spotify.com)
```

## 🔄 Advanced Interaction Patterns

### Mood-Based Requests

```powershell
# Emotional states
You > I'm feeling melancholy today
You > something to cheer me up
You > music for when I'm angry
You > romantic music for dinner

# Activity-based
You > coding music
You > driving music
You > cleaning the house music
You > studying background music

# Genre exploration
You > introduce me to jazz fusion
You > some underground hip hop
You > classic rock from the 70s
You > modern classical composers
```

### Contextual Requests

```powershell
# Time-based
You > good morning music
You > late night vibes
You > afternoon pick-me-up
You > Sunday morning relaxation

# Weather-based
You > rainy day music
You > sunny day playlist
You > music for a stormy evening
You > snow day vibes

# Seasonal
You > autumn mood music
You > summer road trip songs
You > winter cozy vibes
You > spring awakening music
```

## 🎵 Source Detection Examples

### Different Source Types in Action

**Navidrome Server:**
```powershell
You > play my favorite jazz album
Now Playing: Miles Davis - Kind of Blue
Source: 🎵 Navidrome Server via 🎬 MPV Media Player (Server: localhost, API: Subsonic API)
```

**Local Files:**
```powershell
You > play something from my local collection
Now Playing: The Beatles - Abbey Road
Source: 🎵 Personal Music Library via 🎬 MPV Media Player (Location: Music, Type: Audio)
```

**YouTube:**
```powershell
You > play that viral song from youtube
Now Playing: Viral Hit - Artist Name
Source: 📺 YouTube via 🎬 MPV Media Player (Host: youtube.com)
```

**Radio Stream:**
```powershell
You > tune into some internet radio
Now Playing: Jazz FM Live Stream
Source: 📻 Radio Stream via 🎬 MPV Media Player (Host: jazzfm.com)
```

## 🛠️ Troubleshooting Examples

### Common Issues and Solutions

**No Music Playing:**
```powershell
You > play some music
DJ Echo: Here's something great for you!

Now Playing: None

You > status
Status: Stopped
Track: None
Volume: 70%
Position: 0s
Player: 🎬 MPV Media Player - Free, open source, and cross-platform media player

# Check if MPV is installed
# Verify audio settings
# Check logs for errors
```

**Volume Issues:**
```powershell
You > volume 50
Volume set to 50%

# If no audio, check:
You > status
# Look for source information
# Verify system audio isn't muted
```

**Source Connection Problems:**
```powershell
You > status
Status: Stopped
Track: None
Source: ❓ Unknown Source via 🎬 MPV Media Player

# Check Navidrome connection
# Verify .env configuration
# Test network connectivity
```

## 💡 Pro Tips

### Efficient CLI Usage

1. **Quick Commands**: Use single words for common actions
   ```powershell
   You > pause
   You > resume
   You > stop
   ```

2. **Status Monitoring**: Check status regularly during long sessions
   ```powershell
   You > status
   ```

3. **Volume Management**: Set appropriate volume for different times
   ```powershell
   You > volume 30  # Morning
   You > volume 60  # Afternoon
   You > volume 20  # Evening
   ```

4. **Graceful Exit**: Always use quit to properly close
   ```powershell
   You > quit
   ```

### Personalization Tips

1. **Be Specific**: The more specific your requests, the better the results
   ```powershell
   You > upbeat 80s synthwave for coding
   ```

2. **Use Context**: Mention your activity or mood
   ```powershell
   You > relaxing music for reading
   ```

3. **Explore Genres**: Ask for introductions to new music
   ```powershell
   You > introduce me to ambient techno
   ```

## 🎧 Complete Session Example

Here's a complete CLI session showing various features:

```powershell
C:\Users\David\CascadeProjects\Personal-DJ> python run.py --cli

🎧  Local AI-DJ ready. Available commands:
  • Enter a vibe to start music
  • 'pause' - pause current track
  • 'resume' - resume paused track
  • 'stop' - stop current track
  • 'skip' - skip current track
  • 'volume <0-100>' - set volume
  • 'status' - show current status
  • 'quit' - exit

You > good morning, play some energetic music to start my day

DJ Echo: Good morning! Let's energize your day with some uplifting beats.

Now Playing: The Killers - Mr. Brightside

You > volume 45
Volume set to 45%

You > status
Status: Playing
Track: The Killers - Mr. Brightside
Volume: 45%
Position: 30s
Source: 🎵 Navidrome Server via 🎬 MPV Media Player (Server: localhost, API: Subsonic API)

You > pause
Music paused.

You > resume
Music resumed.

You > skip
Track skipped. Ready for a new vibe.

You > something more chill for work
DJ Echo: Switching to a more focused vibe perfect for productivity.

Now Playing: Tycho - A Walk

You > volume 30
Volume set to 30%

You > status
Status: Playing
Track: Tycho - A Walk
Volume: 30%
Position: 15s
Source: 🎵 Personal Music Library via 🎬 MPV Media Player (Location: Electronic, Type: Audio)

You > stop
Playback stopped.

You > quit
```

This comprehensive guide shows how Personal DJ's CLI mode provides a powerful, flexible way to control your music experience through simple text commands while giving you complete visibility into your music sources and playback status.
