"""
Cross-platform utility functions for path handling, configuration directories,
and OS-specific operations.
"""

import os
import sys
import platform
from pathlib import Path
from typing import Optional

try:
    from platformdirs import user_config_dir, user_data_dir, user_log_dir
    PLATFORMDIRS_AVAILABLE = True
except ImportError:
    PLATFORMDIRS_AVAILABLE = False


class PlatformUtils:
    """Utilities for cross-platform operations."""
    
    APP_NAME = "youtuber"
    APP_AUTHOR = "YouTuber"
    
    @staticmethod
    def get_os_name() -> str:
        """
        Get the operating system name.
        
        Returns:
            OS name: 'windows', 'macos', 'linux', or 'unknown'
        """
        system = platform.system().lower()
        if system == 'darwin':
            return 'macos'
        elif system in ['linux', 'windows']:
            return system
        return 'unknown'
    
    @staticmethod
    def get_config_dir() -> Path:
        """
        Get the configuration directory for the application.
        
        Returns:
            Path to config directory
        """
        if PLATFORMDIRS_AVAILABLE:
            config_dir = Path(user_config_dir(
                PlatformUtils.APP_NAME,
                PlatformUtils.APP_AUTHOR
            ))
        else:
            # Fallback implementation
            home = Path.home()
            os_name = PlatformUtils.get_os_name()
            
            if os_name == 'windows':
                config_dir = home / 'AppData' / 'Roaming' / PlatformUtils.APP_NAME
            elif os_name == 'macos':
                config_dir = home / 'Library' / 'Application Support' / PlatformUtils.APP_NAME
            else:  # Linux and others
                config_dir = home / '.config' / PlatformUtils.APP_NAME
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    @staticmethod
    def get_data_dir() -> Path:
        """
        Get the data directory for the application.
        
        Returns:
            Path to data directory
        """
        if PLATFORMDIRS_AVAILABLE:
            data_dir = Path(user_data_dir(
                PlatformUtils.APP_NAME,
                PlatformUtils.APP_AUTHOR
            ))
        else:
            # Fallback - use config dir for data as well
            data_dir = PlatformUtils.get_config_dir()
        
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
    
    @staticmethod
    def get_log_dir() -> Path:
        """
        Get the log directory for the application.
        
        Returns:
            Path to log directory
        """
        if PLATFORMDIRS_AVAILABLE:
            log_dir = Path(user_log_dir(
                PlatformUtils.APP_NAME,
                PlatformUtils.APP_AUTHOR
            ))
        else:
            # Fallback - use logs subdirectory in config
            log_dir = PlatformUtils.get_config_dir() / 'logs'
        
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
    
    @staticmethod
    def get_default_download_dir() -> Path:
        """
        Get the default download directory.
        
        Returns:
            Path to default download directory
        """
        home = Path.home()
        os_name = PlatformUtils.get_os_name()
        
        # Try to use OS-specific common directories
        if os_name == 'windows':
            download_dir = home / 'Videos' / 'YouTuber'
        elif os_name == 'macos':
            download_dir = home / 'Movies' / 'YouTuber'
        else:  # Linux and others
            # Try XDG user directories first
            videos_dir = home / 'Videos'
            if videos_dir.exists():
                download_dir = videos_dir / 'YouTuber'
            else:
                download_dir = home / 'YouTuber'
        
        download_dir.mkdir(parents=True, exist_ok=True)
        return download_dir
    
    @staticmethod
    def normalize_path(path: str) -> Path:
        """
        Normalize a path string to a Path object, expanding user home directory.
        
        Args:
            path: Path string (may contain ~ for home)
        
        Returns:
            Normalized Path object
        """
        return Path(path).expanduser().resolve()
    
    @staticmethod
    def ensure_directory(path: Path) -> None:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            path: Directory path
        """
        path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def get_safe_filename(filename: str, max_length: int = 255) -> str:
        """
        Convert a string to a safe filename by removing/replacing invalid characters.
        
        Args:
            filename: Original filename
            max_length: Maximum filename length
        
        Returns:
            Safe filename string
        """
        # Characters that are invalid in filenames on various OS
        invalid_chars = '<>:"/\\|?*'
        
        # Replace invalid characters with underscore
        safe_name = filename
        for char in invalid_chars:
            safe_name = safe_name.replace(char, '_')
        
        # Remove control characters
        safe_name = ''.join(char for char in safe_name if ord(char) >= 32)
        
        # Trim whitespace and dots from ends
        safe_name = safe_name.strip('. ')
        
        # Truncate to max length
        if len(safe_name) > max_length:
            name, ext = os.path.splitext(safe_name)
            max_name_length = max_length - len(ext)
            safe_name = name[:max_name_length] + ext
        
        # Ensure not empty
        if not safe_name:
            safe_name = 'unnamed'
        
        return safe_name
    
    @staticmethod
    def get_file_size_human(size_bytes: int) -> str:
        """
        Convert bytes to human-readable size.
        
        Args:
            size_bytes: Size in bytes
        
        Returns:
            Human-readable size string
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def is_windows() -> bool:
        """Check if running on Windows."""
        return sys.platform.startswith('win')
    
    @staticmethod
    def is_macos() -> bool:
        """Check if running on macOS."""
        return sys.platform == 'darwin'
    
    @staticmethod
    def is_linux() -> bool:
        """Check if running on Linux."""
        return sys.platform.startswith('linux')
    
    @staticmethod
    def get_system_info() -> dict:
        """
        Get system information for debugging.
        
        Returns:
            Dictionary with system info
        """
        return {
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'python_implementation': platform.python_implementation(),
        }


# Convenience functions
def get_config_dir() -> Path:
    """Get config directory."""
    return PlatformUtils.get_config_dir()


def get_data_dir() -> Path:
    """Get data directory."""
    return PlatformUtils.get_data_dir()


def get_log_dir() -> Path:
    """Get log directory."""
    return PlatformUtils.get_log_dir()


def get_default_download_dir() -> Path:
    """Get default download directory."""
    return PlatformUtils.get_default_download_dir()
