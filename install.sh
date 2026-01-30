#!/data/data/com.termux/files/usr/bin/bash
# Lyrics Shower Installation Script

echo "🎵 Installing Lyrics Shower..."
echo ""

# Create bin directory if it doesn't exist
mkdir -p ~/bin

# Download the main script from GitHub
echo "📥 Downloading main script from GitHub..."
if command -v curl &> /dev/null; then
    curl -sL "https://raw.githubusercontent.com/sparxmathsalternative/termux-lyrics-shower/refs/heads/main/main.py" -o ~/bin/lyrics
elif command -v wget &> /dev/null; then
    wget -q "https://raw.githubusercontent.com/sparxmathsalternative/termux-lyrics-shower/refs/heads/main/main.py" -O ~/bin/lyrics
else
    echo "❌ Error: Neither curl nor wget found. Installing curl..."
    pkg install curl -y
    curl -sL "https://raw.githubusercontent.com/sparxmathsalternative/termux-lyrics-shower/refs/heads/main/main.py" -o ~/bin/lyrics
fi

# Make executable
chmod +x ~/bin/lyrics

# Add shebang if not present
if ! head -n 1 ~/bin/lyrics | grep -q "^#!"; then
    echo '#!/data/data/com.termux/files/usr/bin/python3' | cat - ~/bin/lyrics > ~/bin/lyrics.tmp
    mv ~/bin/lyrics.tmp ~/bin/lyrics
    chmod +x ~/bin/lyrics
fi

# Add to PATH if not already there
PATH_ADDED=false
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo "🔧 Adding ~/bin to PATH..."
    
    # Add to .bashrc
    if [ -f ~/.bashrc ]; then
        if ! grep -q 'export PATH="$HOME/bin:$PATH"' ~/.bashrc; then
            echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
            PATH_ADDED=true
        fi
    fi
    
    # Add to .zshrc if it exists
    if [ -f ~/.zshrc ]; then
        if ! grep -q 'export PATH="$HOME/bin:$PATH"' ~/.zshrc; then
            echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
        fi
    fi
    
    # Add to current session
    export PATH="$HOME/bin:$PATH"
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pkg update -y
pkg install python ffmpeg curl -y
pip install yt-dlp requests

echo ""
echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  lyrics                                # Interactive mode"
echo "  lyrics <song name>                    # Download and play with lyrics"
echo "  lyrics -l <song>                      # Fetch lyrics only"
echo "  lyrics -s -l <song>                   # Show lyrics"
echo "  lyrics -m <song>                      # Download music only"
echo "  lyrics -p <song>                      # Play music only"
echo "  lyrics -ls                            # List cached files"
echo "  lyrics --settings                     # Open settings menu"
echo "  lyrics --update                       # Update to latest version"
echo "  lyrics --uninstall                    # Uninstall lyrics shower"
echo "  lyrics -h                             # Show help"
echo ""
echo "Examples:"
echo "  lyrics overnight - mirrors demo"
echo "  lyrics -l 'shape of you'"
echo "  lyrics --clear-music 'overnight'"
echo ""
echo "🎉 Ready to use! Type 'lyrics -h' for all options"

if [ "$PATH_ADDED" = true ]; then
    echo ""
    echo "⚠️  Important: Restart your terminal or run:"
    echo "  source ~/.bashrc"
    echo "  (or: source ~/.zshrc if using zsh)"
fi
