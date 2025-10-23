"""
UI Dialogs for Text Helper IA
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from typing import Optional, Callable
from ..config import Config
from ..logger import Logger


class LoadingDialog:
    """Enhanced loading dialog with better animations and status updates"""
    
    def __init__(self, parent, message: str = "Processando texto...", logger: Optional[Logger] = None):
        self.parent = parent
        self.logger = logger
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Processando")
        self.dialog.geometry("350x180")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        
        # Animation control
        self._animation_running = True
        self._animation_id = None
        self._timeout_id = None
        self._is_closed = False
        
        # Center the dialog
        self._center_dialog()
        
        # Make it always on top
        self.dialog.attributes('-topmost', True)
        
        self.setup_ui(message)
        self._animate_loading()
        
        # Set grab with timeout protection
        self._safe_grab_set()
        
        # Auto-timeout after 60 seconds to prevent permanent freeze
        self._timeout_id = self.dialog.after(60000, self._auto_close_timeout)
        
        # Handle window close event
        self.dialog.protocol("WM_DELETE_WINDOW", self.close)
        
    def _center_dialog(self):
        """Center the dialog on parent window"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (180 // 2)
        self.dialog.geometry(f"350x180+{x}+{y}")
        
    def setup_ui(self, message: str):
        """Setup the loading dialog UI"""
        # Main frame with modern styling
        main_frame = tk.Frame(self.dialog, bg='#f8f9fa', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Loading icon (spinning)
        self.loading_label = tk.Label(
            main_frame, 
            text="⏳", 
            font=("Arial", 28), 
            bg='#f8f9fa',
            fg='#007bff'
        )
        self.loading_label.pack(pady=15)
        
        # Message
        message_label = tk.Label(
            main_frame, 
            text=message, 
            font=("Arial", 12, "bold"), 
            bg='#f8f9fa', 
            fg='#343a40'
        )
        message_label.pack(pady=5)
        
        # Progress bar with modern styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar",
                       background='#007bff',
                       troughcolor='#e9ecef',
                       borderwidth=0,
                       lightcolor='#007bff',
                       darkcolor='#007bff')
        
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate', 
            length=250,
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=10)
        self.progress.start(8)
        
        # Status label
        self.status_label = tk.Label(
            main_frame, 
            text="Aguarde...", 
            font=("Arial", 10), 
            bg='#f8f9fa', 
            fg='#6c757d'
        )
        self.status_label.pack(pady=5)
        
    def _animate_loading(self):
        """Animate the loading icon with more icons"""
        if not self._animation_running:
            return
            
        icons = ["⏳", "⏰", "🔄", "⚡", "✨", "🌟", "💫", "🚀"]
        if hasattr(self, 'current_icon'):
            self.current_icon = (self.current_icon + 1) % len(icons)
        else:
            self.current_icon = 0
            
        self.loading_label.config(text=icons[self.current_icon])
        
        # Only schedule next animation if still running
        if self._animation_running:
            self._animation_id = self.dialog.after(400, self._animate_loading)
        
    def update_status(self, message: str):
        """Update the status message"""
        self.status_label.config(text=message)
        self.dialog.update()
        if self.logger:
            self.logger.info(f"Loading status: {message}")
        
    def _safe_grab_set(self):
        """Safely set grab with error handling"""
        try:
            self.dialog.grab_set()
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not set grab: {e}")
    
    def _safe_grab_release(self):
        """Safely release grab with error handling"""
        try:
            self.dialog.grab_release()
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not release grab: {e}")
    
    def _auto_close_timeout(self):
        """Auto-close dialog after timeout to prevent permanent freeze"""
        if not self._is_closed:
            if self.logger:
                self.logger.warning("Loading dialog auto-closed due to timeout")
            self.close()
    
    def close(self):
        """Close the loading dialog with safe cleanup"""
        if self._is_closed:
            return
        
        self._is_closed = True
        
        # Stop animation
        self._animation_running = False
        if self._animation_id:
            try:
                self.dialog.after_cancel(self._animation_id)
            except:
                pass
            self._animation_id = None
        
        # Cancel timeout
        if self._timeout_id:
            try:
                self.dialog.after_cancel(self._timeout_id)
            except:
                pass
            self._timeout_id = None
        
        # Stop progress bar
        try:
            self.progress.stop()
        except:
            pass
        
        # Safe grab release
        self._safe_grab_release()
        
        # Remove topmost attribute
        try:
            self.dialog.attributes('-topmost', False)
        except:
            pass
        
        # Destroy dialog
        try:
            self.dialog.destroy()
        except:
            pass




