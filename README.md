# YouTuber - Professional YouTube Video Downloader CLI

A powerful, cross-platform command-line tool for downloading YouTube videos with advanced features including collection management, authentication support, and transcript downloading.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Features

- 🎥 **Download Videos** - Single videos, playlists, or entire channels
- 📝 **Transcript Support** - Download subtitles and auto-generated captions in multiple languages
- 🗃️ **Collection Management** - SQLite-based local library with metadata tracking
- 🔐 **Authentication** - Support for age-restricted and private videos via cookies
- 🎨 **Quality Selection** - Choose specific resolutions (1080p, 720p, etc.) or formats (mp4, webm, mkv)
- 🔍 **Search & Filter** - Query your local collection with powerful search
- 📊 **Statistics** - Track your collection size, downloads, and more
- 🪵 **Enhanced Debugging** - Comprehensive logging and error diagnostics
- 🖥️ **Cross-Platform** - Works seamlessly on Windows, macOS, and Linux
- ⚡ **Professional CLI** - Built with Click and Rich for beautiful terminal UI

## 📋 Requirements

- Python 3.8 or higher
- ffmpeg (for merging video/audio streams)
- yt-dlp (installed automatically)

## 🚀 Installation

### Quick Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/youtuber.git
cd youtuber

# Run setup script
# Windows:
.\setup.ps1

# macOS/Linux:
chmod +x setup.sh
./setup.sh
```

### Manual Installation

```bash
# Clone and navigate
git clone https://github.com/yourusername/youtuber.git
cd youtuber

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install package
pip install -e .
```

### Install ffmpeg

**Windows (using winget):**
```powershell
winget install Gyan.FFmpeg
```

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install ffmpeg
```

## 📖 Quick Start

### Basic Usage

```bash
# Download a video (default quality: best)
youtuber download https://www.youtube.com/watch?v=VIDEO_ID

# Download with specific quality
youtuber download https://www.youtube.com/watch?v=VIDEO_ID --quality 1080p

# Download with transcripts
youtuber download https://www.youtube.com/watch?v=VIDEO_ID --transcripts

# Download entire playlist
youtuber download https://www.youtube.com/playlist?list=PLAYLIST_ID --playlist
```

### Authentication (for age-restricted/private videos)

```bash
# Using browser cookies
youtuber download URL --cookies-from-browser chrome

# Using exported cookies file
youtuber download URL --cookies cookies.txt
```

### Collection Management

```bash
# List all downloaded videos
youtuber list

# Search your collection
youtuber search "python tutorial"

# View statistics
youtuber stats

# Get video info without downloading
youtuber info https://www.youtube.com/watch?v=VIDEO_ID
```

### Configuration

```bash
# View current configuration
youtuber config list

# Set default download directory
youtuber config set download_dir "C:\Videos"

# Set default quality
youtuber config set default_quality 1080p

# View all paths
youtuber paths
```

## 📚 Command Reference

### `download` - Download videos

```bash
youtuber download URL [OPTIONS]

Options:
  -q, --quality TEXT          Video quality (best, 1080p, 720p, 480p, 360p, audio)
  -f, --format TEXT           Output format (mp4, mkv, webm)
  -o, --output-dir PATH       Custom download directory
  -t, --transcripts           Download subtitles/transcripts
  -l, --transcript-lang TEXT  Transcript languages (default: en)
  -p, --playlist              Download entire playlist
  -u, --username TEXT         YouTube account username/email
  -pw, --password TEXT        YouTube account password
  -c, --cookies PATH          Path to cookies.txt file
  -cfb, --cookies-from-browser [chrome|firefox|edge|safari|opera|brave]
                              Extract cookies from browser
  -v, --verbose               Enable verbose logging
  -d, --debug                 Enable debug mode
  --no-collection             Skip adding to collection database
```

### `list` - List downloaded videos

```bash
youtuber list [OPTIONS]

Options:
  --sort-by TEXT   Sort by: date, title, size (default: date)
  --limit INTEGER  Maximum number of videos to show
```

### `search` - Search collection

```bash
youtuber search QUERY [OPTIONS]

Options:
  --limit INTEGER  Maximum results to show
```

### `info` - Get video information

```bash
youtuber info URL [OPTIONS]

Options:
  -v, --verbose  Show detailed information
```

### `config` - Manage configuration

```bash
# List all settings
youtuber config list

# Get specific setting
youtuber config get SETTING_NAME

# Set a value
youtuber config set SETTING_NAME VALUE

# Reset to defaults
youtuber config reset
```

### `stats` - View collection statistics

```bash
youtuber stats
```

### `paths` - Show application directories

```bash
youtuber paths
```

## 🔒 Security & Privacy

- **No data collection** - All data stays on your machine
- **Sensitive files protected** - `.gitignore` prevents committing cookies, configs, and downloads
- **Cookie encryption** - When using `--cookies-from-browser`, relies on browser's native encryption
- **No API keys required** - Uses yt-dlp's direct extraction

### Important Security Notes:

1. **Never commit** `cookies.txt` or `config.json` files
2. **Clear cookies** when done if using shared machine: `rm cookies.txt`
3. **Use environment-specific configs** for different machines

## 🗂️ Project Structure

```
YouTuber/
├── youtuber/              # Main package
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # Entry point
│   ├── cli.py             # CLI commands (Click)
│   ├── downloader.py      # YouTube download logic (yt-dlp)
│   ├── collection.py      # SQLite collection management
│   ├── config.py          # Configuration management
│   ├── logger.py          # Enhanced logging system
│   └── platform_utils.py  # Cross-platform utilities
├── tests/                 # Test suite
│   └── test_youtuber.py   # Unit tests
├── docs/                  # Documentation
├── setup.py               # Package setup
├── pyproject.toml         # Build configuration
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=youtuber tests/

# Run specific test
pytest tests/test_youtuber.py::test_config
```

## 🛠️ Development

```bash
# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run linter
flake8 youtuber/

# Format code
black youtuber/
```

## 🐛 Troubleshooting

### "ffmpeg not found" error

Install ffmpeg (see [Installation](#install-ffmpeg) section)

### "Could not copy Chrome cookie database" error

Close your browser completely before running with `--cookies-from-browser`

### "Sign in to confirm you're not a bot" error

Some videos require authentication. Use `--cookies-from-browser` or `--cookies`:

```bash
youtuber download URL --cookies-from-browser chrome
```

### Permission errors on Windows

Run PowerShell as Administrator for first-time setup

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The excellent YouTube downloader
- [Click](https://click.palletsprojects.com/) - Beautiful CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting and UI

## 📮 Support

For issues, questions, or suggestions, please [open an issue](https://github.com/yourusername/youtuber/issues) on GitHub.

## ⚠️ Disclaimer

This tool is for personal use only. Respect copyright laws and YouTube's Terms of Service. Only download videos you have the right to download.

---

**Made with ❤️ for the community**

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

## Requirements

- Python 3.8 or higher
- ffmpeg (optional, for format conversion)

## License

MIT License - see LICENSE file for details

## Troubleshooting

### Common Issues

**Video unavailable**: Check if video is region-restricted or requires authentication

**Download fails**: Update yt-dlp: `pip install --upgrade yt-dlp`

**Permission errors**: Check write permissions in download directory

**FFmpeg not found**: Install ffmpeg for format conversion support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The powerful YouTube downloader library
- [Click](https://click.palletsprojects.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
