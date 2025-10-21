"""
Tests for TextProcessor class
"""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.text_processor import TextProcessor


class TestTextProcessor(unittest.TestCase):
    """Test cases for TextProcessor"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_logger = Mock()
        self.processor = TextProcessor(self.mock_logger)
    
    def test_validate_text_valid(self):
        """Test text validation with valid text"""
        valid_text = "Este é um texto válido para teste."
        self.assertTrue(self.processor.validate_text(valid_text))
    
    def test_validate_text_empty(self):
        """Test text validation with empty text"""
        self.assertFalse(self.processor.validate_text(""))
        self.assertFalse(self.processor.validate_text("   "))
        self.assertFalse(self.processor.validate_text(None))
    
    def test_validate_text_too_short(self):
        """Test text validation with text too short"""
        short_text = "ab"
        self.assertFalse(self.processor.validate_text(short_text))
    
    def test_validate_text_too_long(self):
        """Test text validation with text too long"""
        long_text = "a" * 10001  # More than 10k characters
        self.assertFalse(self.processor.validate_text(long_text))
    
    def test_clean_text(self):
        """Test text cleaning functionality"""
        dirty_text = "  Este   é   um   texto   com   espaços   extras.  \n\n\n"
        cleaned = self.processor.clean_text(dirty_text)
        expected = "Este é um texto com espaços extras."
        self.assertEqual(cleaned, expected)
    
    def test_clean_text_empty(self):
        """Test text cleaning with empty text"""
        self.assertEqual(self.processor.clean_text(""), "")
        self.assertEqual(self.processor.clean_text(None), "")
    
    def test_get_text_stats(self):
        """Test text statistics calculation"""
        text = "Este é um texto de teste.\nTem duas linhas."
        stats = self.processor.get_text_stats(text)
        
        self.assertEqual(stats['characters'], len(text))
        self.assertEqual(stats['words'], 9)  # "Este é um texto de teste. Tem duas linhas." = 9 words
        self.assertEqual(stats['lines'], 2)
        self.assertEqual(stats['sentences'], 2)
    
    def test_get_text_stats_empty(self):
        """Test text statistics with empty text"""
        stats = self.processor.get_text_stats("")
        
        self.assertEqual(stats['characters'], 0)
        self.assertEqual(stats['words'], 0)
        self.assertEqual(stats['lines'], 0)
        self.assertEqual(stats['sentences'], 0)
    
    @patch('pyperclip.paste')
    @patch('pyperclip.copy')
    def test_copy_to_clipboard_success(self, mock_copy, mock_paste):
        """Test successful clipboard copy"""
        test_text = "Texto de teste"
        result = self.processor.copy_to_clipboard(test_text)
        
        self.assertTrue(result)
        mock_copy.assert_called_once_with(test_text)
    
    @patch('pyperclip.copy')
    def test_copy_to_clipboard_error(self, mock_copy):
        """Test clipboard copy with error"""
        mock_copy.side_effect = Exception("Clipboard error")
        test_text = "Texto de teste"
        
        result = self.processor.copy_to_clipboard(test_text)
        
        self.assertFalse(result)
        self.mock_logger.error.assert_called()


if __name__ == '__main__':
    unittest.main()
