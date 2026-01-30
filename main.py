#!/data/data/com.termux/files/usr/bin/python3
"""
Termux Lyrics Shower - Real-time synced lyrics display with music playback
Version: 1.0.0-alpha
License: MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys
import time
import json
import subprocess
import argparse
import re
import random
import shutil
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from datetime import datetime

# VERSION INFORMATION
CURRENT_VERSION = {
    "version": "1.0.0-alpha",
    "major": 1,
    "minor": 0,
    "patch": 0,
    "status": "alpha",
    "build": 1,
    "last_updated": "2026-01-30"
}

VERSION_CHECK_URL = "https://raw.githubusercontent.com/sparxmathsalternative/termux-lyrics-shower/refs/heads/main/version.json"

# ============= CONFIGURATION =============
CONFIG_DIR = Path.home() / ".config" / "lyrics-shower"
MUSIC_DIR = Path.home() / "Music"
LYRICS_DIR = Path.home() / ".lyrics_cache"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Create directories
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
MUSIC_DIR.mkdir(exist_ok=True)
LYRICS_DIR.mkdir(exist_ok=True)

# Default configuration
DEFAULT_CONFIG = {
    "platform": "youtube",
    "media_player": "ffplay",
    "display_mode": "scrolling",  # scrolling, centered, list
    "use_graph": False,
    "effects": {
        "glitch": False,
        "flash": False,
        "bass_threshold": 0.7,
        "high_threshold": 0.8
    },
    "auto_install": True,
    "check_updates": True
}

# ============= VERSION CHECKING =============

def compare_versions(v1: dict, v2: dict) -> int:
    """Compare two version dicts. Returns: 1 if v1 > v2, -1 if v1 < v2, 0 if equal"""
    if v1["major"] != v2["major"]:
        return 1 if v1["major"] > v2["major"] else -1
    if v1["minor"] != v2["minor"]:
        return 1 if v1["minor"] > v2["minor"] else -1
    if v1["patch"] != v2["patch"]:
        return 1 if v1["patch"] > v2["patch"] else -1
    if v1.get("build", 0) != v2.get("build", 0):
        return 1 if v1.get("build", 0) > v2.get("build", 0) else -1
    return 0

def check_version() -> Optional[str]:
    """Check version and return warning message if needed"""
    config = load_config()
    if not config.get("check_updates", True):
        return None
    
    try:
        import requests
        response = requests.get(VERSION_CHECK_URL, timeout=5)
        if response.status_code == 200:
            remote_version = response.json()
            
            comparison = compare_versions(CURRENT_VERSION, remote_version)
            
            if comparison < 0:
                # Current version is older
                warning = f"""
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  WARNING: OUTDATED VERSION                               ║
╟──────────────────────────────────────────────────────────────╢
║  Current Version: {CURRENT_VERSION['version']:<15} (from {CURRENT_VERSION['last_updated']})  ║
║  Latest Version:  {remote_version['version']:<15} (from {remote_version['last_updated']})  ║
║                                                              ║
║  Please update using: lyrics --update                        ║
╚══════════════════════════════════════════════════════════════╝
"""
                return warning
            elif comparison > 0:
                # Current version is newer (unreleased/dev)
                warning = f"""
╔══════════════════════════════════════════════════════════════╗
║  ⚠️  WARNING: UNRELEASED/DEVELOPER VERSION                   ║
╟──────────────────────────────────────────────────────────────╢
║  You are using version {CURRENT_VERSION['version']} which is ahead of        ║
║  the official release ({remote_version['version']}).                          ║
║                                                              ║
║  This version may contain severe bugs and untested features. ║
║  The developers are not responsible for any outcomes.        ║
╚══════════════════════════════════════════════════════════════╝
"""
                return warning
    except:
        pass  # Silently fail if can't check version
    
    return None

VERSION_WARNING = None

# ============= UTILITY FUNCTIONS =============

def load_config() -> dict:
    """Load configuration from file"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG.copy()

def save_config(config: dict):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def clear_screen():
    """Clear terminal screen"""
    os.system('clear')

def install_dependency(package: str, pip: bool = False):
    """Install a dependency"""
    try:
        if pip:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
        else:
            subprocess.run(["pkg", "install", package, "-y"], 
                         check=True, capture_output=True)
        return True
    except:
        return False

