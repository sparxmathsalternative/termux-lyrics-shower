# # 🎵 Termux Lyrics Shower

Real-time synced lyrics display with music playback for Termux. Download songs, fetch synced lyrics, and watch them scroll as the music plays!

## ✨ Features

- 🔍 **Auto-search & download** songs from YouTube
- 📝 **Synced LRC lyrics** from multiple sources
- 🎵 **Real-time display** with scrolling, centered, or list modes
- 💾 **Smart caching** for offline playback
- 🎨 **Visual effects** (glitch, flash, bass response)
- ⚙️ **Configurable** media players and platforms
- 🔎 **Fuzzy search** for cached files
- 📦 **Auto-install** dependencies

## 📥 Installation

```bash
pkg update
pkg install git
pkg install python3
git clone https://github.com/sparxmathsalternative/termux-lyrics-shower.git
cd termux-lyrics-shower
chmod +x install.sh
bash install.sh
```


## 🚀 Usage

### Basic Commands

```bash
# Download and play with synced lyrics
lyrics overnight - mirrors demo
lyrics shape of you
lyrics bohemian rhapsody

# Just fetch lyrics (no download/play)
lyrics -l "never gonna give you up"

# Show lyrics in terminal
lyrics -s -l "somebody that i used to know"

# Download music only (cache for later)
lyrics -m "rickroll"

# Play cached music (no lyrics)
lyrics -p "overnight"
```

### Management Commands

```bash
# List all cached music and lyrics
lyrics -ls
lyrics --list

# Clear cached music (with fuzzy search)
lyrics -cm overnight        # Find and delete matches
lyrics --clear-music        # Delete all music

# Clear cached lyrics
lyrics -cl "shape of you"   # Find and delete
lyrics --clear-lyrics       # Delete all lyrics
```

### Settings & Configuration

```bash
# Open interactive settings menu
lyrics --settings
lyrics --menu

# Settings include:
# - Platform (YouTube, SoundCloud, etc.)
# - Media player (ffplay, mpv)
# - Display mode (scrolling, centered, list)
# - Visual effects (glitch, flash)
# - Auto-install dependencies
```

### Advanced Options

```bash
# Use custom URLs for music/lyrics
lyrics -ext "https://example.com/song.mp3"
lyrics --music-url "https://cdn.com/audio.mp3" --lyrics-url "https://cdn.com/lyrics.lrc"

# Show help
lyrics -h
lyrics --help
```

## 🎨 Display Modes

**Scrolling Mode** (default)
- Shows current line highlighted
- Context lines above and below
- Smooth scrolling animation

**Centered Mode**
- Only current line in center of screen
- Minimal, focused display
- Great for small screens

**List Mode**
- All lyrics visible at once
- Current line highlighted
- Easy to see full song structure

Change in settings menu: `lyrics --settings`

## 🎭 Visual Effects

### Glitch Effect
- Unicode character distortion on current line
- Cyberpunk aesthetic

### Flash Effect
- Bright white flash on current line
- High contrast for emphasis

Enable in settings: `lyrics --settings` → Option 5/6

## 📁 File Structure

```
~/
├── Music/                  # Downloaded music files
│   └── *.mp3
├── .lyrics_cache/         # Cached lyrics
│   └── *.lrc
└── .config/
    └── lyrics-shower/
        └── config.json    # Configuration file
```

## 🔧 Configuration

Config file: `~/.config/lyrics-shower/config.json`

```json
{
  "platform": "youtube",
  "media_player": "ffplay",
  "display_mode": "scrolling",
  "use_graph": false,
  "effects": {
    "glitch": false,
    "flash": false,
    "bass_threshold": 0.7,
    "high_threshold": 0.8
  },
  "auto_install": true
}
```

## 📋 All Commands Reference

| Command | Aliases | Description |
|---------|---------|-------------|
| `lyrics <query>` | - | Download & play with lyrics |
| `-l, --lyrics` | - | Fetch lyrics only |
| `-s, --showcase` | - | Display lyrics (use with -l) |
| `-p, --play` | - | Play music only |
| `-m, --music` | - | Download music only |
| `-ls, --list` | - | List cached files |
| `-cm, --clear-music` | - | Delete cached music |
| `-cl, --clear-lyrics` | - | Delete cached lyrics |
| `--settings, --menu` | - | Settings menu |
| `-e, --effects` | - | Toggle effects |
| `-ext, --external-url` | - | Custom URL |
| `--music-url` | - | Custom music URL |
| `--lyrics-url` | - | Custom lyrics URL |
| `-h, --help` | - | Show help |

## 🎯 Examples

```bash
# Search and play
lyrics overnight - mirrors demo

# Just get lyrics for offline viewing
lyrics -l "your favorite song"
lyrics -s -l "your favorite song"  # Show immediately

# Download a bunch of songs for offline
lyrics -m "song 1"
lyrics -m "song 2"
lyrics -m "song 3"

# Play cached songs later
lyrics -p "song 1"

# Clean up old songs
lyrics -ls                    # See what you have
lyrics -cm "old song"         # Remove specific song
lyrics --clear-music          # Remove all

# Customize your experience
lyrics --settings
# Change to centered mode
# Enable glitch effects
# Switch to mpv player
```

## 🐛 Troubleshooting

**Dependencies not found:**
```bash
pkg install python ffmpeg -y
pip install yt-dlp requests
```

**Command not found:**
```bash
export PATH="$HOME/bin:$PATH"
source ~/.bashrc
```

**No lyrics found:**
- Not all songs have synced lyrics
- Try different search terms
- Check internet connection
- Use `-s -l` to see if plain lyrics are available

**Download fails:**
- Check internet connection
- Try different search query
- Update yt-dlp: `pip install -U yt-dlp`

**Player issues:**
```bash
# Install alternative player
pkg install mpv
lyrics --settings  # Change to mpv
```

## 📜 License

MIT License - See script header for full license text

## 🙏 Credits

- Uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloads
- Lyrics from [LRCLIB](https://lrclib.net/) API
- Media playback via FFmpeg or MPV

## 🌟 Tips

1. **Cache songs ahead of time** with `-m` for offline listening
2. **Use fuzzy search** when clearing - type partial names
3. **Customize display mode** to match your terminal size
4. **Try effects** for a unique visual experience
5. **Check settings menu** for all customization options

---

Made with ❤️ for Termux users who love music and lyrics!
