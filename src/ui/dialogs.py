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
        self.dialog.grab_set()
        
        # Animation control
        self._animation_running = True
        self._animation_id = None
        
        # Center the dialog
        self._center_dialog()
        
        # Make it always on top
        self.dialog.attributes('-topmost', True)
        
        self.setup_ui(message)
        self._animate_loading()
        
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
        
    def close(self):
        """Close the loading dialog"""
        # Stop animation
        self._animation_running = False
        if self._animation_id:
            self.dialog.after_cancel(self._animation_id)
            self._animation_id = None
        
        # Stop progress bar
        self.progress.stop()
        
        # Destroy dialog
        self.dialog.destroy()


class SuccessDialog:
    """Enhanced success dialog with better layout and functionality"""
    
    def __init__(self, parent, operation_name: str, original_text: str, 
                 processed_text: str, config: Config, logger: Optional[Logger] = None):
        self.parent = parent
        self.config = config
        self.logger = logger
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"✅ {operation_name}")
        
        # Make responsive - calculate size based on screen size
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        
        # Use 70% of screen width and 60% of screen height, with minimums
        dialog_width = max(700, int(screen_width * 0.7))
        dialog_height = max(500, int(screen_height * 0.6))
        
        self.dialog.geometry(f"{dialog_width}x{dialog_height}")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self._center_dialog(dialog_width, dialog_height)
        
        # Make it always on top
        self.dialog.attributes('-topmost', True)
        
        self.setup_ui(operation_name, original_text, processed_text)
        
        # Auto-close after configured delay
        try:
            auto_close_delay = self.config.get('UI', 'auto_close_delay', '10')
            delay_seconds = int(auto_close_delay)
            if delay_seconds > 0:
                self.dialog.after(delay_seconds * 1000, self.close)
        except (ValueError, TypeError):
            # If auto_close_delay is invalid, don't auto-close
            pass
        
    def _center_dialog(self, width: int, height: int):
        """Center the dialog on parent window"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self, operation_name: str, original_text: str, processed_text: str):
        """Setup the success dialog UI with side-by-side layout"""
        # Main frame with modern styling
        main_frame = tk.Frame(self.dialog, bg='#f8f9fa', relief=tk.RAISED, bd=2)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Success icon and title
        title_frame = tk.Frame(main_frame, bg='#f8f9fa')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        success_label = tk.Label(
            title_frame, 
            text="✅", 
            font=("Arial", 24), 
            bg='#f8f9fa'
        )
        success_label.pack(side=tk.LEFT)
        
        title_text = tk.Label(
            title_frame, 
            text=f"Texto {operation_name} com Sucesso!", 
            font=("Arial", 14, "bold"), 
            bg='#f8f9fa', 
            fg='#28a745'
        )
        title_text.pack(side=tk.LEFT, padx=10)
        
        # Side-by-side content frame
        content_frame = tk.Frame(main_frame, bg='#f8f9fa')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Original text
        left_frame = tk.Frame(content_frame, bg='#f8f9fa')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Original text header
        original_header = tk.Frame(left_frame, bg='#f8f9fa')
        original_header.pack(fill=tk.X, pady=(0, 5))
        
        original_icon = tk.Label(
            original_header, 
            text="📄", 
            font=("Arial", 16), 
            bg='#f8f9fa'
        )
        original_icon.pack(side=tk.LEFT)
        
        original_label = tk.Label(
            original_header, 
            text="Texto Original", 
            font=("Arial", 12, "bold"), 
            bg='#f8f9fa',
            fg='#495057'
        )
        original_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Original text widget with scrollbar
        original_text_frame = tk.Frame(left_frame, bg='#f8f9fa')
        original_text_frame.pack(fill=tk.BOTH, expand=True)
        
        original_text_widget = tk.Text(
            original_text_frame, 
            height=12, 
            wrap=tk.WORD, 
            bg='#ffffff', 
            relief=tk.SUNKEN, 
            bd=1,
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        original_scrollbar = tk.Scrollbar(original_text_frame, orient="vertical", command=original_text_widget.yview)
        original_text_widget.configure(yscrollcommand=original_scrollbar.set)
        
        original_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        original_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        original_text_widget.insert(tk.END, original_text)
        # Keep it in normal state for selection but prevent editing
        original_text_widget.config(state=tk.NORMAL)
        
        # Add click to select all functionality for original text
        def select_all_original(event):
            original_text_widget.tag_add(tk.SEL, "1.0", tk.END)
            original_text_widget.mark_set(tk.INSERT, "1.0")
            original_text_widget.see(tk.INSERT)
            return 'break'
        
        original_text_widget.bind("<Button-1>", select_all_original)
        
        # Add Ctrl+A support
        def select_all_original_ctrl_a(event):
            original_text_widget.tag_add(tk.SEL, "1.0", tk.END)
            original_text_widget.mark_set(tk.INSERT, "1.0")
            return 'break'
        
        original_text_widget.bind("<Control-a>", select_all_original_ctrl_a)
        
        # Prevent editing but allow selection
        def prevent_edit_original(event):
            if event.keysym in ['BackSpace', 'Delete', 'Return', 'space']:
                return 'break'
            if len(event.char) > 0 and ord(event.char) >= 32:
                return 'break'
        
        original_text_widget.bind("<Key>", prevent_edit_original)
        
        # Add Ctrl+C support for easy copying
        def copy_original_text(event):
            try:
                # Get selected text or all text
                selected_text = original_text_widget.get(tk.SEL_FIRST, tk.SEL_LAST) if original_text_widget.tag_ranges(tk.SEL) else original_text_widget.get("1.0", tk.END).strip()
                if selected_text:
                    # Copy to system clipboard using tkinter's built-in method
                    original_text_widget.clipboard_clear()
                    original_text_widget.clipboard_append(selected_text)
                    original_text_widget.update()
            except:
                pass
            return 'break'
        
        original_text_widget.bind("<Control-c>", copy_original_text)
        
        # Right side - Processed text
        right_frame = tk.Frame(content_frame, bg='#f8f9fa')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Processed text header
        processed_header = tk.Frame(right_frame, bg='#f8f9fa')
        processed_header.pack(fill=tk.X, pady=(0, 5))
        
        processed_icon = tk.Label(
            processed_header, 
            text="✨", 
            font=("Arial", 16), 
            bg='#f8f9fa'
        )
        processed_icon.pack(side=tk.LEFT)
        
        processed_label = tk.Label(
            processed_header, 
            text="Texto Processado", 
            font=("Arial", 12, "bold"), 
            bg='#f8f9fa',
            fg='#28a745'
        )
        processed_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Processed text widget with scrollbar
        processed_text_frame = tk.Frame(right_frame, bg='#f8f9fa')
        processed_text_frame.pack(fill=tk.BOTH, expand=True)
        
        processed_text_widget = tk.Text(
            processed_text_frame, 
            height=12, 
            wrap=tk.WORD, 
            bg='#e8f5e8', 
            relief=tk.SUNKEN, 
            bd=1,
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        processed_scrollbar = tk.Scrollbar(processed_text_frame, orient="vertical", command=processed_text_widget.yview)
        processed_text_widget.configure(yscrollcommand=processed_scrollbar.set)
        
        processed_text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        processed_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        processed_text_widget.insert(tk.END, processed_text)
        # Keep it editable and selectable
        
        # Add click to select all functionality for processed text
        def select_all_processed(event):
            processed_text_widget.tag_add(tk.SEL, "1.0", tk.END)
            processed_text_widget.mark_set(tk.INSERT, "1.0")
            processed_text_widget.see(tk.INSERT)
            return 'break'
        
        processed_text_widget.bind("<Button-1>", select_all_processed)
        
        # Add Ctrl+A support for processed text
        def select_all_processed_ctrl_a(event):
            processed_text_widget.tag_add(tk.SEL, "1.0", tk.END)
            processed_text_widget.mark_set(tk.INSERT, "1.0")
            return 'break'
        
        processed_text_widget.bind("<Control-a>", select_all_processed_ctrl_a)
        
        # Add Ctrl+C support for easy copying
        def copy_processed_text(event):
            try:
                # Get selected text or all text
                selected_text = processed_text_widget.get(tk.SEL_FIRST, tk.SEL_LAST) if processed_text_widget.tag_ranges(tk.SEL) else processed_text_widget.get("1.0", tk.END).strip()
                if selected_text:
                    # Copy to system clipboard using tkinter's built-in method
                    processed_text_widget.clipboard_clear()
                    processed_text_widget.clipboard_append(selected_text)
                    processed_text_widget.update()
            except:
                pass
            return 'break'
        
        processed_text_widget.bind("<Control-c>", copy_processed_text)
        
        # Store reference for copy functionality
        self.processed_text_widget = processed_text_widget
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='#f8f9fa')
        buttons_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Copy instructions button with modern styling
        copy_btn = tk.Button(
            buttons_frame, 
            text="📋 Como Copiar", 
            command=lambda: self.copy_to_clipboard(),
            bg='#28a745', 
            fg='white', 
            font=("Arial", 10, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save button
        save_btn = tk.Button(
            buttons_frame, 
            text="💾 Salvar", 
            command=lambda: self.save_text(),
            bg='#17a2b8', 
            fg='white', 
            font=("Arial", 10, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        close_btn = tk.Button(
            buttons_frame, 
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
        close_btn.pack(side=tk.RIGHT)
        
    def copy_to_clipboard(self, text: str = None):
        """Show copy instructions"""
        messagebox.showinfo(
            "Como Copiar Texto", 
            "Para copiar o texto:\n\n📄 Texto Original (esquerda):\n• Clique na caixa → seleciona tudo\n• Pressione Ctrl+C para copiar\n\n✨ Texto Processado (direita):\n• Clique na caixa → seleciona tudo\n• Pressione Ctrl+C para copiar\n• Ou edite antes de copiar\n\n💡 Dica: Use Ctrl+A para selecionar tudo se necessário"
        )
        if self.logger:
            self.logger.info("Copy instructions shown")
    
    def save_text(self, text: str = None):
        """Save text to file"""
        try:
            from tkinter import filedialog
            # If no text provided, get from the editable widget
            if text is None and hasattr(self, 'processed_text_widget'):
                text = self.processed_text_widget.get("1.0", tk.END).strip()
            
            if text:
                filename = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
                if filename:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(text)
                    messagebox.showinfo("Salvo!", f"Texto salvo em: {filename}")
                    if self.logger:
                        self.logger.info(f"Text saved to file: {filename}")
            else:
                messagebox.showwarning("Aviso", "Nenhum texto para salvar!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar arquivo: {e}")
            if self.logger:
                self.logger.error(f"Error saving text to file: {e}")
        
    def close(self):
        """Close the success dialog"""
        self.dialog.destroy()


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
        self.dialog.grab_set()
        self.dialog.attributes('-topmost', True)
        
        # Center the dialog
        self._center_dialog()
        
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
            command=self.dialog.destroy,
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
        self.dialog.grab_set()
        
        # Center the dialog
        self._center_dialog()
        
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
            command=self.dialog.destroy,
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
        # Auto copy
        self.auto_copy_var = tk.BooleanVar(value=self.config.get('DEFAULT', 'auto_copy', 'true').lower() == 'true')
        auto_copy_check = tk.Checkbutton(parent, text="Copiar automaticamente o resultado", variable=self.auto_copy_var, bg='#f8f9fa', font=("Arial", 10))
        auto_copy_check.pack(anchor=tk.W, pady=(10, 5))
        
        # Auto replace selected text
        self.auto_replace_var = tk.BooleanVar(value=self.config.get('DEFAULT', 'auto_replace_selected', 'true').lower() == 'true')
        auto_replace_check = tk.Checkbutton(parent, text="Substituir texto selecionado automaticamente", variable=self.auto_replace_var, bg='#f8f9fa', font=("Arial", 10))
        auto_replace_check.pack(anchor=tk.W, pady=(10, 5))
        
        # Show notifications
        self.show_notifications_var = tk.BooleanVar(value=self.config.get('DEFAULT', 'show_notifications', 'true').lower() == 'true')
        notifications_check = tk.Checkbutton(parent, text="Mostrar notificações", variable=self.show_notifications_var, bg='#f8f9fa', font=("Arial", 10))
        notifications_check.pack(anchor=tk.W, pady=(10, 5))
        
        # Auto close delay
        tk.Label(parent, text="Fechar diálogo automaticamente após (segundos):", font=("Arial", 10, "bold"), bg='#f8f9fa').pack(anchor=tk.W, pady=(10, 5))
        self.auto_close_var = tk.StringVar(value=self.config.get('UI', 'auto_close_delay', '10'))
        auto_close_entry = tk.Entry(parent, textvariable=self.auto_close_var, width=10, font=("Arial", 10))
        auto_close_entry.pack(anchor=tk.W, pady=(0, 10))
        
        # Theme selection
        tk.Label(parent, text="Tema:", font=("Arial", 10, "bold"), bg='#f8f9fa').pack(anchor=tk.W, pady=(10, 5))
        self.theme_var = tk.StringVar(value=self.config.get('DEFAULT', 'theme', 'light'))
        theme_combo = ttk.Combobox(parent, textvariable=self.theme_var, values=['light', 'dark'], width=57)
        theme_combo.pack(fill=tk.X, pady=(0, 10))
    
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
            self.config.set('DEFAULT', 'auto_copy', str(self.auto_copy_var.get()).lower())
            self.config.set('DEFAULT', 'auto_replace_selected', str(self.auto_replace_var.get()).lower())
            self.config.set('DEFAULT', 'show_notifications', str(self.show_notifications_var.get()).lower())
            self.config.set('DEFAULT', 'theme', self.theme_var.get())
            self.config.set('UI', 'auto_close_delay', self.auto_close_var.get())
            
            self.config.save_config()
            self.on_save()
            
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            self.dialog.destroy()
            
            if self.logger:
                self.logger.info("Configuration saved successfully")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")
            if self.logger:
                self.logger.error(f"Error saving configuration: {e}")
