"""
Command-line interface for YouTuber - Professional YouTube video downloader.

Provides commands for downloading videos, managing collection, searching,
and configuring the application.
"""

import sys
import click
from pathlib import Path
from typing import Optional
import json

try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import (
        Progress,
        SpinnerColumn,
        TextColumn,
        BarColumn,
        TaskProgressColumn,
        TimeRemainingColumn,
        DownloadColumn
    )
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .logger import get_logger
from .platform_utils import PlatformUtils, get_config_dir, get_data_dir, get_log_dir
from .config import Config
from .collection import CollectionManager
from .downloader import YouTubeDownloader


# Initialize console
console = Console() if RICH_AVAILABLE else None


@click.group()
@click.version_option(version='1.0.0')
@click.pass_context
def main(ctx):
    """
    YouTuber - Professional YouTube Video Downloader CLI
    
    Download YouTube videos with collection management, authentication support,
    and transcript downloading capabilities.
    """
    ctx.ensure_object(dict)


@main.command()
@click.argument('url')
@click.option('--quality', '-q', default=None, 
              help='Video quality (best, 1080p, 720p, 480p, 360p, audio)')
@click.option('--format', '-f', 'format_ext', default=None,
              help='Output format (mp4, mkv, webm)')
@click.option('--output-dir', '-o', type=click.Path(),
              help='Custom download directory')
@click.option('--transcripts', '-t', is_flag=True,
              help='Download subtitles/transcripts')
@click.option('--transcript-lang', '-l', multiple=True,
              help='Transcript languages (default: en)')
@click.option('--playlist', '-p', is_flag=True,
              help='Download entire playlist')
@click.option('--username', '-u', help='YouTube account username/email')
@click.option('--password', '-pw', help='YouTube account password')
@click.option('--cookies', '-c', type=click.Path(exists=True),
              help='Path to cookies.txt file')
@click.option('--cookies-from-browser', '-cfb', 
              type=click.Choice(['chrome', 'firefox', 'edge', 'safari', 'opera', 'brave'], case_sensitive=False),
              help='Extract cookies from browser')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--debug', '-d', is_flag=True, help='Enable debug mode')
@click.option('--no-collection', is_flag=True,
              help='Skip adding to collection database')
