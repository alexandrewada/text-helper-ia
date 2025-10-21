"""
Text processing utilities and clipboard management
"""
import time
import pyperclip
from pynput import keyboard
from typing import Optional, Tuple
from .logger import Logger


class TextProcessor:
    """Text processing and clipboard management utilities"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def get_selected_text(self) -> Optional[str]:
        """Get selected text by simulating Ctrl+C and checking clipboard"""
        try:
            # Store current clipboard content
            original_clipboard = pyperclip.paste()
            self.logger.info(f"Original clipboard content: '{original_clipboard[:50]}{'...' if len(original_clipboard) > 50 else ''}'")
            
            # Simulate Ctrl+C to copy selected text
            controller = keyboard.Controller()
            
            # Add a small delay before copying
            time.sleep(0.1)
            
            controller.press(keyboard.Key.ctrl)
            controller.press('c')
            controller.release('c')
            controller.release(keyboard.Key.ctrl)
            
            # Wait a bit longer for the copy operation to complete
            time.sleep(0.2)
            
            # Get the new clipboard content
            new_clipboard = pyperclip.paste()
            self.logger.info(f"New clipboard content: '{new_clipboard[:50]}{'...' if len(new_clipboard) > 50 else ''}'")
            
            # Check if something was actually copied (different from original)
            if new_clipboard != original_clipboard and new_clipboard.strip():
                self.logger.info("Successfully captured selected text")
                return new_clipboard.strip()
            else:
                # Restore original clipboard if nothing was selected
                pyperclip.copy(original_clipboard)
                self.logger.info("No text selected, restored original clipboard")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting selected text: {e}")
            return None
    
    def get_text_from_clipboard(self) -> Optional[str]:
        """Get text from clipboard"""
        try:
            clipboard_text = pyperclip.paste()
            if clipboard_text and clipboard_text.strip():
                self.logger.info("Successfully read text from clipboard")
                return clipboard_text.strip()
            else:
                self.logger.info("Clipboard is empty or contains no text")
                return None
        except Exception as e:
            self.logger.error(f"Error reading clipboard: {e}")
            return None
    
    def get_text_from_source(self) -> Tuple[Optional[str], str, bool]:
        """Get text from selected text first, then fallback to clipboard
        
        Returns:
            Tuple of (text, source_type, has_selection)
        """
        # Try to get selected text first
        selected_text = self.get_selected_text()
        
        if selected_text:
            return selected_text, "selecionado", True
        else:
            # Fallback to clipboard
            clipboard_text = self.get_text_from_clipboard()
            if clipboard_text:
                return clipboard_text, "clipboard", False
            else:
                return None, None, False
    
    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard"""
        try:
            pyperclip.copy(text)
            self.logger.info("Text copied to clipboard successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error copying text to clipboard: {e}")
            return False
    
    def replace_selected_text(self, text: str) -> bool:
        """Replace selected text by pasting the new text"""
        try:
            self.logger.info(f"Replacing selected text with: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            
            # Store original clipboard content
            original_clipboard = pyperclip.paste()
            
            # Copy new text to clipboard
            pyperclip.copy(text)
            time.sleep(0.2)
            
            # Verify clipboard was updated
            if pyperclip.paste() != text:
                self.logger.error("Failed to copy text to clipboard")
                pyperclip.copy(original_clipboard)
                return False
            
            # Simulate Ctrl+V to paste
            controller = keyboard.Controller()
            time.sleep(0.1)
            
            controller.press(keyboard.Key.ctrl)
            controller.press('v')
            controller.release('v')
            controller.release(keyboard.Key.ctrl)
            
            time.sleep(0.3)
            
            self.logger.info("Text replacement completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Error replacing selected text: {e}")
            try:
                pyperclip.copy(original_clipboard)
            except:
                pass
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
