# YouTuber - Command Reference Card

## Installation
```bash
# Windows
.\setup.ps1

# Linux/macOS
chmod +x setup.sh && ./setup.sh
source venv/bin/activate
```

## Quick Commands

### Download
```bash
youtuber download [URL]                                    # Best quality
youtuber download [URL] -q 1080p                          # Specific quality
youtuber download [URL] -t                                 # With transcripts
youtuber download [URL] -t -l en -l es                    # Multiple languages
youtuber download [URL] -p                                 # Playlist
youtuber download [URL] -c cookies.txt                    # With auth
youtuber download [URL] -v                                 # Verbose
youtuber download [URL] -d                                 # Debug
youtuber download [URL] -o "D:\Videos"                    # Custom output
```

### Collection
```bash
youtuber list                                              # List all
youtuber list -n 10 -s title -o ASC                       # Sorted list
youtuber search "keyword"                                  # Search all
youtuber search "keyword" -f title                        # Search field
youtuber stats                                             # Statistics
```

### Info & Config
```bash
youtuber info [URL]                                        # Video info
youtuber info [URL] -j                                     # JSON output
youtuber config list                                       # All config
youtuber config set default_quality 1080p                 # Set value
youtuber config get download_dir                           # Get value
youtuber paths                                             # Show paths
```

## Quality Options
- `best` - Best available quality (default)
- `1080p`, `720p`, `480p`, `360p` - Specific resolution
- `audio` - Audio only (MP3 extraction)

## Format Options
- `mp4` - MP4 format (default)
- `mkv` - Matroska format
- `webm` - WebM format

## Common Workflows

### First Time Setup
```bash
youtuber config set download_dir "D:\YouTube"
youtuber config set default_quality 1080p
youtuber config set download_transcripts true
youtuber config set cookies_file "cookies.txt"
```

### Download Educational Playlist
```bash
youtuber download [PLAYLIST_URL] -p -t -q 1080p -o "D:\Education"
```

### Download Audio Podcast
```bash
youtuber download [URL] -q audio -o "D:\Podcasts"
```

### Batch Download (PowerShell)
```powershell
Get-Content urls.txt | ForEach-Object { youtuber download $_ -t -v }
```

### Search and Export
```bash
youtuber search "python" -j > results.json
```

## Help Commands
```bash
youtuber --help                  # General help
youtuber download --help         # Download help
youtuber config --help           # Config help
youtuber --version              # Version info
```

## Troubleshooting
```bash
youtuber download [URL] -v       # Verbose mode
youtuber download [URL] -d       # Debug mode
youtuber paths                   # Check paths
pip install --upgrade yt-dlp     # Update downloader
```

## File Locations

### Windows
- Config: `%APPDATA%\youtuber\config.json`
- Database: `%APPDATA%\youtuber\collection.db`
- Logs: `%APPDATA%\youtuber\logs\`
- Downloads: `%USERPROFILE%\Videos\YouTuber`

### macOS
- Config: `~/Library/Application Support/youtuber/config.json`
- Database: `~/Library/Application Support/youtuber/collection.db`
- Logs: `~/Library/Application Support/youtuber/logs/`
- Downloads: `~/Movies/YouTuber`

### Linux
- Config: `~/.config/youtuber/config.json`
- Database: `~/.config/youtuber/collection.db`
- Logs: `~/.config/youtuber/logs/`
- Downloads: `~/Videos/YouTuber`

## Authentication

### Export Browser Cookies
1. Install browser extension (Chrome: "Get cookies.txt LOCALLY")
2. Navigate to YouTube
3. Export cookies to `cookies.txt`
4. Configure: `youtuber config set cookies_file "path/to/cookies.txt"`

### Username/Password
```bash
youtuber download [URL] -u your@email.com -pw yourpassword
```

## Quick Tips

✅ Use config for repeated settings  
✅ Enable transcripts for accessibility  
✅ Use cookies for better access  
✅ Check stats to monitor disk usage  
✅ Use verbose mode for troubleshooting  
✅ Keep yt-dlp updated regularly  

---

**For full documentation, see README.md**