def download(
    url: str,
    quality: Optional[str],
    format_ext: Optional[str],
    output_dir: Optional[str],
    transcripts: bool,
    transcript_lang: tuple,
    playlist: bool,
    username: Optional[str],
    password: Optional[str],
    cookies: Optional[str],
    cookies_from_browser: Optional[str],
    verbose: bool,
    debug: bool,
    no_collection: bool
):
    """Download a YouTube video or playlist."""
    
    # Load configuration
    config = Config()
    
    # Override config with command-line options
    quality = quality or config.get('default_quality')
    format_ext = format_ext or config.get('default_format')
    transcripts = transcripts or config.get('download_transcripts')
    transcript_languages = list(transcript_lang) if transcript_lang else config.get('transcript_languages')
    
    if output_dir:
        output_path = PlatformUtils.normalize_path(output_dir)
    else:
        output_path = config.get_download_dir()
    
    # Set up logger
    debug_mode = debug or config.get('debug')
    verbose_mode = verbose or config.get('verbose')
    logger = get_logger(
        log_dir=get_log_dir(),
        verbose=verbose_mode,
        debug=debug_mode
    )
    
    # Authentication
    cookies_path = None
    if cookies:
        cookies_path = Path(cookies)
    elif config.get('cookies_file'):
        cookies_path = config.get_cookies_file()
    
    username = username or config.get('username')
    password = password or config.get('password')
    
    logger.progress(f"Initializing download from: {url}")
    logger.debug(f"Output directory: {output_path}")
    logger.debug(f"Quality: {quality}, Format: {format_ext}")
    
    try:
        # Initialize downloader
        downloader = YouTubeDownloader(
            output_dir=output_path,
            logger=logger,
            quality=quality,
            format_ext=format_ext,
            cookies_file=cookies_path,
            cookies_from_browser=cookies_from_browser,
            username=username,
            password=password
        )
        
        # Initialize collection manager
        collection = None
        if not no_collection:
            db_path = get_data_dir() / 'collection.db'
            collection = CollectionManager(db_path)
            logger.debug(f"Collection database: {db_path}")
        
        # Progress callback for rich progress bars
        progress_instance = None
        task_id = None
        
        def progress_callback(d):
            nonlocal progress_instance, task_id
            
            if d['status'] == 'downloading':
                if RICH_AVAILABLE and console and not progress_instance:
                    progress_instance = Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        TaskProgressColumn(),
                        DownloadColumn(),
                        TimeRemainingColumn(),
                        console=console
                    )
                    progress_instance.start()
                    task_id = progress_instance.add_task(
                        f"Downloading: {d.get('filename', 'video')}",
                        total=d.get('total_bytes') or d.get('total_bytes_estimate') or 100
                    )
                
                if progress_instance and task_id is not None:
                    downloaded = d.get('downloaded_bytes', 0)
                    progress_instance.update(task_id, completed=downloaded)
            
            elif d['status'] == 'finished':
                if progress_instance:
                    progress_instance.stop()
                    progress_instance = None
                logger.info(f"Download finished: {d.get('filename', '')}")
        
        # Download video or playlist
        if playlist or downloader.is_playlist_url(url):
            logger.progress("Downloading playlist...")
            results = downloader.download_playlist(
                url=url,
                download_transcripts=transcripts,
                transcript_languages=transcript_languages,
                progress_callback=progress_callback,
                embed_thumbnail=config.get('embed_thumbnail'),
                embed_metadata=config.get('embed_metadata'),
                write_description=config.get('write_description'),
                write_info_json=config.get('write_info_json')
            )
            
            # Add to collection
            if collection:
                for result in results:
                    try:
                        collection.add_video(result['info'], result['filepath'])
                    except Exception as e:
                        logger.warning(f"Failed to add to collection: {e}")
            
            logger.success(f"Successfully downloaded {len(results)} videos from playlist")
            
        else:
            logger.progress("Downloading video...")
            result = downloader.download_video(
                url=url,
                download_transcripts=transcripts,
                transcript_languages=transcript_languages,
                progress_callback=progress_callback,
                embed_thumbnail=config.get('embed_thumbnail'),
                embed_metadata=config.get('embed_metadata'),
                write_description=config.get('write_description'),
                write_info_json=config.get('write_info_json')
            )
            
            # Add to collection
            if collection:
                try:
                    if collection.add_video(result['info'], result['filepath']):
                        logger.info("Added to collection database")
                    else:
                        logger.info("Video already exists in collection")
                except Exception as e:
                    logger.warning(f"Failed to add to collection: {e}")
            
            logger.success(f"Successfully downloaded: {result['filepath'].name}")
    
    except Exception as e:
        logger.fail(f"Download failed: {str(e)}")
        if debug:
            logger.exception("Full traceback:")
        sys.exit(1)


@main.command()
@click.option('--limit', '-n', type=int, help='Number of videos to display')
@click.option('--sort', '-s', default='downloaded_at',
              type=click.Choice(['downloaded_at', 'title', 'upload_date', 'duration', 'file_size']),
              help='Sort by field')
@click.option('--order', '-o', default='DESC',
              type=click.Choice(['ASC', 'DESC']),
              help='Sort order')
@click.option('--json-output', '-j', is_flag=True, help='Output as JSON')
def list(limit: Optional[int], sort: str, order: str, json_output: bool):
    """List videos in your collection."""
    
    db_path = get_data_dir() / 'collection.db'
    collection = CollectionManager(db_path)
    
    videos = collection.list_videos(limit=limit, sort_by=sort, order=order)
    
    if json_output:
        click.echo(json.dumps(videos, indent=2, default=str))
        return
    
    if not videos:
        click.echo("No videos in collection.")
        return
    
    if RICH_AVAILABLE and console:
        table = Table(title=f"Video Collection ({len(videos)} videos)")
        table.add_column("Title", style="cyan", no_wrap=False, max_width=50)
        table.add_column("Uploader", style="green")
        table.add_column("Resolution", style="yellow")
        table.add_column("Size", style="magenta")
        table.add_column("Downloaded", style="blue")
        
        for video in videos:
            table.add_row(
                video['title'][:47] + "..." if len(video['title']) > 50 else video['title'],
                video['uploader'] or 'Unknown',
                video['resolution'] or 'N/A',
                PlatformUtils.get_file_size_human(video['file_size'] or 0),
                video['downloaded_at'][:10] if video['downloaded_at'] else 'N/A'
            )
        
        console.print(table)
    else:
        # Fallback text output
        for i, video in enumerate(videos, 1):
            click.echo(f"\n{i}. {video['title']}")
            click.echo(f"   Uploader: {video['uploader']}")
            click.echo(f"   Resolution: {video['resolution']}")
            click.echo(f"   Size: {PlatformUtils.get_file_size_human(video['file_size'] or 0)}")
            click.echo(f"   Downloaded: {video['downloaded_at'][:10] if video['downloaded_at'] else 'N/A'}")


