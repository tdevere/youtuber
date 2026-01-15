"""
Enhanced logging and debugging system for YouTuber CLI.

Provides configurable verbosity levels, structured logging to file and console,
colored output, and comprehensive error context capture for troubleshooting.
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
import traceback

try:
    from rich.console import Console
    from rich.logging import RichHandler
    from rich.traceback import install as install_rich_traceback
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

import colorama


class DebugLogger:
    """Enhanced logger with debugging capabilities."""
    
    def __init__(
        self,
        name: str = "youtuber",
        log_dir: Optional[Path] = None,
        verbose: bool = False,
        debug: bool = False
    ):
        """
        Initialize the debug logger.
        
        Args:
            name: Logger name
            log_dir: Directory for log files
            verbose: Enable verbose output
            debug: Enable debug mode with detailed diagnostics
        """
        self.name = name
        self.verbose = verbose
        self.debug_mode = debug
        self.console = Console() if RICH_AVAILABLE else None
        
        # Set log level based on verbosity
        if debug:
            self.log_level = logging.DEBUG
        elif verbose:
            self.log_level = logging.INFO
        else:
            self.log_level = logging.WARNING
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)
        self.logger.handlers.clear()  # Clear existing handlers
        
        # Initialize colorama for cross-platform colored output
        colorama.init()
        
        # Set up console handler
        self._setup_console_handler()
        
        # Set up file handler if log directory is provided
        if log_dir:
            self._setup_file_handler(log_dir)
        
        # Install rich traceback if available and debug mode is on
        if RICH_AVAILABLE and debug:
            install_rich_traceback(show_locals=True)
    
    def _setup_console_handler(self) -> None:
        """Set up console handler with appropriate formatting."""
        if RICH_AVAILABLE and self.console:
            # Use Rich handler for beautiful console output
            console_handler = RichHandler(
                console=self.console,
                show_time=True,
                show_path=self.debug_mode,
                rich_tracebacks=True,
                tracebacks_show_locals=self.debug_mode,
                markup=True
            )
        else:
            # Fall back to standard handler with colors
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(ColoredFormatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
        
        console_handler.setLevel(self.log_level)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self, log_dir: Path) -> None:
        """Set up file handler for persistent logging."""
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"youtuber_{timestamp}.log"
        
        # Also create/append to a main log file
        main_log_file = log_dir / "youtuber.log"
        
        # Detailed file handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # Always log everything to file
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Main log file handler
        main_file_handler = logging.FileHandler(main_log_file, encoding='utf-8')
        main_file_handler.setLevel(logging.INFO)
        main_file_handler.setFormatter(file_formatter)
        self.logger.addHandler(main_file_handler)
        
        self.logger.info(f"Logging to: {log_file}")
    
    def debug(self, message: str, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs) -> None:
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs) -> None:
        """Log error message."""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs) -> None:
        """Log critical message."""
        self.logger.critical(message, **kwargs)
    
    def exception(self, message: str, exc_info: bool = True) -> None:
        """Log exception with full traceback."""
        self.logger.exception(message, exc_info=exc_info)
    
    def log_context(self, context: dict) -> None:
        """Log contextual information for debugging."""
        if self.debug_mode:
            self.logger.debug("=" * 50)
            self.logger.debug("DEBUG CONTEXT:")
            for key, value in context.items():
                self.logger.debug(f"  {key}: {value}")
            self.logger.debug("=" * 50)
    
    def log_error_context(self, error: Exception, context: Optional[dict] = None) -> None:
        """
        Log comprehensive error context for troubleshooting.
        
        Args:
            error: The exception that occurred
            context: Additional context information
        """
        self.logger.error("=" * 70)
        self.logger.error("ERROR OCCURRED")
        self.logger.error("=" * 70)
        self.logger.error(f"Error Type: {type(error).__name__}")
        self.logger.error(f"Error Message: {str(error)}")
        
        if context:
            self.logger.error("\nContext:")
            for key, value in context.items():
                self.logger.error(f"  {key}: {value}")
        
        self.logger.error("\nTraceback:")
        self.logger.error(traceback.format_exc())
        self.logger.error("=" * 70)
    
    def progress(self, message: str) -> None:
        """Log progress message (always visible unless quiet mode)."""
        if self.console and RICH_AVAILABLE:
            self.console.print(f"[cyan]➜[/cyan] {message}")
        else:
            print(f"➜ {message}")
    
    def success(self, message: str) -> None:
        """Log success message."""
        if self.console and RICH_AVAILABLE:
            self.console.print(f"[green]✓[/green] {message}")
        else:
            print(f"✓ {message}")
    
    def fail(self, message: str) -> None:
        """Log failure message."""
        if self.console and RICH_AVAILABLE:
            self.console.print(f"[red]✗[/red] {message}")
        else:
            print(f"✗ {message}")


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output for different log levels."""
    
    # Color codes
    COLORS = {
        'DEBUG': colorama.Fore.CYAN,
        'INFO': colorama.Fore.GREEN,
        'WARNING': colorama.Fore.YELLOW,
        'ERROR': colorama.Fore.RED,
        'CRITICAL': colorama.Fore.RED + colorama.Style.BRIGHT,
    }
    
    RESET = colorama.Style.RESET_ALL
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


def get_logger(
    name: str = "youtuber",
    log_dir: Optional[Path] = None,
    verbose: bool = False,
    debug: bool = False
) -> DebugLogger:
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name
        log_dir: Directory for log files
        verbose: Enable verbose output
        debug: Enable debug mode
    
    Returns:
        DebugLogger instance
    """
    return DebugLogger(name=name, log_dir=log_dir, verbose=verbose, debug=debug)
