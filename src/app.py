"""
Main Application for Text Helper IA
"""
import sys
import threading
import asyncio
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
                
                # Handle result - show in dialog only (no clipboard operations to prevent freezing)
                ui_config = self.config.get_ui_config()
                
                # No clipboard operations to prevent system freezing
                self.logger.info("Text processed successfully (no clipboard operations to prevent freezing)")
                
                # Close loading dialog
                loading_dialog.close()
                
                # Set result in main window
                if self.main_window:
                    self.main_window.set_result(processed_text)
                    self.main_window.show_info(
                        "Processamento Concluído", 
                        f"Texto {operation_type} processado com sucesso!"
                    )
                
                # Reset processing status
                self.is_processing = False
                
                self.logger.info(f"Text successfully processed: {operation_type}")
                
            except Exception as e:
                self.logger.error(f"Error processing text: {e}")
                loading_dialog.close()
                
                # Reset processing status
                self.is_processing = False
                
                # Show error dialog
                error_dialog = ErrorDialog(parent_window, str(e), self.logger)
        
        # Start processing in thread with proper cleanup
        thread = threading.Thread(target=process_in_thread, name=f"TextProcessor-{operation_type}")
        thread.daemon = True
        thread.start()
        
        # Store thread reference for potential cleanup
        if not hasattr(self, '_processing_threads'):
            self._processing_threads = []
        self._processing_threads.append(thread)
    
    def _show_text_input_dialog(self, parent):
        """Show custom text input dialog with auto-paste functionality"""
        import tkinter as tk
        
        # Create dialog window
        dialog = tk.Toplevel(parent)
        dialog.title("Texto para Processar")
        dialog.geometry("600x400")
        dialog.resizable(True, True)
        dialog.transient(parent)
        
        # Ensure parent window is not withdrawn when creating dialog
        if hasattr(parent, 'deiconify'):
            parent.deiconify()
        
        # Center the dialog first
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"600x400+{x}+{y}")
        
        # Make it always on top
        dialog.attributes('-topmost', True)
        
        # Set grab after positioning
        dialog.grab_set()
        
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
            height=15, 
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
        
        # Auto-paste clipboard content
        try:
            import pyperclip
            clipboard_content = pyperclip.paste()
            if clipboard_content and clipboard_content.strip():
                text_widget.insert(tk.END, clipboard_content.strip())
                self.logger.info("Auto-pasted clipboard content")
        except Exception as e:
            self.logger.warning(f"Could not auto-paste clipboard: {e}")
        
        # Focus on text widget
        text_widget.focus_set()
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#f8f9fa')
        buttons_frame.pack(fill=tk.X)
        
        # Paste button
        paste_btn = tk.Button(
            buttons_frame, 
            text="📋 Colar do Clipboard", 
            command=lambda: self._paste_clipboard(text_widget),
            bg='#17a2b8', 
            fg='white', 
            font=("Arial", 10, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        paste_btn.pack(side=tk.LEFT, padx=(0, 10))
        
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
            command=lambda: self._close_dialog(dialog, text_widget),
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
            command=lambda: self._close_dialog(dialog, None),
            bg='#6c757d', 
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
            self._close_dialog(dialog, text_widget)
        
        text_widget.bind("<Control-Return>", on_enter)
        
        # Handle window close event
        def on_closing():
            self._dialog_result = None
            # Ensure proper cleanup to prevent dialog freeze
            try:
                dialog.grab_release()  # Release the grab before destroying
                dialog.attributes('-topmost', False)  # Remove topmost attribute
            except:
                pass  # Ignore errors during cleanup
            dialog.destroy()
        
        dialog.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Store result
        self._dialog_result = None
        
        # Wait for dialog to close with proper error handling
        try:
            dialog.wait_window()
        except Exception as e:
            self.logger.error(f"Error waiting for dialog: {e}")
            # Force cleanup if wait_window fails
            try:
                dialog.grab_release()
                dialog.attributes('-topmost', False)
                dialog.destroy()
            except:
                pass
        
        return self._dialog_result
    
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
        
        # Auto-paste clipboard content
        try:
            import pyperclip
            clipboard_content = pyperclip.paste()
            if clipboard_content and clipboard_content.strip():
                text_widget.insert(tk.END, clipboard_content.strip())
                self.logger.info("Auto-pasted clipboard content")
        except Exception as e:
            self.logger.warning(f"Could not auto-paste clipboard: {e}")
        
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
        """Close dialog and return result"""
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
                dialog.attributes('-topmost', False)  # Remove topmost attribute
            except:
                pass  # Ignore errors during cleanup
            dialog.destroy()
    
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
            # Stop any processing
            self.is_processing = False
            
            # Wait for threads to finish (with timeout)
            if hasattr(self, '_processing_threads'):
                for thread in self._processing_threads:
                    if thread.is_alive():
                        thread.join(timeout=2.0)  # Wait max 2 seconds
                        if thread.is_alive():
                            self.logger.warning(f"Thread {thread.name} did not finish in time")
            
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
