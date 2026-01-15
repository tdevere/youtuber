# Installation and Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- ffmpeg (optional, for format conversion and embedding)

### Installing FFmpeg

#### Windows
```powershell
# Using winget
winget install FFmpeg

# Or download from https://ffmpeg.org/download.html
```

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/youtuber.git
cd youtuber
```

### 2. Create Virtual Environment

#### Windows (PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install YouTuber Package

```bash
# Development mode (recommended for testing)
pip install -e .

# Or production install
pip install .
```

### 5. Verify Installation

```bash
youtuber --version
```

## Quick Start

### Download Your First Video

```bash
youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8
```

### Download with Transcripts

```bash
youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8 --transcripts
```

### Download Specific Quality

```bash
youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8 --quality 1080p
```

### Download Playlist

```bash
youtuber download "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist
```

### View Your Collection

```bash
youtuber list
```

### Search Your Collection

```bash
youtuber search "python tutorial"
```

## Configuration

### View Configuration Paths

```bash
youtuber paths
```

### Set Default Download Directory

```bash
youtuber config set download_dir "C:\Users\YourName\Videos\YouTube"
```

### Enable Transcripts by Default

```bash
youtuber config set download_transcripts true
```

### Set Default Quality

```bash
youtuber config set default_quality 1080p
```

## Authentication Setup

### For Age-Restricted or Private Videos

#### Option 1: Using Cookies (Recommended)

1. Install a browser extension to export cookies:
   - Chrome/Edge: "Get cookies.txt LOCALLY"
   - Firefox: "cookies.txt"

2. Export cookies from YouTube

3. Save as `cookies.txt`

4. Use with download:
```bash
youtuber download [URL] --cookies cookies.txt
```

5. Or set as default:
```bash
youtuber config set cookies_file "path/to/cookies.txt"
```

#### Option 2: Username/Password

```bash
youtuber download [URL] --username your@email.com --password yourpassword
```

Or set in config:
```bash
youtuber config set username "your@email.com"
youtuber config set password "yourpassword"
```

**Note:** Storing passwords in config is less secure. Use cookies when possible.

## Common Use Cases

### Download Audio Only

```bash
youtuber download [URL] --quality audio
```

### Custom Output Directory

```bash
youtuber download [URL] --output-dir "D:\My Videos"
```

### Download with Verbose Logging

```bash
youtuber download [URL] --verbose
```

### Download with Debug Mode

```bash
youtuber download [URL] --debug
```

### Download Multiple Transcript Languages

```bash
youtuber download [URL] --transcripts -l en -l es -l fr
```

## Troubleshooting

### Video Unavailable

```bash
# Try with authentication
youtuber download [URL] --cookies cookies.txt --verbose
```

### Permission Errors

```bash
# Check directory permissions
youtuber paths

# Use custom directory
youtuber download [URL] --output-dir "path/with/write/access"
```

### Update yt-dlp

```bash
pip install --upgrade yt-dlp
```

### View Logs

```bash
# On Windows
explorer %APPDATA%\youtuber\logs

# On macOS
open ~/Library/Application\ Support/youtuber/logs

# On Linux
xdg-open ~/.config/youtuber/logs
```

## Development

### Run Tests

```bash
pytest tests/ -v --cov=src
```

### Format Code

```bash
black src/ tests/
```

### Type Checking

```bash
mypy src/
```

### Linting

```bash
flake8 src/ tests/
```

## Uninstallation

```bash
pip uninstall youtuber
```

To remove all data:

#### Windows
```powershell
Remove-Item -Recurse -Force "$env:APPDATA\youtuber"
```

#### macOS
```bash
rm -rf ~/Library/Application\ Support/youtuber
```

#### Linux
```bash
rm -rf ~/.config/youtuber
```

## Getting Help

```bash
# General help
youtuber --help

# Command-specific help
youtuber download --help
youtuber config --help
```

## Support

For issues, bug reports, or feature requests, please visit:
https://github.com/yourusername/youtuber/issues
