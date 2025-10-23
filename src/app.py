"""
Main Application for Text Helper IA
"""
import sys
import threading
import tkinter as tk
from typing import Optional
from .config import Config
from .logger import Logger
from .ia_client import AIClient
from .text_processor import TextProcessor
from .ui.main_window import MainWindow
from .ui.dialogs import LoadingDialog, ErrorDialog, ConfigDialog


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
        
        self.logger.info("Text Helper IA application initialized")
    
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
            self.logger.info("Configuration updated and IA client reinitialized")
        
        config_dialog = ConfigDialog(parent, self.config, on_save, self.logger)
    
    def show_main_window(self):
        """Show the main application window"""
        self.main_window = MainWindow(
            config=self.config,
            logger=self.logger,
            on_process_text=self.process_text_from_clipboard,
            on_show_config=self.show_config_dialog
        )
        
        # No global event handling needed - let system handle CTRL+C naturally
        
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
        
        # For now, we'll use a simple text input dialog instead of clipboard
        # This prevents any system freezing issues
        import tkinter as tk
        from tkinter import simpledialog
        
        # Get parent window for dialog
        parent_window = None
        if self.main_window:
            parent_window = self.main_window.root
        else:
            parent_window = tk.Tk()
            parent_window.withdraw()
        
        # Create simple input dialog with auto-paste (more stable)
        selected_text = self._show_simple_input_dialog(parent_window)
        
        self.logger.info(f"Text received from dialog: '{selected_text[:100] if selected_text else 'None'}{'...' if selected_text and len(selected_text) > 100 else ''}'")
        
        if not selected_text or not selected_text.strip():
            self.logger.warning("No text provided by user")
            if self.main_window:
                self.main_window.show_error(
                    "Nenhum Texto Fornecido", 
                    "Nenhum texto foi fornecido. Por favor, digite ou cole o texto que deseja processar."
                )
            return
        
        text_source = "manual"
        has_selection = False
        
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
        
        # Store reference to root window for thread-safe UI updates
        root_window = parent_window
        
        # Show loading dialog
        source_text = "selecionado" if text_source == "selecionado" else "da área de transferência"
        loading_dialog = LoadingDialog(parent_window, f"Processando texto {source_text}...", self.logger)
        
        
        # Process in a separate thread to avoid blocking UI
        def process_in_thread():
            try:
                self.is_processing = True
                self.logger.info(f"Processing text with operation: {operation_type}")
                
                # Update loading status (thread-safe)
                def update_loading_status(message):
                    try:
                        if not loading_dialog._is_closed:
                            loading_dialog.update_status(message)
                    except Exception as e:
                        self.logger.warning(f"Could not update loading status: {e}")
                
                # Schedule UI updates on main thread
                root_window.after(0, lambda: update_loading_status("Conectando com IA..."))
                
                # Process the text
                root_window.after(0, lambda: update_loading_status("Processando com IA..."))
                processed_text = self.ai_client.process_text(cleaned_text, operation_type)
                
                root_window.after(0, lambda: update_loading_status("Finalizando..."))
                
                # Handle result - show in dialog only (no clipboard operations to prevent freezing)
                ui_config = self.config.get_ui_config()
                
                # No clipboard operations to prevent system freezing
                self.logger.info("Text processed successfully (no clipboard operations to prevent freezing)")
                
                # Close loading dialog (thread-safe)
                def close_loading_safe():
                    try:
                        if not loading_dialog._is_closed:
                            loading_dialog.close()
                    except Exception as e:
                        self.logger.warning(f"Could not close loading dialog: {e}")
                
                root_window.after(0, close_loading_safe)
                
                # Show result in system notification (thread-safe)
                def show_notification_safe():
                    try:
                        if self.main_window:
                            self.main_window.set_result(processed_text)
                            self._show_result_notification(processed_text, operation_type)
                    except Exception as e:
                        self.logger.error(f"Error showing notification: {e}")
                
                root_window.after(0, show_notification_safe)
                
                # Reset processing status
                self.is_processing = False
                
                self.logger.info(f"Text successfully processed: {operation_type}")
                
            except Exception as e:
                self.logger.error(f"Error processing text: {e}")
                
                # Close loading dialog (thread-safe)
                def close_loading_on_error():
                    try:
                        if not loading_dialog._is_closed:
                            loading_dialog.close()
                    except Exception as e:
                        self.logger.warning(f"Could not close loading dialog on error: {e}")
                
                root_window.after(0, close_loading_on_error)
                
                # Reset processing status
                self.is_processing = False
                
                # Show error dialog (thread-safe)
                def show_error_safe():
                    try:
                        error_dialog = ErrorDialog(parent_window, str(e), self.logger)
                    except Exception as e2:
                        self.logger.error(f"Error showing error dialog: {e2}")
                
                root_window.after(0, show_error_safe)
        
        # Start processing in thread with proper cleanup
        thread = threading.Thread(target=process_in_thread, name=f"TextProcessor-{operation_type}")
        thread.daemon = True
        thread.start()
        
        # Store thread reference for potential cleanup
        if not hasattr(self, '_processing_threads'):
            self._processing_threads = []
        self._processing_threads.append(thread)
    
    
    def _show_simple_input_dialog(self, parent):
        """Show improved simple input dialog with auto-paste functionality"""
        import tkinter as tk
        from tkinter import simpledialog
        
        # Create a custom dialog that's more stable than the complex one
        dialog = tk.Toplevel(parent)
        dialog.title("Texto para Processar")
        dialog.geometry("500x350")
        dialog.resizable(True, True)
        dialog.transient(parent)
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (350 // 2)
        dialog.geometry(f"500x350+{x}+{y}")
        
        # Make it always on top
        dialog.attributes('-topmost', True)
        
        # Don't use grab_set to prevent clipboard conflicts
        # dialog.grab_set()  # Removed to prevent clipboard conflicts
        
        # Main frame
        main_frame = tk.Frame(dialog, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="📝 Digite ou cole o texto que deseja processar:", 
            font=("Arial", 12, "bold"), 
            bg='#f8f9fa',
            fg='#343a40'
        )
        title_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Text widget with scrollbar
        text_frame = tk.Frame(main_frame, bg='#f8f9fa')
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        text_widget = tk.Text(
            text_frame, 
            height=12, 
            wrap=tk.WORD, 
            bg='#ffffff', 
            relief=tk.SUNKEN, 
            bd=1,
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Safe auto-paste clipboard content with conflict prevention
        def safe_auto_paste():
            try:
                # Small delay to ensure dialog is fully initialized
                import time
                time.sleep(0.05)
                
                # Try to get clipboard content safely
                import pyperclip
                clipboard_content = pyperclip.paste()
                
                if clipboard_content and clipboard_content.strip():
                    # Only paste if text widget is empty and ready
                    current_content = text_widget.get("1.0", tk.END).strip()
                    if not current_content:
                        text_widget.insert(tk.END, clipboard_content.strip())
                        self.logger.info("Auto-pasted clipboard content safely")
                        
                        # Auto-click process button after paste for better productivity
                        dialog.after(100, lambda: self._close_simple_dialog(dialog, text_widget))
                    else:
                        self.logger.info("Text widget not empty, skipping auto-paste")
                else:
                    self.logger.info("Clipboard empty, no auto-paste")
                    
            except Exception as e:
                self.logger.warning(f"Could not auto-paste clipboard safely: {e}")
        
        # Schedule auto-paste with delay to prevent conflicts
        dialog.after(50, safe_auto_paste)
        
        # Focus on text widget
        text_widget.focus_set()
        
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#f8f9fa')
        buttons_frame.pack(fill=tk.X)
        
        # Clear button
        clear_btn = tk.Button(
            buttons_frame, 
            text="🗑️ Limpar", 
            command=lambda: self._clear_text_widget(text_widget),
            bg='#6c757d', 
            fg='white', 
            font=("Arial", 10, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # OK button
        ok_btn = tk.Button(
            buttons_frame, 
            text="✅ Processar", 
            command=lambda: self._close_simple_dialog(dialog, text_widget),
            bg='#28a745', 
            fg='white', 
            font=("Arial", 10, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        ok_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Cancel button
        cancel_btn = tk.Button(
            buttons_frame, 
            text="❌ Cancelar", 
            command=lambda: self._close_simple_dialog(dialog, None),
            bg='#dc3545', 
            fg='white', 
            font=("Arial", 10, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.RIGHT)
        
        # Bind Enter key to OK
        def on_enter(event):
            self._close_simple_dialog(dialog, text_widget)
        
        text_widget.bind("<Control-Return>", on_enter)
        
        # Handle window close event
        def on_closing():
            self._simple_dialog_result = None
            dialog.destroy()
        
        dialog.protocol("WM_DELETE_WINDOW", on_closing)
        
        # No focus management needed - let system handle naturally
        
        # Store result
        self._simple_dialog_result = None
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return self._simple_dialog_result
    
    def _paste_clipboard(self, text_widget):
        """Paste clipboard content into text widget"""
        try:
            import tkinter as tk
            import pyperclip
            clipboard_content = pyperclip.paste()
            if clipboard_content:
                text_widget.delete("1.0", tk.END)
                text_widget.insert(tk.END, clipboard_content.strip())
                self.logger.info("Manually pasted clipboard content")
        except Exception as e:
            self.logger.error(f"Error pasting clipboard: {e}")
    
    def _clear_text_widget(self, text_widget):
        """Clear text widget content"""
        try:
            import tkinter as tk
            text_widget.delete("1.0", tk.END)
            text_widget.focus_set()
            self.logger.info("Text widget cleared")
        except Exception as e:
            self.logger.error(f"Error clearing text widget: {e}")
    
    def _close_simple_dialog(self, dialog, text_widget):
        """Close simple dialog and return result"""
        try:
            if text_widget:
                # Get all text content
                content = text_widget.get("1.0", "end-1c")
                self._simple_dialog_result = content.strip() if content else None
                self.logger.info(f"Simple dialog result: '{self._simple_dialog_result[:50]}{'...' if len(self._simple_dialog_result) > 50 else ''}'")
            else:
                self._simple_dialog_result = None
                self.logger.info("Simple dialog cancelled")
        except Exception as e:
            self.logger.error(f"Error getting text from simple dialog: {e}")
            self._simple_dialog_result = None
        finally:
            dialog.destroy()
    
    def _close_dialog(self, dialog, text_widget):
        """Close dialog and return result with safe cleanup"""
        try:
            if text_widget:
                # Get all text content
                content = text_widget.get("1.0", "end-1c")
                self._dialog_result = content.strip() if content else None
                self.logger.info(f"Dialog result: '{self._dialog_result[:50]}{'...' if len(self._dialog_result) > 50 else ''}'")
            else:
                self._dialog_result = None
                self.logger.info("Dialog cancelled")
        except Exception as e:
            self.logger.error(f"Error getting text from dialog: {e}")
            self._dialog_result = None
        finally:
            # Ensure proper cleanup to prevent dialog freeze
            try:
                dialog.grab_release()  # Release the grab before destroying
            except:
                pass  # Ignore errors during cleanup
            try:
                dialog.attributes('-topmost', False)  # Remove topmost attribute
            except:
                pass  # Ignore errors during cleanup
            try:
                dialog.destroy()
            except:
                pass  # Ignore errors during cleanup
    
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
    
    
    
    def _show_result_notification(self, processed_text, operation_type):
        """Show result in system notification with copy button"""
        try:
            # Import plyer for system notifications
            from plyer import notification
            
            # Truncate text for notification (max 200 chars)
            display_text = processed_text[:200] + "..." if len(processed_text) > 200 else processed_text
            
            # Operation names in Portuguese
            operation_names = {
                'shorten': 'Encurtado',
                'improve': 'Melhorado', 
                'informal': 'Informal',
                'formal': 'Formal',
                'spellcheck': 'Corrigido',
                'summarize': 'Resumido',
                'translate_en': 'Traduzido para Inglês',
                'emojify': 'Com Emojis'
            }
            
            operation_name = operation_names.get(operation_type, operation_type)
            
            # Copy to clipboard automatically
            import pyperclip
            pyperclip.copy(processed_text)
            
            # Minimize main window for better productivity (no dialog needed)
            if self.main_window:
                self.main_window.root.iconify()  # Minimize the window
                self.main_window.update_status(f"Texto {operation_name}! Resultado copiado para clipboard.", '#28a745')
                
            
            self.logger.info(f"Result notification shown for operation: {operation_type}")
            
        except ImportError:
            # Fallback if plyer is not available
            self.logger.warning("Plyer not available, using fallback notification")
            self._show_fallback_notification(processed_text, operation_type)
        except Exception as e:
            self.logger.error(f"Error showing notification: {e}")
            self._show_fallback_notification(processed_text, operation_type)
    
    def _show_fallback_notification(self, processed_text, operation_type):
        """Fallback notification using tkinter messagebox"""
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            # Truncate text for messagebox
            display_text = processed_text[:500] + "..." if len(processed_text) > 500 else processed_text
            
            # Operation names in Portuguese
            operation_names = {
                'shorten': 'Encurtado',
                'improve': 'Melhorado', 
                'informal': 'Informal',
                'formal': 'Formal',
                'spellcheck': 'Corrigido',
                'summarize': 'Resumido',
                'translate_en': 'Traduzido para Inglês',
                'emojify': 'Com Emojis'
            }
            
            operation_name = operation_names.get(operation_type, operation_type)
            
            # Copy to clipboard
            import pyperclip
            pyperclip.copy(processed_text)
            
            # Minimize main window for better productivity (no dialog needed)
            if self.main_window:
                self.main_window.root.iconify()  # Minimize the window
                self.main_window.update_status(f"Texto {operation_name}! Resultado copiado para clipboard.", '#28a745')
            
            self.logger.info(f"Fallback notification shown for operation: {operation_type}")
            
        except Exception as e:
            self.logger.error(f"Error showing fallback notification: {e}")
            # Last resort - just update status
            if self.main_window:
                self.main_window.update_status(f"Texto processado! Verifique a janela principal.", '#28a745')

    def cleanup(self):
        """Cleanup resources when application exits"""
        try:
            # Stop any processing
            self.is_processing = False
            
            # Close main window if it exists
            if self.main_window:
                try:
                    self.main_window.close()
                except Exception as e:
                    self.logger.warning(f"Error closing main window: {e}")
            
            # Wait for threads to finish (with timeout)
            if hasattr(self, '_processing_threads'):
                for thread in self._processing_threads:
                    if thread.is_alive():
                        thread.join(timeout=2.0)  # Wait max 2 seconds
                        if thread.is_alive():
                            self.logger.warning(f"Thread {thread.name} did not finish in time")
            
            # Force cleanup of any remaining tkinter windows
            try:
                import tkinter as tk
                for widget in tk._default_root.winfo_children() if tk._default_root else []:
                    try:
                        widget.destroy()
                    except:
                        pass
            except:
                pass
            
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
