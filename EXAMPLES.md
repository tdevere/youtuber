# YouTuber CLI - Usage Examples

## Basic Downloads

### Single Video - Best Quality
```bash
youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8
```

### Single Video - Specific Quality
```bash
# 1080p
youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8 --quality 1080p

# 720p
youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8 --quality 720p

# Audio only
youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8 --quality audio
```

### With Transcripts
```bash
# English transcripts (default)
youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8 --transcripts

# Multiple languages
youtuber download https://www.youtube.com/watch?v=XeVLe4dX9V8 --transcripts -l en -l es -l fr
```

## Playlist Downloads

### Entire Playlist
```bash
youtuber download "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf" --playlist
```

### Playlist with Transcripts
```bash
youtuber download "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf" --playlist --transcripts
```

### Specific Playlist Range
Note: This requires modifying the CLI to support start/end options, or you can use yt-dlp directly with:
```bash
yt-dlp --playlist-start 1 --playlist-end 10 [URL]
```

## Custom Output

### Custom Directory
```bash
youtuber download [URL] --output-dir "D:\My YouTube Collection"
```

### Different Format
```bash
# MKV format
youtuber download [URL] --format mkv

# WebM format
youtuber download [URL] --format webm
```

## Authentication

### Using Cookies
```bash
# One-time use
youtuber download [URL] --cookies cookies.txt

# Set as default
youtuber config set cookies_file "C:\Users\YourName\.youtuber\cookies.txt"
youtuber download [URL]
```

### Using Username/Password
```bash
youtuber download [URL] --username your@email.com --password yourpassword
```

## Collection Management

### List All Videos
```bash
youtuber list
```

### List with Limit
```bash
youtuber list --limit 10
```

### Sort by Different Fields
```bash
# Sort by title
youtuber list --sort title --order ASC

# Sort by file size
youtuber list --sort file_size --order DESC

# Sort by upload date
youtuber list --sort upload_date --order DESC
```

### Search Collection
```bash
# Search all fields
youtuber search "python tutorial"

# Search specific field
youtuber search "python" --field title
youtuber search "TechCorp" --field uploader
```

### Get Video Info (No Download)
```bash
youtuber info https://www.youtube.com/watch?v=XeVLe4dX9V8
```

### JSON Output
```bash
# Get info as JSON
youtuber info [URL] --json-output

# List as JSON
youtuber list --json-output

# Search as JSON
youtuber search "python" --json-output
```

### Collection Statistics
```bash
youtuber stats
```

## Configuration

### View All Configuration
```bash
youtuber config list
```

### Set Individual Values
```bash
# Set download directory
youtuber config set download_dir "D:\YouTube Videos"

# Set default quality
youtuber config set default_quality 1080p

# Enable transcripts by default
youtuber config set download_transcripts true

# Set transcript languages
youtuber config set transcript_languages "en,es,fr"

# Enable verbose logging
youtuber config set verbose true
```

### Get Configuration Value
```bash
youtuber config get download_dir
youtuber config get default_quality
```

### Reset Configuration
```bash
youtuber config reset
```

## Debugging

### Verbose Mode
```bash
youtuber download [URL] --verbose
```

### Debug Mode (Maximum Detail)
```bash
youtuber download [URL] --debug
```

### View Application Paths
```bash
youtuber paths
```

## Advanced Examples

### Download Educational Playlist with All Features
```bash
youtuber download "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf" \
  --playlist \
  --quality 1080p \
  --format mp4 \
  --transcripts \
  -l en -l es \
  --output-dir "D:\Education\Python Course" \
  --verbose
```

### Download Audio-Only Podcast Series
```bash
youtuber download "https://www.youtube.com/playlist?list=PODCAST_PLAYLIST_ID" \
  --playlist \
  --quality audio \
  --output-dir "D:\Podcasts" \
  --verbose
```

### Download with Authentication and Debug
```bash
youtuber download [PRIVATE_OR_AGE_RESTRICTED_URL] \
  --cookies cookies.txt \
  --transcripts \
  --debug
```

### Batch Download Multiple Videos (Shell Script)

#### Windows PowerShell
```powershell
# Create a file urls.txt with one URL per line
$urls = Get-Content urls.txt
foreach ($url in $urls) {
    youtuber download $url --transcripts --verbose
    Start-Sleep -Seconds 2
}
```

#### Linux/macOS Bash
```bash
# Create a file urls.txt with one URL per line
while IFS= read -r url; do
    youtuber download "$url" --transcripts --verbose
    sleep 2
done < urls.txt
```

### Search and Export Collection to JSON
```bash
youtuber search "python" --json-output > python_videos.json
```

## Tips and Best Practices

### 1. Use Configuration for Common Settings
```bash
# Set once, use everywhere
youtuber config set default_quality 1080p
youtuber config set download_transcripts true
youtuber config set download_dir "D:\YouTube"

# Now just use
youtuber download [URL]
```

### 2. Use Cookies for Better Access
Many videos require authentication. Export your browser cookies once:
```bash
youtuber config set cookies_file "path/to/cookies.txt"
```

### 3. Monitor Disk Space
```bash
# Check collection size
youtuber stats
```

### 4. Use Verbose Mode for Troubleshooting
```bash
youtuber download [URL] --verbose
```

### 5. Keep yt-dlp Updated
```bash
pip install --upgrade yt-dlp
```

## Integration Examples

### Python Script Integration
```python
from youtuber import YouTubeDownloader, CollectionManager, Config
from youtuber.platform_utils import get_data_dir
from youtuber.logger import get_logger
from pathlib import Path

# Initialize
config = Config()
logger = get_logger(verbose=True)
downloader = YouTubeDownloader(
    output_dir=config.get_download_dir(),
    logger=logger,
    quality='1080p'
)

# Download video
result = downloader.download_video(
    url='https://www.youtube.com/watch?v=XeVLe4dX9V8',
    download_transcripts=True
)

# Add to collection
collection = CollectionManager(get_data_dir() / 'collection.db')
collection.add_video(result['info'], result['filepath'])

print(f"Downloaded: {result['filepath']}")
```

### Automation with Task Scheduler (Windows)
Create a PowerShell script `download_favorites.ps1`:
```powershell
$urls = @(
    "https://www.youtube.com/watch?v=VIDEO1",
    "https://www.youtube.com/watch?v=VIDEO2"
)

foreach ($url in $urls) {
    youtuber download $url --transcripts
}
```

Then schedule it with Task Scheduler to run daily/weekly.

### Automation with Cron (Linux/macOS)
```bash
# Edit crontab
crontab -e

# Add line to run daily at 2 AM
0 2 * * * /path/to/venv/bin/youtuber download [URL] >> /var/log/youtuber.log 2>&1
```
