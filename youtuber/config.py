"""
Configuration management for user preferences, download settings,
and application state.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .platform_utils import PlatformUtils


class Config:
    """Configuration manager for application settings."""
    
    DEFAULT_CONFIG = {
        'download_dir': str(PlatformUtils.get_default_download_dir()),
        'default_quality': 'best',
        'default_format': 'mp4',
        'download_transcripts': False,
        'transcript_languages': ['en'],
        'cookies_file': '',
        'username': '',
        'password': '',
        'max_downloads': 5,
        'embed_thumbnail': True,
        'embed_metadata': True,
        'write_description': False,
        'write_info_json': False,
        'keep_video': True,
        'extract_audio': False,
        'audio_format': 'mp3',
        'audio_quality': '192',
        'quiet': False,
        'verbose': False,
        'debug': False
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to config file (defaults to platform-specific location)
        """
        if config_path is None:
            config_path = PlatformUtils.get_config_dir() / 'config.json'
        
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.load()
    
    def load(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in self.DEFAULT_CONFIG.items():
                    if key not in self.config:
                        self.config[key] = value
            except (json.JSONDecodeError, IOError):
                # If config is corrupted, use defaults
                self.config = self.DEFAULT_CONFIG.copy()
        else:
            # No config file, use defaults
            self.config = self.DEFAULT_CONFIG.copy()
            self.save()
    
    def save(self) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
        
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.
        
        Returns:
            Dictionary of all configuration
        """
        return self.config.copy()
    
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update multiple configuration values.
        
        Args:
            updates: Dictionary of updates
        """
        self.config.update(updates)
        self.save()
    
    def get_download_dir(self) -> Path:
        """Get download directory as Path object."""
        return PlatformUtils.normalize_path(self.config['download_dir'])
    
    def get_cookies_file(self) -> Optional[Path]:
        """Get cookies file path if configured."""
        cookies = self.config.get('cookies_file', '')
        if cookies:
            return PlatformUtils.normalize_path(cookies)
        return None
