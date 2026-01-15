# YouTuber - Quick Start Guide

## 🚀 Installation (5 Minutes)

### Windows

1. **Open PowerShell** in the project directory
2. **Run setup script:**
   ```powershell
   .\setup.ps1
   ```
3. **Done!** The script will:
   - Check Python 3.8+
   - Create virtual environment
   - Install all dependencies
   - Verify installation

### Linux / macOS

1. **Open Terminal** in the project directory
2. **Make script executable:**
   ```bash
   chmod +x setup.sh
   ```
3. **Run setup script:**
   ```bash
   ./setup.sh
   ```
4. **Activate environment:**
   ```bash
   source venv/bin/activate
   ```

## 📥 Download Your First Video

```bash
youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8
```

## 🎯 Common Commands

### Download with Transcripts
```bash
youtuber download [URL] --transcripts
```

### Download Playlist
```bash
youtuber download [PLAYLIST_URL] --playlist
```

### Download Specific Quality
```bash
youtuber download [URL] --quality 1080p
# Options: best, 1080p, 720p, 480p, 360p, audio
```

### View Your Collection
```bash
youtuber list
```

### Search Collection
```bash
youtuber search "python tutorial"
```

### Get Video Info (No Download)
```bash
youtuber info [URL]
```

## ⚙️ Configuration

### View All Settings
```bash
youtuber config list
```

### Change Download Location
```bash
youtuber config set download_dir "D:\YouTube Videos"
```

### Enable Transcripts by Default
```bash
youtuber config set download_transcripts true
```

### Set Default Quality
```bash
youtuber config set default_quality 1080p
```

## 🔐 Authentication (For Age-Restricted Videos)

### Method 1: Cookies (Recommended)

1. Install browser extension to export cookies:
   - **Chrome/Edge:** "Get cookies.txt LOCALLY"
   - **Firefox:** "cookies.txt"

2. Export YouTube cookies to `cookies.txt`

3. Configure:
   ```bash
   youtuber config set cookies_file "path/to/cookies.txt"
   ```

### Method 2: Username/Password

```bash
youtuber download [URL] --username your@email.com --password yourpassword
```

## 📊 Collection Management

### View Statistics
```bash
youtuber stats
```

### View Application Paths
```bash
youtuber paths
```

## 🐛 Troubleshooting

### Enable Verbose Logging
```bash
youtuber download [URL] --verbose
```

### Enable Debug Mode
```bash
youtuber download [URL] --debug
```

### Update yt-dlp
```bash
# Activate virtual environment first
pip install --upgrade yt-dlp
```

## 📚 More Information

- **Full Documentation:** [README.md](README.md)
- **Installation Guide:** [INSTALL.md](INSTALL.md)
- **Usage Examples:** [EXAMPLES.md](EXAMPLES.md)

## 🆘 Getting Help

```bash
# General help
youtuber --help

# Command-specific help
youtuber download --help
youtuber config --help
```

## ✨ Features

- ✅ Download single videos or entire playlists
- ✅ Automatic transcript/subtitle downloading
- ✅ SQLite-based collection management
- ✅ Multiple quality options (best, 1080p, 720p, etc.)
- ✅ Authentication support for restricted videos
- ✅ Cross-platform (Windows, macOS, Linux)
- ✅ Beautiful CLI with progress bars
- ✅ Enhanced debugging and logging
- ✅ Search and filter your collection
- ✅ Audio-only extraction
- ✅ Multiple format support (MP4, MKV, WebM)

## 🎓 Example: Download Educational Playlist

```bash
youtuber download "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID" \
  --playlist \
  --quality 1080p \
  --transcripts \
  --output-dir "D:\Education\Python Course" \
  --verbose
```

## 💡 Pro Tips

1. **Use configuration** for repeated settings
2. **Enable transcripts** for better accessibility
3. **Export browser cookies** for better access
4. **Use verbose mode** when troubleshooting
5. **Check stats regularly** to monitor disk usage

---

**Ready to build your YouTube collection? Start downloading now!** 🎉