def check_dependencies():
    """Check and install required dependencies"""
    config = load_config()
    
    # Check for yt-dlp
    if shutil.which("yt-dlp") is None:
        print("📦 Installing yt-dlp...")
        if config["auto_install"]:
            install_dependency("yt-dlp", pip=True)
    
    # Check for ffplay/mpv
    player = config["media_player"]
    if shutil.which(player) is None:
        print(f"📦 Installing {player}...")
        if config["auto_install"]:
            install_dependency("ffmpeg" if player == "ffplay" else player)
    
    # Check for requests
    try:
        import requests
    except ImportError:
        print("📦 Installing requests...")
        install_dependency("requests", pip=True)

def fuzzy_search(query: str, items: List[str], threshold: float = 0.6) -> List[Tuple[str, float]]:
    """Simple fuzzy search implementation"""
    query = query.lower()
    results = []
    
    for item in items:
        item_lower = item.lower()
        
        # Exact match
        if query == item_lower:
            results.append((item, 1.0))
            continue
        
        # Substring match
        if query in item_lower:
            score = len(query) / len(item_lower)
            results.append((item, score))
            continue
        
        # Word match
        query_words = set(query.split())
        item_words = set(item_lower.split())
        if query_words & item_words:
            score = len(query_words & item_words) / len(query_words | item_words)
            if score >= threshold:
                results.append((item, score))
    
    return sorted(results, key=lambda x: x[1], reverse=True)

# ============= LYRICS FUNCTIONS =============

def fetch_lyrics_from_url(url: str) -> Optional[str]:
    """Fetch lyrics from custom URL"""
    try:
        import requests
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
    except:
        pass
    return None

def fetch_lyrics(song_title: str, artist: str = "", custom_url: str = None) -> Optional[str]:
    """Fetch synced lyrics from various sources"""
    if custom_url:
        print(f"📝 Fetching lyrics from custom URL...")
        lyrics = fetch_lyrics_from_url(custom_url)
        if lyrics:
            return lyrics
    
    print(f"📝 Fetching lyrics for: {song_title}")
    
    try:
        import requests
        
        # Try LRCLIB API
        search_query = f"{artist} {song_title}".strip()
        response = requests.get(
            "https://lrclib.net/api/search",
            params={"q": search_query},
            timeout=10
        )
        
        if response.status_code == 200:
            results = response.json()
            if results:
                track = results[0]
                if track.get('syncedLyrics'):
                    return track['syncedLyrics']
                elif track.get('plainLyrics'):
                    # Convert plain lyrics to simple format
                    lines = track['plainLyrics'].split('\n')
                    return '\n'.join([f"[00:00.00] {line}" for line in lines if line.strip()])
    except Exception as e:
        print(f"⚠️  Failed to fetch lyrics: {e}")
    
    return None

def parse_lrc(lrc_content: str) -> List[Tuple[float, str]]:
    """Parse LRC format lyrics"""
    lyrics = []
    for line in lrc_content.split('\n'):
        line = line.strip()
        if line.startswith('[') and ']' in line:
            try:
                time_str = line[1:line.index(']')]
                text = line[line.index(']')+1:].strip()
                
                # Skip metadata
                if not text or time_str[0].isalpha():
                    continue
                
                # Parse time [mm:ss.xx]
                if ':' in time_str:
                    parts = time_str.split(':')
                    minutes = float(parts[0])
                    seconds = float(parts[1])
                    timestamp = minutes * 60 + seconds
                    lyrics.append((timestamp, text))
            except:
                continue
    
    return sorted(lyrics, key=lambda x: x[0])

def save_lyrics(song_title: str, lyrics: str):
    """Save lyrics to cache"""
    lyrics_file = LYRICS_DIR / f"{song_title}.lrc"
    with open(lyrics_file, 'w', encoding='utf-8') as f:
        f.write(lyrics)
    print(f"💾 Lyrics saved to: {lyrics_file}")

