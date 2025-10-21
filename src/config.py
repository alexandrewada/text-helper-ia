"""
Configuration management for Text Helper IA
"""
import os
import configparser
from typing import Optional, Dict, Any


class Config:
    """Configuration manager for the application"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or os.path.expanduser("~/.text_helper_ia_config.ini")
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self._create_default_config()
            self.save_config()
    
    def _create_default_config(self) -> None:
        """Create default configuration"""
        self.config['DEFAULT'] = {
            'openai_api_key': '',
            'model': 'gpt-3.5-turbo',
            'max_tokens': '300',
            'temperature': '0.3',
            'timeout': '30',
            'auto_copy': 'true',
            'auto_replace_selected': 'true',
            'show_notifications': 'true',
            'theme': 'light'
        }
        
        self.config['UI'] = {
            'window_width': '600',
            'window_height': '500',
            'auto_close_delay': '10'
        }
        
        self.config['LOGGING'] = {
            'level': 'INFO',
            'file': os.path.expanduser('~/.text_helper_ia.log'),
            'max_size': '10485760',  # 10MB
            'backup_count': '3'
        }
    
    def save_config(self) -> None:
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            self.config.write(f)
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(section, key, fallback=fallback)
    
    def set(self, section: str, key: str, value: Any) -> None:
        """Set configuration value"""
        if section != 'DEFAULT' and not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
    
    def get_openai_config(self) -> Dict[str, Any]:
        """Get OpenAI configuration"""
        return {
            'api_key': self.get('DEFAULT', 'openai_api_key', ''),
            'model': self.get('DEFAULT', 'model', 'gpt-3.5-turbo'),
            'max_tokens': int(self.get('DEFAULT', 'max_tokens', '300')),
            'temperature': float(self.get('DEFAULT', 'temperature', '0.3')),
            'timeout': int(self.get('DEFAULT', 'timeout', '30'))
        }
    
    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration"""
        return {
            'window_width': int(self.get('UI', 'window_width', '600')),
            'window_height': int(self.get('UI', 'window_height', '500')),
            'auto_close_delay': int(self.get('UI', 'auto_close_delay', '10')),
            'auto_copy': self.get('DEFAULT', 'auto_copy', 'true').lower() == 'true',
            'auto_replace_selected': self.get('DEFAULT', 'auto_replace_selected', 'true').lower() == 'true',
            'show_notifications': self.get('DEFAULT', 'show_notifications', 'true').lower() == 'true',
            'theme': self.get('DEFAULT', 'theme', 'light')
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return {
            'level': self.get('LOGGING', 'level', 'INFO'),
            'file': self.get('LOGGING', 'file', os.path.expanduser('~/.text_helper_ia.log')),
            'max_size': int(self.get('LOGGING', 'max_size', '10485760')),
            'backup_count': int(self.get('LOGGING', 'backup_count', '3'))
        }
    
    def is_configured(self) -> bool:
        """Check if OpenAI API key is configured"""
        api_key = self.get('DEFAULT', 'openai_api_key', '')
        return bool(api_key and api_key.strip())