class ErrorDialog:
    """Enhanced error dialog with better error handling"""
    
    def __init__(self, parent, error_message: str, logger: Optional[Logger] = None):
        self.parent = parent
        self.logger = logger
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("❌ Erro")
        self.dialog.geometry("450x250")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.attributes('-topmost', True)
        self._is_closed = False
        
        # Center the dialog
        self._center_dialog()
        
        # Safe grab set
        self._safe_grab_set()
        
        # Auto-timeout after 30 seconds
        self._timeout_id = self.dialog.after(30000, self._auto_close_timeout)
        
        self.setup_ui(error_message)
        
    def _center_dialog(self):
        """Center the dialog on parent window"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (250 // 2)
        self.dialog.geometry(f"450x250+{x}+{y}")
        
    def setup_ui(self, error_message: str):
        """Setup the error dialog UI"""
        # Main frame with modern styling
        main_frame = tk.Frame(self.dialog, bg='#f8f9fa', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Error icon
        error_label = tk.Label(
            main_frame, 
            text="❌", 
            font=("Arial", 24), 
            bg='#f8f9fa'
        )
        error_label.pack(pady=10)
        
        # Error title
        error_title = tk.Label(
            main_frame, 
            text="Erro ao processar texto:", 
            font=("Arial", 12, "bold"), 
            bg='#f8f9fa', 
            fg='#dc3545'
        )
        error_title.pack(pady=5)
        
        # Error message with scrollbar
        error_frame = tk.Frame(main_frame, bg='#f8f9fa')
        error_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        error_text = tk.Text(
            error_frame, 
            height=6, 
            wrap=tk.WORD, 
            bg='#f8d7da', 
            relief=tk.SUNKEN, 
            bd=1,
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        error_scrollbar = tk.Scrollbar(error_frame, orient="vertical", command=error_text.yview)
        error_text.configure(yscrollcommand=error_scrollbar.set)
        
        error_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        error_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        error_text.insert(tk.END, str(error_message))
        error_text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(
            main_frame, 
            text="✖️ Fechar", 
            command=self.close,
            bg='#dc3545', 
            fg='white', 
            font=("Arial", 10, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        close_btn.pack(pady=10)
        
        if self.logger:
            self.logger.error(f"Error dialog shown: {error_message}")
    
    def _safe_grab_set(self):
        """Safely set grab with error handling"""
        try:
            self.dialog.grab_set()
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not set grab: {e}")
    
    def _safe_grab_release(self):
        """Safely release grab with error handling"""
        try:
            self.dialog.grab_release()
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not release grab: {e}")
    
    def _auto_close_timeout(self):
        """Auto-close dialog after timeout to prevent permanent freeze"""
        if not self._is_closed:
            if self.logger:
                self.logger.warning("Error dialog auto-closed due to timeout")
            self.close()
    
    def close(self):
        """Close the error dialog with safe cleanup"""
        if self._is_closed:
            return
        
        self._is_closed = True
        
        # Cancel timeout
        if hasattr(self, '_timeout_id') and self._timeout_id:
            try:
                self.dialog.after_cancel(self._timeout_id)
            except:
                pass
        
        # Safe grab release
        self._safe_grab_release()
        
        # Remove topmost attribute
        try:
            self.dialog.attributes('-topmost', False)
        except:
            pass
        
        # Destroy dialog
        try:
            self.dialog.destroy()
        except:
            pass


class ConfigDialog:
    """Enhanced configuration dialog"""
    
    def __init__(self, parent, config: Config, on_save: Callable[[], None], logger: Optional[Logger] = None):
        self.parent = parent
        self.config = config
        self.on_save = on_save
        self.logger = logger
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("⚙️ Configurações - Text Helper IA")
        self.dialog.geometry("500x600")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self._is_closed = False
        
        # Center the dialog
        self._center_dialog()
        
        # Safe grab set
        self._safe_grab_set()
        
        # Auto-timeout after 5 minutes
        self._timeout_id = self.dialog.after(300000, self._auto_close_timeout)
        
        self.setup_ui()
        
    def _center_dialog(self):
        """Center the dialog on parent window"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"500x600+{x}+{y}")
        
    def setup_ui(self):
        """Setup the configuration dialog UI"""
        # Main frame with scrollable content
        main_frame = tk.Frame(self.dialog, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="⚙️ Configurações", 
            font=("Arial", 16, "bold"), 
            bg='#f8f9fa',
            fg='#343a40'
        )
        title_label.pack(pady=(0, 20))
        
        # Create notebook for different configuration sections
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # OpenAI Configuration Tab
        openai_frame = tk.Frame(notebook, bg='#f8f9fa')
        notebook.add(openai_frame, text="🤖 OpenAI")
        
        self._setup_openai_tab(openai_frame)
        
        # UI Configuration Tab
        ui_frame = tk.Frame(notebook, bg='#f8f9fa')
        notebook.add(ui_frame, text="🎨 Interface")
        
        self._setup_ui_tab(ui_frame)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#f8f9fa')
        buttons_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Save button
        save_btn = tk.Button(
            buttons_frame, 
            text="💾 Salvar Configurações", 
            command=self.save_config,
            bg='#28a745', 
            fg='white', 
            font=("Arial", 12, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2'
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn = tk.Button(
            buttons_frame, 
            text="❌ Cancelar", 
            command=self.close,
            bg='#6c757d', 
            fg='white', 
            font=("Arial", 12, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.RIGHT)
    
    def _setup_openai_tab(self, parent):
        """Setup OpenAI configuration tab"""
        # API Key
        tk.Label(parent, text="Chave de API OpenAI:", font=("Arial", 10, "bold"), bg='#f8f9fa').pack(anchor=tk.W, pady=(10, 5))
        self.api_key_var = tk.StringVar(value=self.config.get('DEFAULT', 'openai_api_key', ''))
        api_key_entry = tk.Entry(parent, textvariable=self.api_key_var, show='*', width=60, font=("Arial", 10))
        api_key_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Model selection
        tk.Label(parent, text="Modelo:", font=("Arial", 10, "bold"), bg='#f8f9fa').pack(anchor=tk.W, pady=(10, 5))
        self.model_var = tk.StringVar(value=self.config.get('DEFAULT', 'model', 'gpt-3.5-turbo'))
        model_combo = ttk.Combobox(parent, textvariable=self.model_var, values=['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo'], width=57)
        model_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Max tokens
        tk.Label(parent, text="Máximo de Tokens:", font=("Arial", 10, "bold"), bg='#f8f9fa').pack(anchor=tk.W, pady=(10, 5))
        self.tokens_var = tk.StringVar(value=self.config.get('DEFAULT', 'max_tokens', '300'))
        tokens_entry = tk.Entry(parent, textvariable=self.tokens_var, width=10, font=("Arial", 10))
        tokens_entry.pack(anchor=tk.W, pady=(0, 10))
        
        # Temperature
        tk.Label(parent, text="Temperatura (0.0 - 1.0):", font=("Arial", 10, "bold"), bg='#f8f9fa').pack(anchor=tk.W, pady=(10, 5))
        self.temperature_var = tk.StringVar(value=self.config.get('DEFAULT', 'temperature', '0.3'))
        temperature_entry = tk.Entry(parent, textvariable=self.temperature_var, width=10, font=("Arial", 10))
        temperature_entry.pack(anchor=tk.W, pady=(0, 10))
        
        # Timeout
        tk.Label(parent, text="Timeout (segundos):", font=("Arial", 10, "bold"), bg='#f8f9fa').pack(anchor=tk.W, pady=(10, 5))
        self.timeout_var = tk.StringVar(value=self.config.get('DEFAULT', 'timeout', '30'))
        timeout_entry = tk.Entry(parent, textvariable=self.timeout_var, width=10, font=("Arial", 10))
        timeout_entry.pack(anchor=tk.W, pady=(0, 10))
    
    def _setup_ui_tab(self, parent):
        """Setup UI configuration tab"""
        # Auto close delay
        tk.Label(parent, text="Fechar diálogo automaticamente após (segundos):", font=("Arial", 10, "bold"), bg='#f8f9fa').pack(anchor=tk.W, pady=(10, 5))
        self.auto_close_var = tk.StringVar(value=self.config.get('UI', 'auto_close_delay', '10'))
        auto_close_entry = tk.Entry(parent, textvariable=self.auto_close_var, width=10, font=("Arial", 10))
        auto_close_entry.pack(anchor=tk.W, pady=(0, 10))
    
    def save_config(self):
        """Save configuration"""
        try:
            # Validate inputs
            try:
                int(self.tokens_var.get())
                float(self.temperature_var.get())
                int(self.timeout_var.get())
                int(self.auto_close_var.get())
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos.")
                return
            
            # Save configuration
            self.config.set('DEFAULT', 'openai_api_key', self.api_key_var.get())
            self.config.set('DEFAULT', 'model', self.model_var.get())
            self.config.set('DEFAULT', 'max_tokens', self.tokens_var.get())
            self.config.set('DEFAULT', 'temperature', self.temperature_var.get())
            self.config.set('DEFAULT', 'timeout', self.timeout_var.get())
            self.config.set('UI', 'auto_close_delay', self.auto_close_var.get())
            
            self.config.save_config()
            self.on_save()
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            self.close()
            
            if self.logger:
                self.logger.info("Configuration saved successfully")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")
            if self.logger:
                self.logger.error(f"Error saving configuration: {e}")
    
    def _safe_grab_set(self):
        """Safely set grab with error handling"""
        try:
            self.dialog.grab_set()
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not set grab: {e}")
    
    def _safe_grab_release(self):
        """Safely release grab with error handling"""
        try:
            self.dialog.grab_release()
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not release grab: {e}")
    
    def _auto_close_timeout(self):
        """Auto-close dialog after timeout to prevent permanent freeze"""
        if not self._is_closed:
            if self.logger:
                self.logger.warning("Config dialog auto-closed due to timeout")
            self.close()
    
    def close(self):
        """Close the config dialog with safe cleanup"""
        if self._is_closed:
            return
        
        self._is_closed = True
        
        # Cancel timeout
        if hasattr(self, '_timeout_id') and self._timeout_id:
            try:
                self.dialog.after_cancel(self._timeout_id)
            except:
                pass
        
        # Safe grab release
        self._safe_grab_release()
        
        # Destroy dialog
        try:
            self.dialog.destroy()
        except:
            pass
