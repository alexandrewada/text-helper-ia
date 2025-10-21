"""
Linux-specific Hotkey Manager for Text Helper AI
Uses a combination of approaches that work well on Linux
"""
import threading
import time
import subprocess
import os
import signal
from typing import Optional, Callable
from .logger import Logger


class LinuxHotkeyManager:
    """Linux-specific hotkey manager with multiple fallback options"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.is_running = False
        self.callbacks = {}  # Dictionary to store multiple callbacks
        self.trigger_file = os.path.expanduser("~/.text_helper_ai_trigger")
        self.monitor_thread: Optional[threading.Thread] = None
        
    def register_hotkey(self, keys: list, callback: Callable[[], None], description: str = ""):
        """Register a hotkey callback"""
        key_str = "+".join(keys)
        self.callbacks[key_str] = {
            'callback': callback,
            'description': description,
            'keys': keys
        }
        self.logger.info(f"Registered hotkey {keys} for: {description}")
        
        # Create trigger file with instructions
        self._create_trigger_file()
        
        # Show notification
        self._show_setup_notification()
    
    def register_operation(self, operation: str, callback: Callable[[], None], description: str = ""):
        """Register a specific operation callback"""
        self.callbacks[operation] = {
            'callback': callback,
            'description': description,
            'operation': operation
        }
        self.logger.info(f"Registered operation '{operation}' for: {description}")
        
        # Update trigger file
        self._create_trigger_file()
    
    def start_listening(self):
        """Start the hotkey system"""
        if self.is_running:
            return
            
        self.is_running = True
        self.monitor_thread = threading.Thread(target=self._monitor_trigger_file, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Linux hotkey system started")
    
    def stop_listening(self):
        """Stop the hotkey system"""
        self.is_running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        
        # Clean up trigger file
        try:
            if os.path.exists(self.trigger_file):
                os.remove(self.trigger_file)
        except:
            pass
            
        self.logger.info("Linux hotkey system stopped")
    
    def _create_trigger_file(self):
        """Create trigger file with instructions"""
        try:
            with open(self.trigger_file, 'w') as f:
                f.write(f"# Text Helper AI - Hotkey Triggers\n")
                f.write(f"# Atalhos disponíveis:\n")
                
                for key_str, hotkey_info in self.callbacks.items():
                    key_combo = key_str.upper()
                    description = hotkey_info['description']
                    f.write(f"# {key_combo}: {description}\n")
                
                f.write(f"\n# Para usar os atalhos, execute:\n")
                f.write(f"# echo 'operation' >> {self.trigger_file}\n")
                f.write(f"# Onde 'operation' é uma das operações disponíveis\n\n")
                
                f.write(f"# Operações disponíveis:\n")
                operations = {
                    'shorten': 'Encurtar texto',
                    'improve': 'Melhorar texto',
                    'informal': 'Tornar informal',
                    'formal': 'Tornar formal',
                    'spellcheck': 'Corrigir ortografia',
                    'summarize': 'Resumir texto',
                    'expand': 'Expandir texto',
                    'translate_en': 'Traduzir para inglês',
                    'translate_pt': 'Traduzir para português',
                    'creative': 'Versão criativa',
                    'technical': 'Versão técnica',
                    'emojify': 'Adicionar emojis',
                    'analyze': 'Analisar texto',
                    'rewrite': 'Reescrever texto'
                }
                
                for op, desc in operations.items():
                    f.write(f"# {op}: {desc}\n")
                    
        except Exception as e:
            self.logger.error(f"Error creating trigger file: {e}")
    
    def _show_setup_notification(self):
        """Show setup notification with instructions"""
        try:
            # Try desktop notification
            try:
                subprocess.run([
                    'notify-send', 
                    'Text Helper AI - Atalhos Configurados', 
                    f"Atalhos configurados!\n\nPara usar:\n1. Selecione um texto\n2. Execute: echo 'operation' >> {self.trigger_file}\n3. Ou use a janela principal",
                    '--icon=info',
                    '--expire-time=8000'
                ], check=False)
            except:
                pass
            
            # Always print to console
            print(f"\n🔔 Text Helper AI - Atalhos Configurados")
            print(f"⌨️  Atalhos disponíveis:")
            
            for key_str, hotkey_info in self.callbacks.items():
                key_combo = key_str.upper()
                description = hotkey_info['description']
                print(f"   {key_combo}: {description}")
            
            print(f"\n🚀 Para usar os atalhos:")
            print(f"   1. Selecione um texto")
            print(f"   2. Execute: echo 'operation' >> {self.trigger_file}")
            print(f"   3. Ou use a janela principal")
            print(f"\n💡 Operações disponíveis:")
            operations = ['shorten', 'improve', 'informal', 'formal', 'spellcheck', 'summarize', 'expand', 'translate_en', 'translate_pt', 'creative', 'technical', 'emojify', 'analyze', 'rewrite']
            print(f"   {', '.join(operations)}")
            print()
                
        except Exception as e:
            self.logger.error(f"Error showing setup notification: {e}")
    
    def _monitor_trigger_file(self):
        """Monitor the trigger file for changes"""
        last_modified = 0
        
        while self.is_running:
            try:
                if os.path.exists(self.trigger_file):
                    current_modified = os.path.getmtime(self.trigger_file)
                    if current_modified > last_modified:
                        last_modified = current_modified
                        
                        # Read the file to get the operation
                        try:
                            with open(self.trigger_file, 'r') as f:
                                content = f.read().strip()
                                
                            # Check if it's a valid operation
                            operations = ['shorten', 'improve', 'informal', 'formal', 'spellcheck', 'summarize', 'expand', 'translate_en', 'translate_pt', 'creative', 'technical', 'emojify', 'analyze', 'rewrite']
                            
                            # Get the last line that contains an operation
                            lines = content.split('\n')
                            operation = None
                            for line in reversed(lines):
                                line = line.strip()
                                if line in operations:
                                    operation = line
                                    break
                            
                            if operation:
                                self.logger.info(f"Trigger file activated - operation: {operation}")
                                # Find callback for this operation
                                for key_str, hotkey_info in self.callbacks.items():
                                    if hotkey_info.get('operation') == operation:
                                        hotkey_info['callback']()
                                        break
                            else:
                                # Default callback if no specific operation
                                for key_str, hotkey_info in self.callbacks.items():
                                    if not hotkey_info.get('operation'):
                                        hotkey_info['callback']()
                                        break
                                        
                        except Exception as e:
                            self.logger.error(f"Error reading trigger file: {e}")
                
                time.sleep(0.3)
            except Exception as e:
                self.logger.error(f"Error monitoring trigger file: {e}")
                break


class SystemTrayHotkeyManager:
    """Hotkey manager using system tray integration"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
        self.is_running = False
        self.callback: Optional[Callable[[], None]] = None
        
    def register_hotkey(self, keys: list, callback: Callable[[], None], description: str = ""):
        """Register a hotkey callback"""
        self.callback = callback
        self.logger.info(f"Registered system tray hotkey for: {description}")
        
        # Show instructions
        key_combo = "+".join(keys).upper()
        print(f"\n🔔 Text Helper AI - Sistema de Atalhos")
        print(f"⌨️  Atalho configurado: {key_combo}")
        print(f"📝 {description}")
        print(f"\n💡 Como usar:")
        print(f"   1. Use o botão 'Mostrar Menu Flutuante' na janela principal")
        print(f"   2. Ou use o comando de arquivo trigger")
        print(f"   3. O menu flutuante ficará sempre visível")
        print()
    
    def start_listening(self):
        """Start the system tray hotkey system"""
        self.is_running = True
        self.logger.info("System tray hotkey system started")
    
    def stop_listening(self):
        """Stop the system tray hotkey system"""
        self.is_running = False
        self.logger.info("System tray hotkey system stopped")