@main.command()
@click.argument('query')
@click.option('--field', '-f', default='all',
              type=click.Choice(['all', 'title', 'description', 'uploader']),
              help='Search in specific field')
@click.option('--limit', '-n', type=int, help='Maximum results')
@click.option('--json-output', '-j', is_flag=True, help='Output as JSON')
def search(query: str, field: str, limit: Optional[int], json_output: bool):
    """Search your video collection."""
    
    db_path = get_data_dir() / 'collection.db'
    collection = CollectionManager(db_path)
    
    results = collection.search_videos(query=query, field=field, limit=limit)
    
    if json_output:
        click.echo(json.dumps(results, indent=2, default=str))
        return
    
    if not results:
        click.echo(f"No videos found matching '{query}'")
        return
    
    click.echo(f"\nFound {len(results)} video(s) matching '{query}':\n")
    
    if RICH_AVAILABLE and console:
        table = Table()
        table.add_column("Title", style="cyan", no_wrap=False, max_width=50)
        table.add_column("Uploader", style="green")
        table.add_column("Duration", style="yellow")
        table.add_column("Downloaded", style="blue")
        
        for video in results:
            duration_str = f"{video['duration'] // 60}:{video['duration'] % 60:02d}" if video['duration'] else 'N/A'
            table.add_row(
                video['title'][:47] + "..." if len(video['title']) > 50 else video['title'],
                video['uploader'] or 'Unknown',
                duration_str,
                video['downloaded_at'][:10] if video['downloaded_at'] else 'N/A'
            )
        
        console.print(table)
    else:
        for i, video in enumerate(results, 1):
            click.echo(f"{i}. {video['title']}")
            click.echo(f"   Uploader: {video['uploader']}")
            click.echo(f"   Downloaded: {video['downloaded_at'][:10] if video['downloaded_at'] else 'N/A'}\n")


@main.command()
@click.argument('url')
@click.option('--json-output', '-j', is_flag=True, help='Output as JSON')
@click.option('--cookies', '-c', type=click.Path(exists=True), help='Path to cookies.txt file')
def info(url: str, json_output: bool, cookies: Optional[str]):
    """Get information about a video without downloading."""
    
    config = Config()
    logger = get_logger(verbose=False, debug=False)
    
    cookies_path = None
    if cookies:
        cookies_path = Path(cookies)
    elif config.get('cookies_file'):
        cookies_path = config.get_cookies_file()
    
    try:
        downloader = YouTubeDownloader(
            output_dir=Path('/tmp'),  # Not used for info
            logger=logger,
            cookies_file=cookies_path
        )
        
        info_dict = downloader.get_video_info(url)
        
        if json_output:
            click.echo(json.dumps(info_dict, indent=2, default=str))
        else:
            if RICH_AVAILABLE and console:
                console.print(f"\n[bold cyan]Title:[/] {info_dict.get('title', 'N/A')}")
                console.print(f"[bold cyan]Uploader:[/] {info_dict.get('uploader', 'N/A')}")
                console.print(f"[bold cyan]Duration:[/] {info_dict.get('duration', 0) // 60}:{info_dict.get('duration', 0) % 60:02d}")
                console.print(f"[bold cyan]Views:[/] {info_dict.get('view_count', 0):,}")
                console.print(f"[bold cyan]Likes:[/] {info_dict.get('like_count', 0):,}")
                console.print(f"[bold cyan]Upload Date:[/] {info_dict.get('upload_date', 'N/A')}")
                console.print(f"[bold cyan]Description:[/]\n{info_dict.get('description', 'N/A')[:200]}...")
            else:
                click.echo(f"\nTitle: {info_dict.get('title', 'N/A')}")
                click.echo(f"Uploader: {info_dict.get('uploader', 'N/A')}")
                click.echo(f"Duration: {info_dict.get('duration', 0) // 60}:{info_dict.get('duration', 0) % 60:02d}")
                click.echo(f"Views: {info_dict.get('view_count', 0):,}")
                click.echo(f"Upload Date: {info_dict.get('upload_date', 'N/A')}\n")
    
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.group()
def config():
    """Manage configuration settings."""
    pass