def load_cached_lyrics(song_title: str) -> Optional[str]:
    """Load lyrics from cache"""
    lyrics_file = LYRICS_DIR / f"{song_title}.lrc"
    if lyrics_file.exists():
        with open(lyrics_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

# ============= MUSIC FUNCTIONS =============

def download_music(query: str, custom_url: str = None) -> Optional[str]:
    """Download music using yt-dlp"""
    print(f"🔍 Searching for: {query}")
    
    output_template = str(MUSIC_DIR / "%(title)s.%(ext)s")
    
    if custom_url:
        url = custom_url
    else:
        config = load_config()
        platform = config["platform"]
        
        # Map platform to search format
        if platform == "youtube":
            url = f"ytsearch1:{query}"
        elif platform == "soundcloud":
            url = f"scsearch1:{query}"
        elif platform == "spotify":
            url = f"spsearch1:{query}"
        else:
            url = f"ytsearch1:{query}"  # Default to YouTube
    
    # Base command
    base_cmd = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",
        "-o", output_template,
        "--extractor-args", "youtube:player_client=web_creator,android_creator",
        "--print", "after_move:filepath"
    ]
    
    # Try with cookies from common browsers
    browsers = ["firefox", "chrome", "chromium"]
    
    for browser in browsers:
        try:
            cmd = base_cmd.copy()
            cmd.insert(-1, "--cookies-from-browser")
            cmd.insert(-1, browser)
            cmd.append(url)
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            filepath = result.stdout.strip().split('\n')[-1]
            print(f"✅ Downloaded: {filepath}")
            return filepath
        except:
            continue
    
    # If cookies don't work, try without
    try:
        cmd = base_cmd + [url]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        filepath = result.stdout.strip().split('\n')[-1]
        print(f"✅ Downloaded: {filepath}")
        return filepath
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download: {e}")
        print("\n💡 YouTube requires authentication. Try:")
        print("   1. Install a browser: pkg install firefox")
        print("   2. Login to YouTube in the browser")
        print("   3. Try again - cookies will be used automatically")
        return None

# ============= DISPLAY FUNCTIONS =============

def apply_glitch_effect(text: str) -> str:
    """Apply unicode glitch effect to text"""
    glitch_chars = ['̴', '̵', '̶', '̷', '̸', '̡', '̢', '̧', '̨', '̛', '̖', '̗', '̘', '̙', '̜', '̝', '̞', '̟']
    result = []
    for char in text:
        if random.random() < 0.3:
            result.append(char + random.choice(glitch_chars))
        else:
            result.append(char)
    return ''.join(result)

def display_scrolling(lyrics: List[Tuple[float, str]], elapsed: float, current_line: int, config: dict):
    """Display scrolling lyrics"""
    clear_screen()
    print("=" * 60)
    print(f"🎵 NOW PLAYING")
    print("=" * 60)
    print("\n")
    
    # Show context lines
    for i in range(max(0, current_line - 1), min(len(lyrics), current_line + 4)):
        timestamp, text = lyrics[i]
        
        if config["effects"]["glitch"] and i == current_line:
            text = apply_glitch_effect(text)
        
        if i == current_line:
            if config["effects"]["flash"]:
                print(f"\n  \033[1;97m► {text}\033[0m\n")  # White/bright
            else:
                print(f"\n  \033[1;96m► {text}\033[0m\n")  # Cyan
        else:
            print(f"    \033[90m{text}\033[0m")  # Gray
    
    print("\n" * 5)
    print(f"⏱️  {int(elapsed//60):02d}:{int(elapsed%60):02d}")
    print("\n[Ctrl+C to stop]")

def display_centered(lyrics: List[Tuple[float, str]], elapsed: float, current_line: int, config: dict):
    """Display only current line centered"""
    clear_screen()
    
    # Center vertically
    for _ in range(10):
        print()
    
    if current_line < len(lyrics):
        _, text = lyrics[current_line]
        
        if config["effects"]["glitch"]:
            text = apply_glitch_effect(text)
        
        # Center horizontally
        term_width = shutil.get_terminal_size().columns
        padding = (term_width - len(text)) // 2
        
        if config["effects"]["flash"]:
            print(" " * padding + f"\033[1;97m{text}\033[0m")
        else:
            print(" " * padding + f"\033[1;96m{text}\033[0m")
    
    # More vertical spacing
    for _ in range(10):
        print()
    
    print(f"\n⏱️  {int(elapsed//60):02d}:{int(elapsed%60):02d}")

def display_list(lyrics: List[Tuple[float, str]], elapsed: float, current_line: int, config: dict):
    """Display all lyrics as a list"""
    clear_screen()
    print("=" * 60)
    print(f"🎵 LYRICS")
    print("=" * 60)
    print()
    
    for i, (timestamp, text) in enumerate(lyrics):
        if i == current_line:
            print(f"  \033[1;96m► {text}\033[0m")
        else:
            print(f"    {text}")
    
    print(f"\n⏱️  {int(elapsed//60):02d}:{int(elapsed%60):02d}")

