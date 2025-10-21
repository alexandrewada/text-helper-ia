"""
Text processing utilities and clipboard management
"""
import time
from typing import Optional, Tuple
from .logger import Logger


class TextProcessor:
    """Text processing and clipboard management utilities"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def get_selected_text(self) -> Optional[str]:
        """Get selected text - DISABLED to prevent system freezing"""
        self.logger.info("Selected text capture disabled to prevent system freezing")
        return None
    
    def get_text_from_clipboard(self) -> Optional[str]:
        """Get text from clipboard - DISABLED to prevent freezing"""
        self.logger.info("Clipboard reading disabled to prevent system freezing")
        return None
    
    def get_text_from_source(self) -> Tuple[Optional[str], str, bool]:
        """Get text from clipboard only (selected text capture disabled)
        
        Returns:
            Tuple of (text, source_type, has_selection)
        """
        # Only use clipboard to prevent system freezing
        clipboard_text = self.get_text_from_clipboard()
        if clipboard_text:
            return clipboard_text, "clipboard", False
        else:
            return None, None, False
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard - DISABLED to prevent freezing"""
        self.logger.info("Clipboard copying disabled to prevent system freezing")
        return False
    
    def replace_selected_text(self, text: str) -> bool:
        """Replace selected text - DISABLED to prevent system freezing"""
        self.logger.info("Selected text replacement disabled to prevent system freezing")
        return False
    
    
    def validate_text(self, text: str) -> bool:
        """Validate text input"""
        if not text or not text.strip():
            return False
        
        # Check for reasonable length (not too short, not too long)
        if len(text.strip()) < 3:
            return False
        
        if len(text.strip()) > 10000:  # 10k characters limit
            return False
        
        return True
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        cleaned = ' '.join(text.split())
        
        # Remove control characters except newlines and tabs
        cleaned = ''.join(char for char in cleaned if ord(char) >= 32 or char in '\n\t')
        
        return cleaned.strip()
    
    def get_text_stats(self, text: str) -> dict:
        """Get statistics about the text"""
        if not text:
            return {
                'characters': 0,
                'words': 0,
                'lines': 0,
                'sentences': 0
            }
        
        # Basic stats
        characters = len(text)
        words = len(text.split())
        lines = len(text.splitlines())
        
        # Count sentences (rough estimate)
        sentences = len([s for s in text.split('.') if s.strip()])
        
        return {
            'characters': characters,
            'words': words,
            'lines': lines,
            'sentences': sentences
        }
    
    def cleanup_after_processing(self):
        """Clean up after processing (simplified - no keyboard operations)"""
        try:
            self.logger.info("Cleaning up after text processing")
            # Give system time to stabilize
            time.sleep(0.1)
            self.logger.info("Cleanup completed successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
