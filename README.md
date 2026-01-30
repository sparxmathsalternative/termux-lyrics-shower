# 🎵 Termux Lyrics Shower

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
- 🖥️ **Interactive mode** for easier use
- 🔄 **Auto-update** checking and installation
- 🔔 **Version warnings** for outdated or dev versions

## 📥 Installation

```bash
pkg update
pkg install git python3
git clone https://github.com/sparxmathsalternative/termux-lyrics-shower.git
cd termux-lyrics-shower
chmod +x install.sh
bash install.sh
```

After installation, restart your terminal or run:
```bash
source ~/.bashrc
```

## 🚀 Usage

### Interactive Mode

Just type `lyrics` with no arguments to enter interactive mode:

```bash
lyrics
```

In interactive mode:
```
lyrics> set overnight - mirrors demo    # Set session song
lyrics> play                             # Play the session song
lyrics> lyrics                           # Get lyrics for session song
lyrics> download shape of you            # Download a different song
lyrics> list                             # List cached files
lyrics> settings                         # Open settings
lyrics> help                             # Show help
lyrics> exit                             # Exit
```

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
# - Check for updates
```

### Update & Maintenance

```bash
# Check version
lyrics -v
lyrics --version

# Update to latest version
lyrics --update

# Uninstall (keeps cached data)
lyrics --uninstall
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

## 🔔 Version Warnings

The app automatically checks for updates and shows warnings:

**Outdated Version:**
```
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  WARNING: OUTDATED VERSION                               ║
╟──────────────────────────────────────────────────────────────╢
║  Current Version: 1.0.0-alpha   (from 2026-01-30)            ║
║  Latest Version:  1.0.1-alpha   (from 2026-02-01)            ║
║                                                              ║
║  Please update using: lyrics --update                        ║
╚══════════════════════════════════════════════════════════════╝
```

**Developer/Unreleased Version:**
```
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  WARNING: UNRELEASED/DEVELOPER VERSION                   ║
╟──────────────────────────────────────────────────────────────╢
║  You are using version 1.1.0-dev which is ahead of           ║
║  the official release (1.0.0-alpha).                         ║
║                                                              ║
║  This version may contain severe bugs and untested features. ║
║  The developers are not responsible for any outcomes.        ║
╚══════════════════════════════════════════════════════════════╝
```

To disable version checking: `lyrics --settings` → Option 8

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
├── bin/
│   └── lyrics              # Main executable
├── Music/                  # Downloaded music files
│   └── *.mp3
├── .lyrics_cache/          # Cached lyrics
│   └── *.lrc
└── .config/
    └── lyrics-shower/
        └── config.json     # Configuration file
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
  "auto_install": true,
  "check_updates": true
}
```

## 📋 All Commands Reference

| Command | Aliases | Description |
|---------|---------|-------------|
| `lyrics` | - | Interactive mode |
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
| `--update` | - | Update to latest version |
| `--uninstall` | - | Uninstall lyrics shower |
| `-v, --version` | - | Show version info |
| `-h, --help` | - | Show help |

## 🎯 Examples

```bash
# Enter interactive mode
lyrics

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

# Keep up to date
lyrics --version              # Check current version
lyrics --update               # Update to latest
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

**Update issues:**
```bash
# Manually update
cd ~/termux-lyrics-shower
git pull
bash install.sh
```

**Version warnings won't go away:**
- Make sure you're updated: `lyrics --update`
- Disable version checking: `lyrics --settings` → Option 8

## 📜 License

MIT License - See main.py header for full license text

## 🙏 Credits

- Uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloads
- Lyrics from [LRCLIB](https://lrclib.net/) API
- Media playback via FFmpeg or MPV

## 🌟 Tips

1. **Use interactive mode** for easier navigation - just type `lyrics`
2. **Cache songs ahead of time** with `-m` for offline listening
3. **Use fuzzy search** when clearing - type partial names
4. **Customize display mode** to match your terminal size
5. **Try effects** for a unique visual experience
6. **Keep updated** - run `lyrics --update` regularly
7. **Check settings menu** for all customization options

## 🔄 Updating

The app checks for updates automatically. When a new version is available, you'll see a warning. Update with:

```bash
lyrics --update
```

This will:
- Backup your current version
- Download the latest version from GitHub
- Install it automatically
- Keep all your settings and cached data

## 🗑️ Uninstalling

To uninstall (keeps your music and lyrics):

```bash
lyrics --uninstall
```

To completely remove everything:

```bash
lyrics --uninstall
rm -rf ~/Music
rm -rf ~/.lyrics_cache
rm -rf ~/.config/lyrics-shower
```

---

Made with ❤️ for Termux users who love music and lyrics!

**Repository:** [github.com/sparxmathsalternative/termux-lyrics-shower](https://github.com/sparxmathsalternative/termux-lyrics-shower)