def showcase_lyrics(lyrics_content: str):
    """Display lyrics without playing music"""
    clear_screen()
    print("=" * 60)
    print("📜 LYRICS")
    print("=" * 60)
    print()
    
    lyrics = parse_lrc(lyrics_content)
    if lyrics:
        for _, text in lyrics:
            print(f"  {text}")
    else:
        # Show raw content if not parseable
        print(lyrics_content)
    
    print()
    print("=" * 60)

# ============= PLAYBACK FUNCTIONS =============

def play_with_lyrics(audio_file: str, lyrics: List[Tuple[float, str]], config: dict):
    """Play audio with synced lyrics"""
    player = config["media_player"]
    display_mode = config["display_mode"]
    
    # Start audio playback
    if player == "ffplay":
        player_cmd = ["ffplay", "-nodisp", "-autoexit", audio_file]
    elif player == "mpv":
        player_cmd = ["mpv", "--no-video", audio_file]
    else:
        player_cmd = [player, audio_file]
    
    player_process = subprocess.Popen(
        player_cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    start_time = time.time()
    current_line = 0
    
    try:
        while player_process.poll() is None:
            elapsed = time.time() - start_time
            
            # Find current lyric line
            while (current_line < len(lyrics) - 1 and 
                   elapsed >= lyrics[current_line + 1][0]):
                current_line += 1
            
            # Display based on mode
            if display_mode == "scrolling":
                display_scrolling(lyrics, elapsed, current_line, config)
            elif display_mode == "centered":
                display_centered(lyrics, elapsed, current_line, config)
            elif display_mode == "list":
                display_list(lyrics, elapsed, current_line, config)
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped")
        player_process.kill()

def play_music_only(audio_file: str, config: dict):
    """Play audio without lyrics"""
    player = config["media_player"]
    
    print(f"🎵 Playing: {Path(audio_file).stem}")
    print("[Ctrl+C to stop]")
    
    if player == "ffplay":
        cmd = ["ffplay", "-nodisp", "-autoexit", audio_file]
    elif player == "mpv":
        cmd = ["mpv", "--no-video", audio_file]
    else:
        cmd = [player, audio_file]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n⏹️  Stopped")

# ============= MANAGEMENT FUNCTIONS =============

def list_cached():
    """List cached music and lyrics"""
    print("\n📁 CACHED MUSIC:")
    print("=" * 60)
    music_files = list(MUSIC_DIR.glob("*.mp3"))
    if music_files:
        for i, file in enumerate(music_files, 1):
            size = file.stat().st_size / (1024 * 1024)
            print(f"  {i}. {file.stem} ({size:.2f} MB)")
    else:
        print("  No cached music found")
    
    print("\n📝 CACHED LYRICS:")
    print("=" * 60)
    lyrics_files = list(LYRICS_DIR.glob("*.lrc"))
    if lyrics_files:
        for i, file in enumerate(lyrics_files, 1):
            print(f"  {i}. {file.stem}")
    else:
        print("  No cached lyrics found")
    print()

def clear_cache(cache_type: str, query: str = None):
    """Clear cached music or lyrics"""
    if cache_type == "music":
        cache_dir = MUSIC_DIR
        ext = "*.mp3"
        name = "music"
    else:
        cache_dir = LYRICS_DIR
        ext = "*.lrc"
        name = "lyrics"
    
    files = list(cache_dir.glob(ext))
    
    if not files:
        print(f"No cached {name} found")
        return
    
    if query:
        # Fuzzy search
        file_names = [f.stem for f in files]
        matches = fuzzy_search(query, file_names)
        
        if not matches:
            print(f"No matches found for '{query}'")
            return
        
        print(f"\n🔍 Found matches for '{query}':")
        for i, (name, score) in enumerate(matches[:5], 1):
            print(f"  {i}. {name} (match: {score:.0%})")
        
        choice = input("\nSelect number to delete (or 'q' to cancel): ").strip()
        if choice.lower() == 'q':
            print("Cancelled")
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(matches):
                file_to_delete = cache_dir / f"{matches[idx][0]}.{ext.replace('*.', '')}"
                confirm = input(f"Delete '{matches[idx][0]}'? (y/N): ").strip().lower()
                if confirm == 'y':
                    file_to_delete.unlink()
                    print(f"✅ Deleted: {matches[idx][0]}")
                else:
                    print("Cancelled")
        except (ValueError, IndexError):
            print("Invalid selection")
    else:
        # Clear all
        confirm = input(f"Delete ALL cached {name}? (y/N): ").strip().lower()
        if confirm == 'y':
            for file in files:
                file.unlink()
            print(f"✅ Deleted {len(files)} {name} file(s)")
        else:
            print("Cancelled")

def settings_menu():
    """Interactive settings menu"""
    config = load_config()
    
    while True:
        clear_screen()
        print("=" * 60)
        print("⚙️  SETTINGS MENU")
        print("=" * 60)
        print()
        print(f"1. Platform: {config['platform']}")
        print(f"2. Media Player: {config['media_player']}")
        print(f"3. Display Mode: {config['display_mode']}")
        print(f"4. Use Graph: {config['use_graph']}")
        print(f"5. Glitch Effect: {config['effects']['glitch']}")
        print(f"6. Flash Effect: {config['effects']['flash']}")
        print(f"7. Auto Install Dependencies: {config['auto_install']}")
        print(f"8. Check for Updates: {config.get('check_updates', True)}")
        print()
        print("0. Save and Exit")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == '0':
            save_config(config)
            print("✅ Settings saved!")
            break
        elif choice == '1':
            print("\nPlatform options: youtube, soundcloud, spotify")
            platform = input("Enter platform: ").strip()
            if platform:
                config['platform'] = platform
        elif choice == '2':
            print("\nMedia player options: ffplay, mpv")
            player = input("Enter player: ").strip()
            if player:
                config['media_player'] = player
                if shutil.which(player) is None:
                    install = input(f"{player} not found. Install? (y/N): ").strip().lower()
                    if install == 'y':
                        install_dependency("ffmpeg" if player == "ffplay" else player)
        elif choice == '3':
            print("\nDisplay modes: scrolling, centered, list")
            mode = input("Enter mode: ").strip()
            if mode in ['scrolling', 'centered', 'list']:
                config['display_mode'] = mode
        elif choice == '4':
            config['use_graph'] = not config['use_graph']
        elif choice == '5':
            config['effects']['glitch'] = not config['effects']['glitch']
        elif choice == '6':
            config['effects']['flash'] = not config['effects']['flash']
        elif choice == '7':
            config['auto_install'] = not config['auto_install']
        elif choice == '8':
            config['check_updates'] = not config.get('check_updates', True)

def uninstall():
    """Uninstall lyrics shower"""
    clear_screen()
    print("=" * 60)
    print("🗑️  UNINSTALL LYRICS SHOWER")
    print("=" * 60)
    print()
    print("This will:")
    print("  - Remove the lyrics command from ~/bin")
    print("  - Keep your cached music and lyrics")
    print("  - Keep your configuration")
    print()
    confirm = input("Are you sure you want to uninstall? (yes/N): ").strip().lower()
    
    if confirm == 'yes':
        script_path = Path.home() / "bin" / "lyrics"
        if script_path.exists():
            script_path.unlink()
            print("✅ Uninstalled successfully!")
            print()
            print("To reinstall, run the install script again.")
            print()
            print("To remove cached data:")
            print(f"  rm -rf {MUSIC_DIR}")
            print(f"  rm -rf {LYRICS_DIR}")
            print(f"  rm -rf {CONFIG_DIR}")
        else:
            print("❌ lyrics command not found in ~/bin")
    else:
        print("Cancelled")

def update_lyrics_shower():
    """Update to latest version"""
    print("🔄 Updating Lyrics Shower...")
    print()
    
    # Download update script
    update_script = Path.home() / ".lyrics_update.sh"
    
    try:
        import requests
        response = requests.get("https://raw.githubusercontent.com/sparxmathsalternative/termux-lyrics-shower/refs/heads/main/update.sh", timeout=10)
        if response.status_code == 200:
            with open(update_script, 'w') as f:
                f.write(response.text)
            update_script.chmod(0o755)
            
            # Run update script
            subprocess.run(["bash", str(update_script)])
            update_script.unlink()
        else:
            print("❌ Failed to download update script")
    except Exception as e:
        print(f"❌ Update failed: {e}")

# ============= INTERACTIVE MODE =============

def interactive_mode():
    """Interactive command-line mode"""
    clear_screen()
    print("=" * 60)
    print("🎵 LYRICS SHOWER - INTERACTIVE MODE")
    print("=" * 60)
    print()
    print("Type 'help' for commands, 'exit' to quit")
    print()
    
    session_song = None
    
    while True:
        try:
            if session_song:
                prompt = f"lyrics [{session_song}]> "
            else:
                prompt = "lyrics> "
            
            cmd = input(prompt).strip()
            
            if not cmd:
                continue
            
            if cmd.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            if cmd.lower() == 'help':
                print("\nAvailable commands:")
                print("  play [song]     - Download and play with lyrics")
                print("  lyrics [song]   - Fetch lyrics only")
                print("  download [song] - Download music only")
                print("  list            - List cached files")
                print("  clear           - Clear cache")
                print("  settings        - Open settings menu")
                print("  set <song>      - Set session song")
                print("  help            - Show this help")
                print("  exit            - Exit interactive mode")
                print()
                continue
            
            parts = cmd.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else session_song
            
            if command == 'set':
                if args:
                    session_song = args
                    print(f"✅ Session song set to: {session_song}")
                else:
                    print("Usage: set <song name>")
            elif command in ['play', 'p']:
                if args:
                    print(f"\nPlaying: {args}\n")
                    # Execute play logic (simplified for interactive)
                    os.system(f'python3 ~/bin/lyrics {args}')
                else:
                    print("Please specify a song or set session song with 'set <song>'")
            elif command in ['lyrics', 'l']:
                if args:
                    os.system(f'python3 ~/bin/lyrics -l "{args}"')
                else:
                    print("Please specify a song")
            elif command in ['download', 'd']:
                if args:
                    os.system(f'python3 ~/bin/lyrics -m "{args}"')
                else:
                    print("Please specify a song")
            elif command == 'list':
                list_cached()
            elif command == 'clear':
                print("\n1. Clear music")
                print("2. Clear lyrics")
                choice = input("Select: ").strip()
                if choice == '1':
                    clear_cache('music')
                elif choice == '2':
                    clear_cache('lyrics')
            elif command == 'settings':
                settings_menu()
            else:
                # Assume it's a song name
                session_song = cmd
                print(f"✅ Session song set to: {session_song}")
                print("Use 'play' to play this song")
        
        except KeyboardInterrupt:
            print("\n\nUse 'exit' to quit")
        except EOFError:
            print("\nGoodbye!")
            break

# ============= MAIN FUNCTION =============

def main():
    global VERSION_WARNING
    
    # Check version
    VERSION_WARNING = check_version()
    
    # Show version warning at start
    if VERSION_WARNING:
        print(VERSION_WARNING)
    
    parser = argparse.ArgumentParser(
        description='Termux Lyrics Shower - Real-time synced lyrics with music playback',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lyrics                              # Enter interactive mode
  lyrics overnight - mirrors demo     # Download and play
  lyrics -l "shape of you"            # Fetch lyrics only
  lyrics -s -l "bohemian rhapsody"    # Show lyrics
  lyrics -m "never gonna give you up" # Download music only
  lyrics --clear-music "shape"        # Clear cached music
  lyrics --settings                   # Settings menu
  lyrics --update                     # Update to latest version
  lyrics --uninstall                  # Uninstall
        """
    )
    
    parser.add_argument('query', nargs='*', help='Song search query')
    parser.add_argument('-l', '--lyrics', action='store_true', help='Fetch lyrics only without playing')
    parser.add_argument('-s', '--showcase', action='store_true', help='Show lyrics (use with -l)')
    parser.add_argument('-p', '--play', action='store_true', help='Play music only (no lyrics)')
    parser.add_argument('-m', '--music', action='store_true', help='Download music only and cache it')
    parser.add_argument('-ls', '--list', action='store_true', help='List cached music and lyrics')
    parser.add_argument('-cm', '--clear-music', nargs='?', const='', help='Delete cached music')
    parser.add_argument('-cl', '--clear-lyrics', nargs='?', const='', help='Delete cached lyrics')
    parser.add_argument('--settings', '--menu', action='store_true', help='Open settings menu')
    parser.add_argument('-e', '--effects', action='store_true', help='Toggle effects')
    parser.add_argument('-ext', '--external-url', help='Custom URL for music/lyrics')
    parser.add_argument('--music-url', help='Custom URL for music download')
    parser.add_argument('--lyrics-url', help='Custom URL for lyrics fetch')
    parser.add_argument('--update', action='store_true', help='Update to latest version')
    parser.add_argument('--uninstall', action='store_true', help='Uninstall lyrics shower')
    parser.add_argument('-v', '--version', action='store_true', help='Show version information')
    
    args = parser.parse_args()
    
    # Handle version
    if args.version:
        print(f"Lyrics Shower v{CURRENT_VERSION['version']}")
        print(f"Build: {CURRENT_VERSION['build']}")
        print(f"Status: {CURRENT_VERSION['status']}")
        print(f"Last Updated: {CURRENT_VERSION['last_updated']}")
        return
    
    # Handle update
    if args.update:
        update_lyrics_shower()
        return
    
    # Handle uninstall
    if args.uninstall:
        uninstall()
        return
    
    # Check dependencies
    check_dependencies()
    
    # Load config
    config = load_config()
    
    # Handle settings
    if args.settings:
        settings_menu()
        if VERSION_WARNING:
            print("\n" + VERSION_WARNING)
        return
    
    # Handle list
    if args.list:
        list_cached()
        if VERSION_WARNING:
            print("\n" + VERSION_WARNING)
        return
    
    # Handle clear cache
    if args.clear_music is not None:
        clear_cache('music', args.clear_music if args.clear_music else None)
        if VERSION_WARNING:
            print("\n" + VERSION_WARNING)
        return
    
    if args.clear_lyrics is not None:
        clear_cache('lyrics', args.clear_lyrics if args.clear_lyrics else None)
        if VERSION_WARNING:
            print("\n" + VERSION_WARNING)
        return
    
    # If no query and no special commands, enter interactive mode
    if not args.query:
        interactive_mode()
        return
    
    # Normal operation with query
    query = ' '.join(args.query)
    song_title = query.replace('/', '-').replace('\\', '-')
    
    # Handle external URLs
    music_url = args.music_url or args.external_url
    lyrics_url = args.lyrics_url or (args.external_url and f"{args.external_url.rsplit('.', 1)[0]}.lrc")
    
    # Lyrics only mode
    if args.lyrics:
        lyrics_content = load_cached_lyrics(song_title)
        if not lyrics_content:
            lyrics_content = fetch_lyrics(query, custom_url=lyrics_url)
            if lyrics_content:
                save_lyrics(song_title, lyrics_content)
        
        if lyrics_content:
            if args.showcase:
                showcase_lyrics(lyrics_content)
            else:
                print("✅ Lyrics fetched and cached")
        else:
            print("❌ No lyrics found")
        
        if VERSION_WARNING:
            print("\n" + VERSION_WARNING)
        return
    
    # Music only mode
    if args.music:
        audio_file = download_music(query, custom_url=music_url)
        if audio_file:
            print("✅ Music downloaded and cached")
        if VERSION_WARNING:
            print("\n" + VERSION_WARNING)
        return
    
    # Play only mode
    if args.play:
        # Check for cached music first
        cached_files = list(MUSIC_DIR.glob(f"*{song_title}*.mp3"))
        if not cached_files:
            cached_files = list(MUSIC_DIR.glob("*.mp3"))
            matches = fuzzy_search(song_title, [f.stem for f in cached_files])
            if matches:
                audio_file = MUSIC_DIR / f"{matches[0][0]}.mp3"
            else:
                audio_file = download_music(query, custom_url=music_url)
        else:
            audio_file = cached_files[0]
        
        if audio_file:
            play_music_only(str(audio_file), config)
        
        if VERSION_WARNING:
            print("\n" + VERSION_WARNING)
        return
    
    # Full mode: download music + fetch lyrics + play
    audio_file = download_music(query, custom_url=music_url)
    if not audio_file:
        if VERSION_WARNING:
            print("\n" + VERSION_WARNING)
        return
    
    lyrics_content = fetch_lyrics(song_title, custom_url=lyrics_url)
    if lyrics_content:
        save_lyrics(song_title, lyrics_content)
        lyrics = parse_lrc(lyrics_content)
        if lyrics:
            play_with_lyrics(audio_file, lyrics, config)
        else:
            print("⚠️  No synced lyrics available, playing music only")
            play_music_only(audio_file, config)
    else:
        print("⚠️  No lyrics found, playing music only")
        play_music_only(audio_file, config)
    
    # Show version warning at end
    if VERSION_WARNING:
        print("\n" + VERSION_WARNING)

if __name__ == "__main__":
    main()
