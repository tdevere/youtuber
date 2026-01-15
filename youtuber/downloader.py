"""
YouTube video downloader core with yt-dlp integration, quality selection,
format options, progress tracking, authentication, and transcript support.
"""

import yt_dlp
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
import re
import shutil

from .logger import DebugLogger
from .platform_utils import PlatformUtils


class YouTubeDownloader:
    """Core YouTube downloader using yt-dlp."""
    
    def __init__(
        self,
        output_dir: Path,
        logger: DebugLogger,
        quality: str = 'best',
        format_ext: str = 'mp4',
        cookies_file: Optional[Path] = None,
        cookies_from_browser: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ):
        """
        Initialize YouTube downloader.
        
        Args:
            output_dir: Directory to save downloads
            logger: Logger instance
            quality: Video quality (best, 1080p, 720p, 480p, 360p, audio)
            format_ext: Output format (mp4, mkv, webm)
            cookies_file: Path to cookies file for authentication
            cookies_from_browser: Browser to extract cookies from (chrome, firefox, etc.)
            username: YouTube account username
            password: YouTube account password
        """
        self.output_dir = output_dir
        self.logger = logger
        self.quality = quality
        self.format_ext = format_ext
        self.cookies_file = cookies_file
        self.cookies_from_browser = cookies_from_browser
        self.username = username
        self.password = password
        
        # Check for ffmpeg
        self.ffmpeg_available = shutil.which('ffmpeg') is not None
        if not self.ffmpeg_available:
            # Log warning about missing ffmpeg
            if self.logger:
                self.logger.warning("ffmpeg not found. Download quality options will be limited to single files.")
        
        PlatformUtils.ensure_directory(output_dir)
    
    def _get_format_selector(self) -> str:
        """
        Get yt-dlp format selector based on quality preference.
        
        Returns:
            Format selector string
        """
        if self.quality == 'best':
            # Best video + best audio if ffmpeg available
            if self.ffmpeg_available:
                return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            # Prefer HTTP download which is more robust without external tools/complex handling
            return 'best[ext=mp4][protocol^=http]/best[ext=mp4]/best'
            
        elif self.quality == 'audio':
            # Audio only
            return 'bestaudio/best'
            
        elif self.quality.endswith('p'):
            # Specific resolution (e.g., 1080p, 720p)
            height = self.quality[:-1]
            if self.ffmpeg_available:
                return f'bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}]/best'
            # Try to get HTTP based format first as it's more reliable without ffmpeg
            return f'best[height<={height}][ext=mp4][protocol^=http]/best[height<={height}][ext=mp4]/best[height<={height}]/best'
            
        else:
            # Fallback to best
            if self.ffmpeg_available:
                return 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            return 'best[ext=mp4][protocol^=http]/best[ext=mp4]/best'
    
    def _build_ydl_opts(
        self,
        output_template: str,
        download_transcripts: bool = False,
        transcript_languages: Optional[List[str]] = None,
        progress_callback: Optional[Callable] = None,
        embed_thumbnail: bool = True,
        embed_metadata: bool = True,
        write_description: bool = False,
        write_info_json: bool = False
    ) -> Dict[str, Any]:
        """
        Build yt-dlp options dictionary.
        
        Args:
            output_template: Output filename template
            download_transcripts: Whether to download subtitles
            transcript_languages: List of subtitle languages to download
            progress_callback: Callback function for download progress
            embed_thumbnail: Embed thumbnail in video file
            embed_metadata: Embed metadata in video file
            write_description: Write description to .description file
            write_info_json: Write metadata to .info.json file
        
        Returns:
            yt-dlp options dictionary
        """
        ydl_opts = {
            'format': self._get_format_selector(),
            'outtmpl': output_template,
            'quiet': not self.logger.verbose,
            'no_warnings': not self.logger.verbose,
            'ignoreerrors': False,
            'merge_output_format': self.format_ext if (self.quality != 'audio' and self.ffmpeg_available) else None,
            'writethumbnail': embed_thumbnail,
            'writesubtitles': download_transcripts,
            'writeautomaticsub': download_transcripts,
            'subtitleslangs': transcript_languages or ['en'],
            'subtitlesformat': 'vtt/srt/best',
            # Only enable embedding if ffmpeg is available
            'embedthumbnail': embed_thumbnail and self.ffmpeg_available,
            'embedsubtitles': False,  # Keep subtitles as separate files
            'writedescription': write_description,
            'writeinfojson': write_info_json,
            'no_color': False,
            'progress_hooks': [progress_callback] if progress_callback else [],
        }
        
        # Add post-processors
        postprocessors = []
        
        if embed_metadata and self.ffmpeg_available:
            postprocessors.append({'key': 'FFmpegMetadata'})
        
        if embed_thumbnail and self.ffmpeg_available:
            postprocessors.append({'key': 'EmbedThumbnail'})
        
        if self.quality == 'audio' and self.ffmpeg_available:
            postprocessors.append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            })
        
        if postprocessors:
            ydl_opts['postprocessors'] = postprocessors
        
        # Authentication
        if self.cookies_file and self.cookies_file.exists():
            ydl_opts['cookiefile'] = str(self.cookies_file)
        elif self.cookies_from_browser:
            ydl_opts['cookiesfrombrowser'] = (self.cookies_from_browser, None, None, None)
        if self.username:
            ydl_opts['username'] = self.username
        if self.password:
            ydl_opts['password'] = self.password
        
        return ydl_opts
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """
        Get video information without downloading.
        
        Args:
            url: YouTube video URL
        
        Returns:
            Video information dictionary
        
        Raises:
            Exception: If video info extraction fails
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        if self.cookies_file and self.cookies_file.exists():
            ydl_opts['cookiefile'] = str(self.cookies_file)
        elif self.cookies_from_browser:
            ydl_opts['cookiesfrombrowser'] = (self.cookies_from_browser, None, None, None)
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            self.logger.log_error_context(e, {'url': url})
            raise
    
    def download_video(
        self,
        url: str,
        download_transcripts: bool = False,
        transcript_languages: Optional[List[str]] = None,
        progress_callback: Optional[Callable] = None,
        custom_filename: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Download a YouTube video.
        
        Args:
            url: YouTube video URL
            download_transcripts: Whether to download subtitles
            transcript_languages: List of subtitle languages
            progress_callback: Callback for download progress
            custom_filename: Custom filename (without extension)
            **kwargs: Additional options (embed_thumbnail, embed_metadata, etc.)
        
        Returns:
            Dictionary with video info and file paths
        
        Raises:
            Exception: If download fails
        """
        self.logger.info(f"Starting download: {url}")
        
        # Build output template
        if custom_filename:
            safe_filename = PlatformUtils.get_safe_filename(custom_filename)
            output_template = str(self.output_dir / f"{safe_filename}.%(ext)s")
        else:
            output_template = str(self.output_dir / "%(title)s.%(ext)s")
        
        # Build yt-dlp options
        ydl_opts = self._build_ydl_opts(
            output_template=output_template,
            download_transcripts=download_transcripts,
            transcript_languages=transcript_languages,
            progress_callback=progress_callback,
            **kwargs
        )
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Download and get info
                info = ydl.extract_info(url, download=True)
                
                if info is None:
                    raise Exception("Failed to extract video information")
                
                # Get the actual downloaded filename
                if 'requested_downloads' in info and info['requested_downloads']:
                    filepath = Path(info['requested_downloads'][0]['filepath'])
                else:
                    # Construct filepath from template
                    filename = ydl.prepare_filename(info)
                    filepath = Path(filename)
                
                self.logger.success(f"Downloaded: {filepath.name}")
                
                return {
                    'info': info,
                    'filepath': filepath,
                    'video_id': info.get('id', ''),
                }
        except Exception as e:
            self.logger.log_error_context(e, {
                'url': url,
                'output_dir': str(self.output_dir),
                'quality': self.quality,
                'format': self.format_ext
            })
            raise
    
    def download_playlist(
        self,
        url: str,
        download_transcripts: bool = False,
        transcript_languages: Optional[List[str]] = None,
        progress_callback: Optional[Callable] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Download a YouTube playlist.
        
        Args:
            url: YouTube playlist URL
            download_transcripts: Whether to download subtitles
            transcript_languages: List of subtitle languages
            progress_callback: Callback for download progress
            start: Start index (1-based)
            end: End index (1-based, inclusive)
            **kwargs: Additional options
        
        Returns:
            List of dictionaries with video info and file paths
        
        Raises:
            Exception: If download fails
        """
        self.logger.info(f"Starting playlist download: {url}")
        
        output_template = str(self.output_dir / "%(playlist)s" / "%(playlist_index)s - %(title)s.%(ext)s")
        
        ydl_opts = self._build_ydl_opts(
            output_template=output_template,
            download_transcripts=download_transcripts,
            transcript_languages=transcript_languages,
            progress_callback=progress_callback,
            **kwargs
        )
        
        # Add playlist options
        if start:
            ydl_opts['playlist_start'] = start
        if end:
            ydl_opts['playlist_end'] = end
        
        ydl_opts['ignoreerrors'] = True  # Continue on errors in playlist
        
        results = []
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                if info is None:
                    raise Exception("Failed to extract playlist information")
                
                # Process each video in playlist
                entries = info.get('entries', [])
                for entry in entries:
                    if entry:
                        video_id = entry.get('id', '')
                        title = entry.get('title', 'Unknown')
                        
                        # Try to determine filepath
                        if 'requested_downloads' in entry and entry['requested_downloads']:
                            filepath = Path(entry['requested_downloads'][0]['filepath'])
                        else:
                            filename = ydl.prepare_filename(entry)
                            filepath = Path(filename)
                        
                        results.append({
                            'info': entry,
                            'filepath': filepath,
                            'video_id': video_id,
                        })
                        
                        self.logger.success(f"Downloaded: {title}")
            
            self.logger.success(f"Playlist download complete: {len(results)} videos")
            return results
            
        except Exception as e:
            self.logger.log_error_context(e, {
                'url': url,
                'output_dir': str(self.output_dir),
                'quality': self.quality
            })
            raise
    
    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL.
        
        Args:
            url: YouTube URL
        
        Returns:
            Video ID or None if not found
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def is_playlist_url(url: str) -> bool:
        """
        Check if URL is a playlist URL.
        
        Args:
            url: YouTube URL
        
        Returns:
            True if playlist URL
        """
        return 'playlist?list=' in url or '/playlists' in url
