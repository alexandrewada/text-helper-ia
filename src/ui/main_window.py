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
        self.root.geometry("520x320")
        self.root.configure(bg='#f0f2f5')
        self.root.resizable(False, False)
        
        # Modern window styling
        self.root.attributes('-alpha', 0.98)  # Slight transparency
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - 260
        y = (self.root.winfo_screenheight() // 2) - 160
        self.root.geometry(f"+{x}+{y}")
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass  # Icon not found, continue without it
    
    def setup_ui(self):
        """Setup the main window UI"""
        # Main container with modern styling
        main_container = tk.Frame(self.root, bg='#f0f2f5')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create modern card container
        card_frame = tk.Frame(main_container, bg='#ffffff', relief=tk.FLAT, bd=0)
        card_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add subtle shadow effect
        shadow_frame = tk.Frame(main_container, bg='#e1e5e9', height=2)
        shadow_frame.place(in_=card_frame, x=2, y=2, relwidth=1, relheight=1)
        card_frame.lift()
        
        # Inner container with padding
        inner_container = tk.Frame(card_frame, bg='#ffffff')
        inner_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self._create_header(inner_container)
        
        # Compact organized sections
        self._create_compact_sections(inner_container)
        
        # Status section
        self._create_status(inner_container)
        
    def _create_header(self, parent):
        """Create header section"""
        header_frame = tk.Frame(parent, bg='#ffffff')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title with modern styling
        title_frame = tk.Frame(header_frame, bg='#ffffff')
        title_frame.pack()
        
        # Modern icon with background
        icon_bg = tk.Frame(title_frame, bg='#667eea', width=40, height=40, relief=tk.FLAT, bd=0)
        icon_bg.pack(side=tk.LEFT, padx=(0, 12))
        icon_bg.pack_propagate(False)
        
        title_icon = tk.Label(
            icon_bg, 
            text="🤖", 
            font=("Arial", 16), 
            bg='#667eea',
            fg='white'
        )
        title_icon.pack(expand=True)
        
        # Title with gradient-like effect
        title_label = tk.Label(
            title_frame, 
            text="Text Helper IA", 
            font=("Segoe UI", 18, "bold"), 
            bg='#ffffff',
            fg='#2c3e50'
        )
        title_label.pack(side=tk.LEFT)
        
        # Subtitle with modern styling
        subtitle_label = tk.Label(
            header_frame, 
            text="Processamento inteligente de texto", 
            font=("Segoe UI", 10), 
            bg='#ffffff',
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=(8, 0))
    
    def _create_compact_sections(self, parent):
        """Create compact organized sections"""
        # Main sections container
        sections_frame = tk.Frame(parent, bg='#ffffff')
        sections_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Edição section
        self._create_edicao_section(sections_frame)
        
        # Estilo section
        self._create_estilo_section(sections_frame)
        
        # Expressão section
        self._create_expressao_section(sections_frame)
        
        # Modern separator
        separator_frame = tk.Frame(sections_frame, bg='#ffffff', height=20)
        separator_frame.pack(fill=tk.X)
        
        separator_line = tk.Frame(separator_frame, height=1, bg='#e8ecf0')
        separator_line.pack(fill=tk.X, pady=10)
        
        # Configurações button
        self._create_config_button(sections_frame)
    
    def _create_edicao_section(self, parent):
        """Create Edição section"""
        edicao_frame = tk.Frame(parent, bg='#ffffff')
        edicao_frame.pack(fill=tk.X, pady=3)
        
        # Section label with modern styling
        label = tk.Label(
            edicao_frame,
            text="✍️ Edição:",
            font=("Segoe UI", 11, "bold"),
            bg='#ffffff',
            fg='#2c3e50'
        )
        label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Buttons with modern design
        buttons = [
            ('Encurtar', 'shorten', '#667eea'),
            ('Melhorar', 'improve', '#56ab2f'),
            ('Corrigir', 'spellcheck', '#56ab2f'),
            ('Resumir', 'summarize', '#36d1dc')
        ]
        
        for text, operation, color in buttons:
            btn = self._create_modern_button(
                edicao_frame,
                text=text,
                command=lambda op=operation: self.on_process_text(op),
                color=color
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def _create_estilo_section(self, parent):
        """Create Estilo section"""
        estilo_frame = tk.Frame(parent, bg='#ffffff')
        estilo_frame.pack(fill=tk.X, pady=3)
        
        # Section label with modern styling
        label = tk.Label(
            estilo_frame,
            text="💬 Estilo:",
            font=("Segoe UI", 11, "bold"),
            bg='#ffffff',
            fg='#2c3e50'
        )
        label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Buttons with modern design
        buttons = [
            ('Informal', 'informal', '#f093fb'),
            ('Formal', 'formal', '#f5576c')
        ]
        
        for text, operation, color in buttons:
            btn = self._create_modern_button(
                estilo_frame,
                text=text,
                command=lambda op=operation: self.on_process_text(op),
                color=color
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def _create_expressao_section(self, parent):
        """Create Expressão section"""
        expressao_frame = tk.Frame(parent, bg='#ffffff')
        expressao_frame.pack(fill=tk.X, pady=3)
        
        # Section label with modern styling
        label = tk.Label(
            expressao_frame,
            text="🌐 Expressão:",
            font=("Segoe UI", 11, "bold"),
            bg='#ffffff',
            fg='#2c3e50'
        )
        label.pack(side=tk.LEFT, padx=(0, 8))
        
        # Buttons with modern design
        buttons = [
            ('Inglês', 'translate_en', '#ff6b6b'),
            ('Emojis', 'emojify', '#feca57')
        ]
        
        for text, operation, color in buttons:
            btn = self._create_modern_button(
                expressao_frame,
                text=text,
                command=lambda op=operation: self.on_process_text(op),
                color=color
            )
            btn.pack(side=tk.LEFT, padx=2)
    
    def _create_config_button(self, parent):
        """Create configuration button"""
        config_frame = tk.Frame(parent, bg='#ffffff')
        config_frame.pack(fill=tk.X, pady=(10, 0))
        
        config_btn = self._create_modern_button(
            config_frame,
            text="⚙️ Configurações",
            command=self.on_show_config,
            color="#95a5a6",
            size="large"
        )
        config_btn.pack()
    
    def _create_modern_button(self, parent, text, command, color, size="normal"):
        """Create a modern button with enhanced styling"""
        if size == "large":
            font = ("Segoe UI", 11, "bold")
            padx, pady = 25, 10
        else:
            font = ("Segoe UI", 9, "bold")
            padx, pady = 12, 6
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg='white',
            font=font,
            relief=tk.FLAT,
            bd=0,
            padx=padx,
            pady=pady,
            cursor='hand2',
            activebackground=self._darken_color(color),
            activeforeground='white'
        )
        
        # Add modern hover effects
        self._add_modern_hover_effect(btn, color)
        return btn
    
    def _create_status(self, parent):
        """Create status section"""
        status_frame = tk.Frame(parent, bg='#ffffff')
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Modern status indicator with background
        status_bg = tk.Frame(status_frame, bg='#e8f5e8', relief=tk.FLAT, bd=0)
        status_bg.pack(fill=tk.X, pady=5)
        
        # Status indicator
        status_indicator = tk.Label(
            status_bg, 
            text="●", 
            font=("Arial", 12), 
            bg='#e8f5e8',
            fg='#27ae60'
        )
        status_indicator.pack(side=tk.LEFT, padx=(10, 8), pady=8)
        
        # Status text
        self.status_text = tk.Label(
            status_bg, 
            text="Pronto para usar", 
            font=("Segoe UI", 10), 
            bg='#e8f5e8',
            fg='#27ae60'
        )
        self.status_text.pack(side=tk.LEFT, pady=8)
    
    def _darken_color(self, color: str) -> str:
        """Darken a hex color for hover effect"""
        color_map = {
            '#667eea': '#5a6fd8',
            '#56ab2f': '#4a9a26',
            '#36d1dc': '#2bb8c4',
            '#f093fb': '#e67ee6',
            '#f5576c': '#e74c3c',
            '#ff6b6b': '#e74c3c',
            '#feca57': '#f39c12',
            '#95a5a6': '#7f8c8d'
        }
        return color_map.get(color, color)
    
    def _add_modern_hover_effect(self, button: tk.Button, original_color: str):
        """Add modern hover effect to button"""
        def on_enter(event):
            button.config(bg=self._darken_color(original_color))
            # Add subtle scale effect (simulated with padding)
            current_padx = button.cget('padx')
            current_pady = button.cget('pady')
            button.config(padx=current_padx + 1, pady=current_pady + 1)
        
        def on_leave(event):
            button.config(bg=original_color)
            # Reset padding
            current_padx = button.cget('padx')
            current_pady = button.cget('pady')
            button.config(padx=current_padx - 1, pady=current_pady - 1)
        
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
    
    def update_status(self, message: str, color: str = '#27ae60'):
        """Update status message"""
        try:
            if hasattr(self, 'status_text'):
                self.status_text.config(text=message, fg=color)
                # Update background color based on status
                if 'erro' in message.lower() or 'error' in message.lower():
                    bg_color = '#fadbd8'
                elif 'processando' in message.lower() or 'processando' in message.lower():
                    bg_color = '#d5e8f4'
                else:
                    bg_color = '#e8f5e8'
                
                # Update parent background
                parent = self.status_text.master
                if hasattr(parent, 'config'):
                    parent.config(bg=bg_color)
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
        """Set result text (now just for compatibility - results shown in notifications)"""
        # Results are now shown in system notifications, this method is kept for compatibility
        self.logger.info("Result text received (shown in notification)")
    
