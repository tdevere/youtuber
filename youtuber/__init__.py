"""
YouTuber - Professional YouTube video downloader CLI.

A powerful, cross-platform command-line tool for downloading YouTube videos
with collection management, authentication support, and transcript downloading.
"""

__version__ = "1.0.0"
__author__ = "YouTuber Developer"
__license__ = "MIT"

from .cli import main
from .downloader import YouTubeDownloader
from .collection import CollectionManager
from .config import Config
from .logger import get_logger, DebugLogger
from .platform_utils import PlatformUtils

__all__ = [
    'main',
    'YouTubeDownloader',
    'CollectionManager',
    'Config',
    'get_logger',
    'DebugLogger',
    'PlatformUtils',
]
