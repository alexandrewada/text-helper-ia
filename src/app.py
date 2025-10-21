"""
Main Application for Text Helper AI
"""
import sys
import threading
import asyncio
from typing import Optional
from .config import Config
from .logger import Logger
from .ai_client import AIClient
from .text_processor import TextProcessor
from .ui.main_window import MainWindow
from .ui.dialogs import LoadingDialog, SuccessDialog, ErrorDialog, ConfigDialog


class TextHelperAI:
    """Main application class with improved architecture and error handling"""
    
    def __init__(self):
        """Initialize the application"""
        # Initialize core components
        self.config = Config()
        self.logger = Logger(self.config)
        self.ai_client = AIClient(self.config, self.logger)
        self.text_processor = TextProcessor(self.logger)
        
        # UI components
        self.main_window: Optional[MainWindow] = None
        
        
        # Application state
        self.is_processing = False
        
        self.logger.info("Text Helper AI application initialized")
    
    def is_configured(self) -> bool:
        """Check if the application is properly configured"""
        return self.config.is_configured() and self.ai_client.is_configured()
    
    def show_config_dialog(self):
        """Show configuration dialog"""
        if self.main_window:
            parent = self.main_window.root
        else:
            parent = None
        
        def on_save():
            """Callback when configuration is saved"""
            self.ai_client._setup_clients()
            self.logger.info("Configuration updated and AI client reinitialized")
        
        config_dialog = ConfigDialog(parent, self.config, on_save, self.logger)
    
    def show_main_window(self):
        """Show the main application window"""
        self.main_window = MainWindow(
            config=self.config,
            logger=self.logger,
            on_process_text=self.process_text_from_clipboard,
            on_show_config=self.show_config_dialog
        )
        
        self.logger.info("Main window created")
        self.main_window.show()
    
    
    def process_text_from_clipboard(self, operation_type: str = 'shorten'):
        """Process text from selected text or clipboard with specified operation"""
        if self.is_processing:
            self.logger.warning("Text processing already in progress")
            return
        
        # Check if application is configured
        if not self.is_configured():
            self.logger.warning("Application not configured")
            if self.main_window:
                self.main_window.show_error(
                    "Configuração Necessária", 
                    "Por favor, configure sua chave de API do OpenAI primeiro."
                )
            return
        
        # Get text from source
        text_result = self.text_processor.get_text_from_source()
        
        if text_result[0] is None:
            self.logger.warning("No text found in selection or clipboard")
            if self.main_window:
                self.main_window.show_error(
                    "Nenhum Texto Encontrado", 
                    "Nenhum texto encontrado. Selecione um texto ou copie algo para a área de transferência primeiro."
                )
            return
        
        selected_text, text_source, has_selection = text_result
        
        # Validate text
        if not self.text_processor.validate_text(selected_text):
            self.logger.warning("Invalid text provided")
            if self.main_window:
                self.main_window.show_error(
                    "Texto Inválido", 
                    "O texto deve ter entre 3 e 10.000 caracteres."
                )
            return
        
        # Clean text
        cleaned_text = self.text_processor.clean_text(selected_text)
        
        # Get parent window for dialogs
        parent_window = None
        if self.main_window:
            parent_window = self.main_window.root
        else:
            # Create a temporary root window for dialogs
            import tkinter as tk
            parent_window = tk.Tk()
            parent_window.withdraw()
        
        # Show loading dialog
        source_text = "selecionado" if text_source == "selecionado" else "da área de transferência"
        loading_dialog = LoadingDialog(parent_window, f"Processando texto {source_text}...", self.logger)
        
        
        # Process in a separate thread to avoid blocking UI
        def process_in_thread():
            try:
                self.is_processing = True
                self.logger.info(f"Processing text with operation: {operation_type}")
                
                # Update loading status
                loading_dialog.update_status("Conectando com IA...")
                
                # Process the text
                loading_dialog.update_status("Processando com IA...")
                processed_text = self.ai_client.process_text(cleaned_text, operation_type)
                
                loading_dialog.update_status("Finalizando...")
                
                # Handle result based on configuration and source
                ui_config = self.config.get_ui_config()
                
                # If text was selected and auto-replace is enabled, replace it directly
                if has_selection and ui_config.get('auto_replace_selected', True):
                    success = self.text_processor.replace_selected_text(processed_text)
                    
                    if success:
                        self.logger.info("Text automatically replaced in selection")
                    else:
                        self.logger.warning("Replacement failed, falling back to clipboard copy")
                        self.text_processor.copy_to_clipboard(processed_text)
                # Otherwise, copy to clipboard if auto-copy is enabled
                elif ui_config.get('auto_copy', True):
                    self.text_processor.copy_to_clipboard(processed_text)
                
                # Close loading dialog
                loading_dialog.close()
                
                # Reset processing status
                self.is_processing = False
                
                # Show success dialog
                operation_names = {
                    'shorten': 'Encurtado',
                    'improve': 'Melhorado',
                    'informal': 'Informal',
                    'formal': 'Formal',
                    'spellcheck': 'Corrigido',
                    'summarize': 'Resumido',
                    'expand': 'Expandido',
                    'translate_en': 'Traduzido (EN)',
                    'translate_pt': 'Traduzido (PT)',
                    'creative': 'Criativo',
                    'technical': 'Técnico',
                    'emojify': 'Com Emojis',
                    'analyze': 'Analisado',
                    'rewrite': 'Reescrito'
                }
                
                source_info = f" (texto {text_source})" if text_source == "selecionado" else ""
                operation_name = operation_names.get(operation_type, operation_type.title())
                
                success_dialog = SuccessDialog(
                    parent_window, 
                    operation_name + source_info, 
                    cleaned_text, 
                    processed_text,
                    self.config,
                    self.logger
                )
                
                self.logger.info(f"Text successfully processed: {operation_type}")
                
            except Exception as e:
                self.logger.error(f"Error processing text: {e}")
                loading_dialog.close()
                
                # Reset processing status
                self.is_processing = False
                
                # Show error dialog
                error_dialog = ErrorDialog(parent_window, str(e), self.logger)
        
        # Start processing in thread
        thread = threading.Thread(target=process_in_thread)
        thread.daemon = True
        thread.start()
    
    def run(self, show_config: bool = False):
        """Run the application"""
        try:
            if show_config:
                self.show_config_dialog()
            else:
                self.show_main_window()
        except Exception as e:
            self.logger.error(f"Error running application: {e}")
            raise
    
    
    def cleanup(self):
        """Cleanup resources when application exits"""
        try:
            self.logger.info("Application cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def main():
    """Main function"""
    app = None
    try:
        app = TextHelperAI()
        
        # Check command line arguments
        show_config = len(sys.argv) > 1 and sys.argv[1] == '--config'
        
        app.run(show_config=show_config)
        
    except KeyboardInterrupt:
        print("\nAplicação interrompida pelo usuário")
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
    finally:
        if app:
            app.cleanup()


if __name__ == "__main__":
    main()
