"""
Main Window for Text Helper AI
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
        
        self.root.title("Text Helper AI - Suíte Completa de Processamento de Texto")
        self.root.geometry(f"{ui_config['window_width']}x{ui_config['window_height']}")
        self.root.configure(bg='#f8f9fa')
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (ui_config['window_width'] // 2)
        y = (self.root.winfo_screenheight() // 2) - (ui_config['window_height'] // 2)
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
        
        # Instructions section
        self._create_instructions(main_container)
        
        # Quick access buttons
        self._create_quick_access(main_container)
        
        # Control buttons
        self._create_controls(main_container)
        
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
            text="Text Helper AI", 
            font=("Arial", 20, "bold"), 
            bg='#f8f9fa',
            fg='#343a40'
        )
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame, 
            text="Suíte completa de processamento de texto com IA", 
            font=("Arial", 12), 
            bg='#f8f9fa',
            fg='#6c757d'
        )
        subtitle_label.pack(pady=(5, 0))
    
    def _create_instructions(self, parent):
        """Create instructions section"""
        instructions_frame = tk.Frame(parent, bg='#f8f9fa')
        instructions_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Instructions title
        instructions_title = tk.Label(
            instructions_frame, 
            text="📋 Instruções de Uso", 
            font=("Arial", 14, "bold"), 
            bg='#f8f9fa',
            fg='#343a40'
        )
        instructions_title.pack(anchor=tk.W, pady=(0, 10))
        
        # Instructions text with scrollbar
        text_frame = tk.Frame(instructions_frame, bg='#f8f9fa')
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        instructions_text = tk.Text(
            text_frame, 
            height=12, 
            wrap=tk.WORD, 
            bg='#ffffff', 
            relief=tk.SUNKEN, 
            bd=1,
            font=("Arial", 10),
            padx=15,
            pady=15
        )
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=instructions_text.yview)
        instructions_text.configure(yscrollcommand=scrollbar.set)
        
        instructions_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Instructions content
        instructions_content = """
🚀 COMO USAR:

1. SELECIONE o texto que você quer processar OU COPIE (Ctrl+C)
2. CLIQUE em "Mostrar Menu Flutuante" para abrir o menu sempre visível
3. ARRASTE o menu flutuante para qualquer lugar da tela
4. ESCOLHA uma das opções organizadas por categoria
5. O texto processado será mostrado e copiado automaticamente
6. COLE o texto processado onde você quiser (Ctrl+V)

⌨️ ATALHO ALTERNATIVO: Use o comando de arquivo trigger
💡 DICA: O sistema prioriza texto selecionado sobre a área de transferência!

📝 FUNCIONALIDADES DISPONÍVEIS:

📝 BÁSICO:
• Encurtar: Reduz o texto mantendo informações essenciais
• Melhorar: Melhora clareza e estrutura do texto
• Resumir: Cria resumos concisos de textos longos
• Expandir: Adiciona detalhes e exemplos ao texto

🎭 ESTILO:
• Informal: Transforma em linguagem casual e descontraída
• Formal: Transforma em linguagem profissional e culta
• Criativo: Reescreve de forma mais envolvente e dinâmica
• Técnico: Reescreve com terminologia técnica e precisa

🌍 TRADUÇÃO:
• → Inglês: Traduz do português para inglês
• → Português: Traduz do inglês para português

✨ EXTRAS:
• Corrigir: Corrige erros ortográficos e gramaticais
• Emojis: Adiciona emojis relevantes ao texto
• Analisar: Fornece insights sobre o texto
• Reescrever: Reescreve com abordagem diferente

🎨 CARACTERÍSTICAS DO MENU FLUTUANTE:
• Sempre visível em cima de outras janelas
• Arrastável para qualquer posição
• Pode ser minimizado ou fechado
• Organizado em categorias com scroll
• Acesso rápido a 14 funcionalidades
• Interface moderna e responsiva

💡 DICA: O menu flutuante fica sempre acessível em qualquer aplicativo!
        """
        
        instructions_text.insert(tk.END, instructions_content)
        instructions_text.config(state=tk.DISABLED)
    
    def _create_quick_access(self, parent):
        """Create quick access buttons section"""
        quick_frame = tk.Frame(parent, bg='#f8f9fa')
        quick_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Quick access title
        quick_title = tk.Label(
            quick_frame, 
            text="⚡ Acesso Rápido", 
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
        status_text = tk.Label(
            status_frame, 
            text="Status: Pronto para usar - Menu flutuante sempre acessível!", 
            font=("Arial", 10), 
            bg='#f8f9fa',
            fg='#28a745'
        )
        status_text.pack(side=tk.LEFT)
    
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
        # This would require storing references to status elements
        # For now, just log the status update
        self.logger.info(f"Status update: {message}")
    
    def show_error(self, title: str, message: str):
        """Show error message"""
        messagebox.showerror(title, message)
        self.logger.error(f"Error shown: {title} - {message}")
    
    def show_info(self, title: str, message: str):
        """Show info message"""
        messagebox.showinfo(title, message)
        self.logger.info(f"Info shown: {title} - {message}")
