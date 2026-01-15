"""
SQLite-based collection manager for tracking downloaded videos with metadata,
deduplication, and search capabilities.
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from contextlib import contextmanager


class CollectionManager:
    """Manages the local video collection database."""
    
    def __init__(self, db_path: Path):
        """
        Initialize the collection manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_database(self) -> None:
        """Initialize database schema."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Videos table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT UNIQUE NOT NULL,
                    url TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    duration INTEGER,
                    upload_date TEXT,
                    uploader TEXT,
                    uploader_id TEXT,
                    channel TEXT,
                    channel_id TEXT,
                    view_count INTEGER,
                    like_count INTEGER,
                    categories TEXT,
                    tags TEXT,
                    thumbnail_url TEXT,
                    file_path TEXT NOT NULL,
                    file_size INTEGER,
                    format_id TEXT,
                    format_note TEXT,
                    resolution TEXT,
                    fps INTEGER,
                    vcodec TEXT,
                    acodec TEXT,
                    downloaded_at TEXT NOT NULL,
                    UNIQUE(video_id)
                )
            """)
            
            # Transcripts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transcripts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    language TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    is_auto_generated BOOLEAN,
                    downloaded_at TEXT NOT NULL,
                    FOREIGN KEY (video_id) REFERENCES videos(video_id),
                    UNIQUE(video_id, language)
                )
            """)
            
            # Playlists table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlists (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    playlist_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    uploader TEXT,
                    video_count INTEGER,
                    downloaded_at TEXT NOT NULL
                )
            """)
            
            # Playlist videos mapping
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS playlist_videos (
                    playlist_id TEXT NOT NULL,
                    video_id TEXT NOT NULL,
                    position INTEGER,
                    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
                    FOREIGN KEY (video_id) REFERENCES videos(video_id),
                    PRIMARY KEY (playlist_id, video_id)
                )
            """)
            
            # Create indexes for better query performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_videos_video_id 
                ON videos(video_id)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_videos_title 
                ON videos(title)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_videos_downloaded_at 
                ON videos(downloaded_at)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_transcripts_video_id 
                ON transcripts(video_id)
            """)
    
    def add_video(self, video_info: Dict[str, Any], file_path: Path) -> bool:
        """
        Add a video to the collection.
        
        Args:
            video_info: Video metadata from yt-dlp
            file_path: Path to downloaded video file
        
        Returns:
            True if added successfully, False if already exists
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Extract relevant fields
                video_id = video_info.get('id', '')
                
                cursor.execute("""
                    INSERT INTO videos (
                        video_id, url, title, description, duration, upload_date,
                        uploader, uploader_id, channel, channel_id,
                        view_count, like_count, categories, tags, thumbnail_url,
                        file_path, file_size, format_id, format_note, resolution,
                        fps, vcodec, acodec, downloaded_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    video_id,
                    video_info.get('webpage_url', video_info.get('url', '')),
                    video_info.get('title', 'Unknown'),
                    video_info.get('description', ''),
                    video_info.get('duration', 0),
                    video_info.get('upload_date', ''),
                    video_info.get('uploader', ''),
                    video_info.get('uploader_id', ''),
                    video_info.get('channel', ''),
                    video_info.get('channel_id', ''),
                    video_info.get('view_count', 0),
                    video_info.get('like_count', 0),
                    ','.join(video_info.get('categories', [])),
                    ','.join(video_info.get('tags', [])) if video_info.get('tags') else '',
                    video_info.get('thumbnail', ''),
                    str(file_path),
                    file_path.stat().st_size if file_path.exists() else 0,
                    video_info.get('format_id', ''),
                    video_info.get('format_note', ''),
                    video_info.get('resolution', ''),
                    video_info.get('fps', 0),
                    video_info.get('vcodec', ''),
                    video_info.get('acodec', ''),
                    datetime.now().isoformat()
                ))
                return True
        except sqlite3.IntegrityError:
            # Video already exists
            return False
    
    def add_transcript(
        self,
        video_id: str,
        language: str,
        file_path: Path,
        is_auto_generated: bool = False
    ) -> bool:
        """
        Add a transcript to the collection.
        
        Args:
            video_id: YouTube video ID
            language: Language code
            file_path: Path to transcript file
            is_auto_generated: Whether transcript is auto-generated
        
        Returns:
            True if added successfully
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO transcripts (
                        video_id, language, file_path, is_auto_generated, downloaded_at
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    video_id,
                    language,
                    str(file_path),
                    is_auto_generated,
                    datetime.now().isoformat()
                ))
                return True
        except sqlite3.IntegrityError:
            return False
    
    def video_exists(self, video_id: str) -> bool:
        """
        Check if a video already exists in the collection.
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            True if video exists
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM videos WHERE video_id = ?", (video_id,))
            return cursor.fetchone() is not None
    
    def get_video(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Get video information from the collection.
        
        Args:
            video_id: YouTube video ID
        
        Returns:
            Video information dictionary or None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM videos WHERE video_id = ?", (video_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def list_videos(
        self,
        limit: Optional[int] = None,
        offset: int = 0,
        sort_by: str = 'downloaded_at',
        order: str = 'DESC'
    ) -> List[Dict[str, Any]]:
        """
        List videos in the collection.
        
        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            sort_by: Column to sort by
            order: Sort order (ASC or DESC)
        
        Returns:
            List of video dictionaries
        """
        valid_sort_columns = ['downloaded_at', 'title', 'upload_date', 'duration', 'file_size']
        if sort_by not in valid_sort_columns:
            sort_by = 'downloaded_at'
        
        order = order.upper()
        if order not in ['ASC', 'DESC']:
            order = 'DESC'
        
        query = f"SELECT * FROM videos ORDER BY {sort_by} {order}"
        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def search_videos(
        self,
        query: str,
        field: str = 'all',
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Search videos in the collection.
        
        Args:
            query: Search query
            field: Field to search in ('all', 'title', 'description', 'uploader')
            limit: Maximum number of results
        
        Returns:
            List of matching video dictionaries
        """
        search_pattern = f"%{query}%"
        
        if field == 'all':
            where_clause = """
                WHERE title LIKE ? OR description LIKE ? 
                OR uploader LIKE ? OR tags LIKE ?
            """
            params = [search_pattern] * 4
        elif field == 'title':
            where_clause = "WHERE title LIKE ?"
            params = [search_pattern]
        elif field == 'description':
            where_clause = "WHERE description LIKE ?"
            params = [search_pattern]
        elif field == 'uploader':
            where_clause = "WHERE uploader LIKE ?"
            params = [search_pattern]
        else:
            where_clause = "WHERE title LIKE ?"
            params = [search_pattern]
        
        sql = f"SELECT * FROM videos {where_clause} ORDER BY downloaded_at DESC"
        if limit:
            sql += f" LIMIT {limit}"
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get collection statistics.
        
        Returns:
            Dictionary with statistics
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Total videos
            cursor.execute("SELECT COUNT(*) FROM videos")
            total_videos = cursor.fetchone()[0]
            
            # Total size
            cursor.execute("SELECT SUM(file_size) FROM videos")
            total_size = cursor.fetchone()[0] or 0
            
            # Total transcripts
            cursor.execute("SELECT COUNT(*) FROM transcripts")
            total_transcripts = cursor.fetchone()[0]
            
            # Total playlists
            cursor.execute("SELECT COUNT(*) FROM playlists")
            total_playlists = cursor.fetchone()[0]
            
            # Most recent download
            cursor.execute("SELECT downloaded_at FROM videos ORDER BY downloaded_at DESC LIMIT 1")
            row = cursor.fetchone()
            last_download = row[0] if row else None
            
            return {
                'total_videos': total_videos,
                'total_size_bytes': total_size,
                'total_transcripts': total_transcripts,
                'total_playlists': total_playlists,
                'last_download': last_download
            }
    
    def delete_video(self, video_id: str, delete_file: bool = False) -> bool:
        """
        Delete a video from the collection.
        
        Args:
            video_id: YouTube video ID
            delete_file: Whether to also delete the physical file
        
        Returns:
            True if deleted successfully
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            if delete_file:
                # Get file path before deleting
                cursor.execute("SELECT file_path FROM videos WHERE video_id = ?", (video_id,))
                row = cursor.fetchone()
                if row:
                    file_path = Path(row[0])
                    if file_path.exists():
                        file_path.unlink()
            
            # Delete transcripts first (foreign key)
            cursor.execute("DELETE FROM transcripts WHERE video_id = ?", (video_id,))
            
            # Delete video
            cursor.execute("DELETE FROM videos WHERE video_id = ?", (video_id,))
            
            return cursor.rowcount > 0
