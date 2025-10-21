"""
Main Window for Text Helper IA
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
from ..config import Config
from ..logger import Logger


class MainWindow:
    """Enhanced main window with modern styling and better organization"""
    
    def __init__(self, config: Config, logger: Logger, 
                 on_process_text: Callable[[str], None], on_show_config: Callable[[], None]):
        self.config = config
        self.logger = logger
        self.on_process_text = on_process_text
        self.on_show_config = on_show_config
        
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        
    def setup_window(self):
        """Setup main window properties"""
        ui_config = self.config.get_ui_config()
        
        self.root.title("Text Helper IA")
        self.root.geometry("700x600")
        self.root.configure(bg='#f8f9fa')
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 350
        y = (self.root.winfo_screenheight() // 2) - 300
        self.root.geometry(f"+{x}+{y}")
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass  # Icon not found, continue without it
    
    def setup_ui(self):
        """Setup the main window UI"""
        # Main container with padding
        main_container = tk.Frame(self.root, bg='#f8f9fa')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self._create_header(main_container)
        
        # Quick access buttons
        self._create_quick_access(main_container)
        
        # Control buttons
        self._create_controls(main_container)
        
        # Result section
        self._create_result_section(main_container)
        
        # Status section
        self._create_status(main_container)
        
    def _create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg='#f8f9fa')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title with icon
        title_frame = tk.Frame(header_frame, bg='#f8f9fa')
        title_frame.pack()
        
        title_icon = tk.Label(
            title_frame, 
            text="🤖", 
            font=("Arial", 24), 
            bg='#f8f9fa'
        )
        title_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = tk.Label(
            title_frame, 
            text="Text Helper IA", 
            font=("Arial", 20, "bold"), 
            bg='#f8f9fa',
            fg='#343a40'
        )
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame, 
            text="Processamento de texto com IA", 
            font=("Arial", 12), 
            bg='#f8f9fa',
            fg='#6c757d'
        )
        subtitle_label.pack(pady=(5, 0))
    
    
    def _create_quick_access(self, parent):
        """Create quick access buttons section"""
        quick_frame = tk.Frame(parent, bg='#f8f9fa')
        quick_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Quick access title
        quick_title = tk.Label(
            quick_frame, 
            text="⚡ Ferramentas", 
            font=("Arial", 12, "bold"), 
            bg='#f8f9fa',
            fg='#343a40'
        )
        quick_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Button rows
        button_rows = [
            [
                ('📝 Encurtar', 'shorten', '#007bff'),
                ('✨ Melhorar', 'improve', '#28a745'),
                ('✅ Corrigir', 'spellcheck', '#28a745'),
                ('📋 Resumir', 'summarize', '#17a2b8')
            ],
            [
                ('😊 Informal', 'informal', '#ffc107'),
                ('👔 Formal', 'formal', '#fd7e14'),
                ('🇺🇸 Inglês', 'translate_en', '#dc3545'),
                ('😀 Emojis', 'emojify', '#ffc107')
            ]
        ]
        
        for row_buttons in button_rows:
            row_frame = tk.Frame(quick_frame, bg='#f8f9fa')
            row_frame.pack(fill=tk.X, pady=2)
            
            for text, operation, color in row_buttons:
                btn = tk.Button(
                    row_frame, 
                    text=text, 
                    command=lambda op=operation: self.on_process_text(op),
                    bg=color, 
                    fg='white',
                    font=("Arial", 9, "bold"),
                    relief=tk.FLAT, 
                    bd=0,
                    padx=15,
                    pady=8,
                    cursor='hand2',
                    activebackground=self._darken_color(color),
                    activeforeground='white'
                )
                btn.pack(side=tk.LEFT, padx=2, fill=tk.X, expand=True)
                
                # Add hover effects
                self._add_hover_effect(btn, color)
    
    def _create_controls(self, parent):
        """Create control buttons section"""
        controls_frame = tk.Frame(parent, bg='#f8f9fa')
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Main control buttons
        main_controls = tk.Frame(controls_frame, bg='#f8f9fa')
        main_controls.pack()
        
        
        # Configuration button
        config_btn = tk.Button(
            main_controls, 
            text="⚙️ Configurações", 
            command=self.on_show_config, 
            bg="#6c757d", 
            fg='white',
            font=("Arial", 12, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2',
            activebackground='#545b62',
            activeforeground='white'
        )
        config_btn.pack(side=tk.LEFT)
        
        # Add hover effects
        self._add_hover_effect(config_btn, "#6c757d")
    
    def _create_result_section(self, parent):
        """Create result section"""
        self.result_frame = tk.Frame(parent, bg='#f8f9fa')
        # Don't pack initially - will be shown when there's a result
        
        # Result title
        result_title = tk.Label(
            self.result_frame, 
            text="✨ Resultado", 
            font=("Arial", 12, "bold"), 
            bg='#f8f9fa',
            fg='#343a40'
        )
        result_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Result text widget with scrollbar
        text_frame = tk.Frame(self.result_frame, bg='#f8f9fa')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(
            text_frame, 
            height=8, 
            wrap=tk.WORD, 
            bg='#e8f5e8', 
            relief=tk.SUNKEN, 
            bd=1,
            font=("Arial", 10),
            padx=10,
            pady=10,
            state=tk.NORMAL
        )
        result_scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Result buttons frame
        result_buttons_frame = tk.Frame(self.result_frame, bg='#f8f9fa')
        result_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Select button
        copy_btn = tk.Button(
            result_buttons_frame, 
            text="📋 Selecionar", 
            command=self.copy_result,
            bg='#28a745', 
            fg='white', 
            font=("Arial", 9, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear button
        clear_btn = tk.Button(
            result_buttons_frame, 
            text="🗑️ Limpar", 
            command=self.clear_result,
            bg='#6c757d', 
            fg='white', 
            font=("Arial", 9, "bold"),
            relief=tk.FLAT, 
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        clear_btn.pack(side=tk.LEFT)
        
        # Add hover effects
        self._add_hover_effect(copy_btn, "#28a745")
        self._add_hover_effect(clear_btn, "#6c757d")
        
        # Add click to select all functionality for result text
        def select_all_result(event):
            self.result_text.tag_add(tk.SEL, "1.0", tk.END)
            self.result_text.mark_set(tk.INSERT, "1.0")
            self.result_text.see(tk.INSERT)
            return 'break'
        
        self.result_text.bind("<Button-1>", select_all_result)
        
        # Add Ctrl+A support for result text
        def select_all_result_ctrl_a(event):
            self.result_text.tag_add(tk.SEL, "1.0", tk.END)
            self.result_text.mark_set(tk.INSERT, "1.0")
            return 'break'
        
        self.result_text.bind("<Control-a>", select_all_result_ctrl_a)
        
        # Add Ctrl+C support for easy copying (simplified)
        def copy_result_text(event):
            try:
                # Let tkinter handle the copy operation naturally
                # Just update status to show it worked
                if hasattr(self, 'status_text'):
                    self.status_text.config(text="Status: Texto copiado!", fg='#28a745')
            except Exception as e:
                self.logger.error(f"Error in Ctrl+C copy: {e}")
            # Don't return 'break' to allow normal copy behavior
        
        self.result_text.bind("<Control-c>", copy_result_text)
    
    def _create_status(self, parent):
        """Create status section"""
        status_frame = tk.Frame(parent, bg='#f8f9fa')
        status_frame.pack(fill=tk.X)
        
        # Status indicator
        status_indicator = tk.Label(
            status_frame, 
            text="●", 
            font=("Arial", 12), 
            bg='#f8f9fa',
            fg='#28a745'
        )
        status_indicator.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status text
        self.status_text = tk.Label(
            status_frame, 
            text="Status: Pronto para usar", 
            font=("Arial", 10), 
            bg='#f8f9fa',
            fg='#28a745'
        )
        self.status_text.pack(side=tk.LEFT)
    
    def _darken_color(self, color: str) -> str:
        """Darken a hex color for hover effect"""
        color_map = {
            '#007bff': '#0056b3',
            '#28a745': '#1e7e34',
            '#17a2b8': '#117a8b',
            '#6f42c1': '#5a32a3',
            '#ffc107': '#e0a800',
            '#fd7e14': '#e55a00',
            '#e83e8c': '#d91a72',
            '#6c757d': '#545b62',
            '#dc3545': '#c82333',
            '#20c997': '#1aa179'
        }
        return color_map.get(color, color)
    
    def _add_hover_effect(self, button: tk.Button, original_color: str):
        """Add hover effect to button"""
        def on_enter(event):
            button.config(bg=self._darken_color(original_color))
        
        def on_leave(event):
            button.config(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def show(self):
        """Show the main window"""
        self.logger.info("Main window shown")
        self.root.mainloop()
    
    def close(self):
        """Close the main window"""
        self.logger.info("Main window closed")
        self.root.destroy()
    
    def update_status(self, message: str, color: str = '#28a745'):
        """Update status message"""
        try:
            if hasattr(self, 'status_text'):
                self.status_text.config(text=f"Status: {message}", fg=color)
            self.logger.info(f"Status update: {message}")
        except Exception as e:
            self.logger.error(f"Error updating status: {e}")
    
    def show_error(self, title: str, message: str):
        """Show error message"""
        messagebox.showerror(title, message)
        self.logger.error(f"Error shown: {title} - {message}")
    
    def show_info(self, title: str, message: str):
        """Show info message"""
        messagebox.showinfo(title, message)
        self.logger.info(f"Info shown: {title} - {message}")
    
    def set_result(self, text: str):
        """Set result text"""
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.show_result_section()
        self.logger.info("Result text updated")
    
    def copy_result(self):
        """Select all text for easy copying"""
        try:
            text = self.result_text.get("1.0", tk.END).strip()
            if text:
                # Select all text instead of copying to clipboard
                self.result_text.tag_add(tk.SEL, "1.0", tk.END)
                self.result_text.mark_set(tk.INSERT, "1.0")
                self.result_text.see(tk.INSERT)
                
                # Update status
                if hasattr(self, 'status_text'):
                    self.status_text.config(text="Status: Texto selecionado! Pressione Ctrl+C para copiar", fg='#28a745')
                
                self.logger.info("Result text selected for copying")
            else:
                if hasattr(self, 'status_text'):
                    self.status_text.config(text="Status: Nenhum resultado para copiar!", fg='#ffc107')
                self.logger.warning("No result text to copy")
        except Exception as e:
            if hasattr(self, 'status_text'):
                self.status_text.config(text=f"Status: Erro ao selecionar texto: {e}", fg='#dc3545')
            self.logger.error(f"Error selecting result text: {e}")
    
    def clear_result(self):
        """Clear result text"""
        self.result_text.delete("1.0", tk.END)
        self.hide_result_section()
        self.logger.info("Result text cleared")
    
    def show_result_section(self):
        """Show result section"""
        if hasattr(self, 'result_frame'):
            self.result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            self.logger.info("Result section shown")
    
    def hide_result_section(self):
        """Hide result section"""
        if hasattr(self, 'result_frame'):
            self.result_frame.pack_forget()
            self.logger.info("Result section hidden")