@config.command('set')
@click.argument('key')
@click.argument('value')
def config_set(key: str, value: str):
    """Set a configuration value."""
    cfg = Config()
    
    # Type conversion for known keys
    if key in ['download_transcripts', 'embed_thumbnail', 'embed_metadata', 'verbose', 'debug']:
        value = value.lower() in ['true', '1', 'yes', 'on']
    elif key in ['max_downloads']:
        value = int(value)
    
    cfg.set(key, value)
    click.echo(f"Set {key} = {value}")


@config.command('get')
@click.argument('key')
def config_get(key: str):
    """Get a configuration value."""
    cfg = Config()
    value = cfg.get(key)
    if value is not None:
        click.echo(f"{key} = {value}")
    else:
        click.echo(f"Key '{key}' not found")


@config.command('list')
def config_list():
    """List all configuration."""
    cfg = Config()
    config_dict = cfg.get_all()
    
    if RICH_AVAILABLE and console:
        table = Table(title="Configuration")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in sorted(config_dict.items()):
            table.add_row(key, str(value))
        
        console.print(table)
    else:
        for key, value in sorted(config_dict.items()):
            click.echo(f"{key} = {value}")


@config.command('reset')
@click.confirmation_option(prompt='Are you sure you want to reset configuration?')
def config_reset():
    """Reset configuration to defaults."""
    cfg = Config()
    cfg.reset()
    click.echo("Configuration reset to defaults")


@main.command()
def stats():
    """Show collection statistics."""
    db_path = get_data_dir() / 'collection.db'
    collection = CollectionManager(db_path)
    
    stats_dict = collection.get_statistics()
    
    if RICH_AVAILABLE and console:
        table = Table(title="Collection Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Videos", str(stats_dict['total_videos']))
        table.add_row("Total Size", PlatformUtils.get_file_size_human(stats_dict['total_size_bytes']))
        table.add_row("Total Transcripts", str(stats_dict['total_transcripts']))
        table.add_row("Total Playlists", str(stats_dict['total_playlists']))
        table.add_row("Last Download", stats_dict['last_download'] or 'Never')
        
        console.print(table)
    else:
        click.echo("\nCollection Statistics:")
        click.echo(f"Total Videos: {stats_dict['total_videos']}")
        click.echo(f"Total Size: {PlatformUtils.get_file_size_human(stats_dict['total_size_bytes'])}")
        click.echo(f"Total Transcripts: {stats_dict['total_transcripts']}")
        click.echo(f"Last Download: {stats_dict['last_download'] or 'Never'}\n")


@main.command()
def paths():
    """Show application directory paths."""
    if RICH_AVAILABLE and console:
        table = Table(title="Application Paths")
        table.add_column("Location", style="cyan")
        table.add_column("Path", style="green")
        
        table.add_row("Config Directory", str(get_config_dir()))
        table.add_row("Data Directory", str(get_data_dir()))
        table.add_row("Log Directory", str(get_log_dir()))
        table.add_row("Download Directory", str(PlatformUtils.get_default_download_dir()))
        table.add_row("Database", str(get_data_dir() / 'collection.db'))
        table.add_row("Config File", str(get_config_dir() / 'config.json'))
        
        console.print(table)
    else:
        click.echo("\nApplication Paths:")
        click.echo(f"Config Directory: {get_config_dir()}")
        click.echo(f"Data Directory: {get_data_dir()}")
        click.echo(f"Log Directory: {get_log_dir()}")
        click.echo(f"Download Directory: {PlatformUtils.get_default_download_dir()}")
        click.echo(f"Database: {get_data_dir() / 'collection.db'}")
        click.echo(f"Config File: {get_config_dir() / 'config.json'}\n")


if __name__ == '__main__':
    main()
