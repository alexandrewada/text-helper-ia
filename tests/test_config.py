"""
Tests for Config class
"""
import unittest
import tempfile
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary config file (don't create the file, let Config create it)
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.ini')
        self.temp_file.close()
        # Remove the file so Config will create default config
        os.unlink(self.temp_file.name)
        
        self.config = Config(self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_create_default_config(self):
        """Test default configuration creation"""
        # Check if default sections exist (DEFAULT is implicit in ConfigParser)
        self.assertTrue(self.config.config.has_section('UI'))
        self.assertTrue(self.config.config.has_section('LOGGING'))
        
        # Check default values (DEFAULT section is implicit)
        self.assertEqual(self.config.get('DEFAULT', 'model'), 'gpt-3.5-turbo')
        self.assertEqual(self.config.get('DEFAULT', 'max_tokens'), '300')
        self.assertEqual(self.config.get('DEFAULT', 'temperature'), '0.3')
    
    def test_get_set_values(self):
        """Test getting and setting configuration values"""
        # Test setting and getting values
        self.config.set('DEFAULT', 'test_key', 'test_value')
        self.assertEqual(self.config.get('DEFAULT', 'test_key'), 'test_value')
        
        # Test with fallback
        self.assertEqual(self.config.get('DEFAULT', 'nonexistent_key', 'fallback'), 'fallback')
    
    def test_get_openai_config(self):
        """Test OpenAI configuration retrieval"""
        openai_config = self.config.get_openai_config()
        
        self.assertIn('api_key', openai_config)
        self.assertIn('model', openai_config)
        self.assertIn('max_tokens', openai_config)
        self.assertIn('temperature', openai_config)
        self.assertIn('timeout', openai_config)
        
        # Check types
        self.assertIsInstance(openai_config['max_tokens'], int)
        self.assertIsInstance(openai_config['temperature'], float)
        self.assertIsInstance(openai_config['timeout'], int)
    
    def test_get_ui_config(self):
        """Test UI configuration retrieval"""
        ui_config = self.config.get_ui_config()
        
        self.assertIn('auto_close_delay', ui_config)
        
        # Check types
        self.assertIsInstance(ui_config['auto_close_delay'], int)
    
    def test_get_logging_config(self):
        """Test logging configuration retrieval"""
        logging_config = self.config.get_logging_config()
        
        self.assertIn('level', logging_config)
        self.assertIn('file', logging_config)
        self.assertIn('max_size', logging_config)
        self.assertIn('backup_count', logging_config)
        
        # Check types
        self.assertIsInstance(logging_config['max_size'], int)
        self.assertIsInstance(logging_config['backup_count'], int)
    
    def test_is_configured(self):
        """Test configuration status check"""
        # Initially not configured (empty API key)
        self.assertFalse(self.config.is_configured())
        
        # Set API key
        self.config.set('DEFAULT', 'openai_api_key', 'test_api_key')
        self.assertTrue(self.config.is_configured())
        
        # Set empty API key
        self.config.set('DEFAULT', 'openai_api_key', '')
        self.assertFalse(self.config.is_configured())
    
    def test_save_load_config(self):
        """Test configuration save and load"""
        # Set some values
        self.config.set('DEFAULT', 'test_section_key', 'test_section_value')
        self.config.set('TEST_SECTION', 'test_key', 'test_value')
        
        # Save configuration
        self.config.save_config()
        
        # Create new config instance to test loading
        new_config = Config(self.temp_file.name)
        
        # Check if values were loaded
        self.assertEqual(new_config.get('DEFAULT', 'test_section_key'), 'test_section_value')
        self.assertEqual(new_config.get('TEST_SECTION', 'test_key'), 'test_value')


if __name__ == '__main__':
    unittest.main()
