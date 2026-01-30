#!/data/data/com.termux/files/usr/bin/bash
# Lyrics Shower Update Script

echo "🔄 Updating Lyrics Shower..."
echo ""

# Backup current version
if [ -f ~/bin/lyrics ]; then
    echo "📦 Backing up current version..."
    cp ~/bin/lyrics ~/bin/lyrics.backup
fi

# Download the latest version from GitHub
echo "📥 Downloading latest version..."
if command -v curl &> /dev/null; then
    curl -sL "https://raw.githubusercontent.com/sparxmathsalternative/termux-lyrics-shower/refs/heads/main/main.py" -o ~/bin/lyrics.new
elif command -v wget &> /dev/null; then
    wget -q "https://raw.githubusercontent.com/sparxmathsalternative/termux-lyrics-shower/refs/heads/main/main.py" -O ~/bin/lyrics.new
else
    echo "❌ Error: Neither curl nor wget found."
    exit 1
fi

# Check if download was successful
if [ ! -f ~/bin/lyrics.new ]; then
    echo "❌ Download failed!"
    exit 1
fi

# Replace old version with new version
echo "🔧 Installing new version..."
rm -f ~/bin/lyrics
mv ~/bin/lyrics.new ~/bin/lyrics
chmod +x ~/bin/lyrics

# Add shebang if not present
if ! head -n 1 ~/bin/lyrics | grep -q "^#!"; then
    echo '#!/data/data/com.termux/files/usr/bin/python3' | cat - ~/bin/lyrics > ~/bin/lyrics.tmp
    mv ~/bin/lyrics.tmp ~/bin/lyrics
    chmod +x ~/bin/lyrics
fi

echo ""
echo "✅ Update complete!"
echo ""
echo "Backup saved at: ~/bin/lyrics.backup"
echo ""
echo "Run 'lyrics' to start using the updated version!"

