"""
Unit tests for YouTuber application.
"""

import unittest
from pathlib import Path
import tempfile
import shutil

from youtuber.platform_utils import PlatformUtils
from youtuber.config import Config
from youtuber.collection import CollectionManager


class TestPlatformUtils(unittest.TestCase):
    """Test platform utilities."""
    
    def test_get_os_name(self):
        """Test OS name detection."""
        os_name = PlatformUtils.get_os_name()
        self.assertIn(os_name, ['windows', 'macos', 'linux', 'unknown'])
    
    def test_get_safe_filename(self):
        """Test filename sanitization."""
        unsafe = 'test<>:"|?*file.mp4'
        safe = PlatformUtils.get_safe_filename(unsafe)
        self.assertNotIn('<', safe)
        self.assertNotIn('>', safe)
        self.assertNotIn(':', safe)
    
    def test_get_file_size_human(self):
        """Test human-readable file size."""
        self.assertEqual(PlatformUtils.get_file_size_human(1024), "1.00 KB")
        self.assertEqual(PlatformUtils.get_file_size_human(1048576), "1.00 MB")
        self.assertEqual(PlatformUtils.get_file_size_human(1073741824), "1.00 GB")
    
    def test_normalize_path(self):
        """Test path normalization."""
        path = PlatformUtils.normalize_path("~/test")
        self.assertTrue(path.is_absolute())


class TestConfig(unittest.TestCase):
    """Test configuration management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = Path(self.temp_dir) / 'test_config.json'
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_config_creation(self):
        """Test config file creation."""
        config = Config(self.config_path)
        self.assertTrue(self.config_path.exists())
    
    def test_config_get_set(self):
        """Test getting and setting config values."""
        config = Config(self.config_path)
        config.set('test_key', 'test_value')
        self.assertEqual(config.get('test_key'), 'test_value')
    
    def test_config_defaults(self):
        """Test default configuration values."""
        config = Config(self.config_path)
        self.assertIsNotNone(config.get('download_dir'))
        self.assertIsNotNone(config.get('default_quality'))
    
    def test_config_reset(self):
        """Test config reset."""
        config = Config(self.config_path)
        config.set('test_key', 'test_value')
        config.reset()
        self.assertIsNone(config.get('test_key'))


class TestCollectionManager(unittest.TestCase):
    """Test collection database management."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / 'test_collection.db'
        self.collection = CollectionManager(self.db_path)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir)
    
    def test_database_creation(self):
        """Test database file creation."""
        self.assertTrue(self.db_path.exists())
    
    def test_add_video(self):
        """Test adding a video to collection."""
        video_info = {
            'id': 'test123',
            'title': 'Test Video',
            'url': 'https://youtube.com/watch?v=test123',
            'duration': 300,
            'uploader': 'Test Uploader'
        }
        
        # Create dummy file
        test_file = Path(self.temp_dir) / 'test.mp4'
        test_file.touch()
        
        result = self.collection.add_video(video_info, test_file)
        self.assertTrue(result)
        
        # Try adding again (should fail due to duplicate)
        result = self.collection.add_video(video_info, test_file)
        self.assertFalse(result)
    
    def test_video_exists(self):
        """Test checking if video exists."""
        video_info = {
            'id': 'test456',
            'title': 'Test Video 2',
            'url': 'https://youtube.com/watch?v=test456',
        }
        
        test_file = Path(self.temp_dir) / 'test2.mp4'
        test_file.touch()
        
        self.assertFalse(self.collection.video_exists('test456'))
        self.collection.add_video(video_info, test_file)
        self.assertTrue(self.collection.video_exists('test456'))
    
    def test_get_video(self):
        """Test retrieving video information."""
        video_info = {
            'id': 'test789',
            'title': 'Test Video 3',
            'url': 'https://youtube.com/watch?v=test789',
        }
        
        test_file = Path(self.temp_dir) / 'test3.mp4'
        test_file.touch()
        
        self.collection.add_video(video_info, test_file)
        retrieved = self.collection.get_video('test789')
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['video_id'], 'test789')
        self.assertEqual(retrieved['title'], 'Test Video 3')
    
    def test_list_videos(self):
        """Test listing videos."""
        # Add multiple videos
        for i in range(5):
            video_info = {
                'id': f'test{i}',
                'title': f'Test Video {i}',
                'url': f'https://youtube.com/watch?v=test{i}',
            }
            test_file = Path(self.temp_dir) / f'test{i}.mp4'
            test_file.touch()
            self.collection.add_video(video_info, test_file)
        
        videos = self.collection.list_videos(limit=3)
        self.assertEqual(len(videos), 3)
    
    def test_search_videos(self):
        """Test searching videos."""
        video_info = {
            'id': 'searchtest',
            'title': 'Python Tutorial for Beginners',
            'url': 'https://youtube.com/watch?v=searchtest',
            'uploader': 'Tech Channel'
        }
        
        test_file = Path(self.temp_dir) / 'searchtest.mp4'
        test_file.touch()
        self.collection.add_video(video_info, test_file)
        
        results = self.collection.search_videos('Python')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['video_id'], 'searchtest')
    
    def test_get_statistics(self):
        """Test getting collection statistics."""
        video_info = {
            'id': 'stats_test',
            'title': 'Stats Test Video',
            'url': 'https://youtube.com/watch?v=stats_test',
        }
        
        test_file = Path(self.temp_dir) / 'stats_test.mp4'
        test_file.write_text('dummy content')
        self.collection.add_video(video_info, test_file)
        
        stats = self.collection.get_statistics()
        self.assertEqual(stats['total_videos'], 1)
        self.assertGreater(stats['total_size_bytes'], 0)


if __name__ == '__main__':
    unittest.main()
