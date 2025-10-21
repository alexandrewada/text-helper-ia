#!/usr/bin/env python3
"""
Text Helper AI - Suíte completa de processamento de texto com IA
"""

import os
import sys
import time
import configparser
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import pyperclip
from openai import OpenAI
import threading
import logging
import subprocess
from pynput import keyboard
import time

class LoadingDialog:
    def __init__(self, parent, message="Processando texto..."):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Processando")
        self.dialog.geometry("300x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Make it always on top
        self.dialog.attributes('-topmost', True)
        
        self.setup_ui(message)
        
    def setup_ui(self, message):
        """Setup the loading dialog UI"""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Loading icon (spinning)
        self.loading_label = tk.Label(main_frame, text="⏳", font=("Arial", 24), bg='white')
        self.loading_label.pack(pady=10)
        
        # Message
        message_label = tk.Label(main_frame, text=message, font=("Arial", 12), bg='white', fg='#333')
        message_label.pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate', length=200)
        self.progress.pack(pady=10)
        self.progress.start(10)
        
        # Status label
        self.status_label = tk.Label(main_frame, text="Aguarde...", font=("Arial", 10), bg='white', fg='#666')
        self.status_label.pack(pady=5)
        
        # Animate the loading icon
        self.animate_loading()
        
    def animate_loading(self):
        """Animate the loading icon"""
        icons = ["⏳", "⏰", "🔄", "⚡", "✨", "🌟"]
        if hasattr(self, 'current_icon'):
            self.current_icon = (self.current_icon + 1) % len(icons)
        else:
            self.current_icon = 0
            
        self.loading_label.config(text=icons[self.current_icon])
        self.dialog.after(500, self.animate_loading)
        
    def update_status(self, message):
        """Update the status message"""
        self.status_label.config(text=message)
        self.dialog.update()
        
    def close(self):
        """Close the loading dialog"""
        self.dialog.destroy()

class SuccessDialog:
    def __init__(self, parent, operation_name, original_text, processed_text):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"✅ {operation_name}")
        self.dialog.geometry("500x400")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Make it always on top
        self.dialog.attributes('-topmost', True)
        
        self.setup_ui(operation_name, original_text, processed_text)
        
    def setup_ui(self, operation_name, original_text, processed_text):
        """Setup the success dialog UI"""
        # Main frame
        main_frame = tk.Frame(self.dialog, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Success icon and title
        title_frame = tk.Frame(main_frame, bg='white')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        success_label = tk.Label(title_frame, text="✅", font=("Arial", 24), bg='white')
        success_label.pack(side=tk.LEFT)
        
        title_text = tk.Label(title_frame, text=f"Texto {operation_name} com Sucesso!", 
                             font=("Arial", 14, "bold"), bg='white', fg='#2E7D32')
        title_text.pack(side=tk.LEFT, padx=10)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Original text tab
        original_frame = tk.Frame(notebook, bg='white')
        notebook.add(original_frame, text="📄 Original")
        
        original_label = tk.Label(original_frame, text="Texto Original:", 
                                 font=("Arial", 10, "bold"), bg='white')
        original_label.pack(anchor=tk.W, pady=(10, 5), padx=10)
        
        original_text_widget = tk.Text(original_frame, height=8, wrap=tk.WORD, 
                                      bg='#F5F5F5', relief=tk.SUNKEN, bd=1)
        original_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        original_text_widget.insert(tk.END, original_text)
        original_text_widget.config(state=tk.DISABLED)
        
        # Processed text tab
        processed_frame = tk.Frame(notebook, bg='white')
        notebook.add(processed_frame, text="✨ Resultado")
        
        processed_label = tk.Label(processed_frame, text="Texto Processado:", 
                                  font=("Arial", 10, "bold"), bg='white')
        processed_label.pack(anchor=tk.W, pady=(10, 5), padx=10)
        
        processed_text_widget = tk.Text(processed_frame, height=8, wrap=tk.WORD, 
                                       bg='#E8F5E8', relief=tk.SUNKEN, bd=1)
        processed_text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        processed_text_widget.insert(tk.END, processed_text)
        processed_text_widget.config(state=tk.DISABLED)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Copy button
        copy_btn = tk.Button(buttons_frame, text="📋 Copiar Resultado", 
                            command=lambda: self.copy_to_clipboard(processed_text),
                            bg='#4CAF50', fg='white', font=("Arial", 10, "bold"),
                            relief=tk.RAISED, bd=2)
        copy_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        close_btn = tk.Button(buttons_frame, text="✖️ Fechar", 
                             command=self.close,
                             bg='#F44336', fg='white', font=("Arial", 10, "bold"),
                             relief=tk.RAISED, bd=2)
        close_btn.pack(side=tk.RIGHT)
        
        # Auto-close after 10 seconds
        self.dialog.after(10000, self.close)
        
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        pyperclip.copy(text)
        messagebox.showinfo("Copiado!", "Texto copiado para a área de transferência!")
        
    def close(self):
        """Close the success dialog"""
        self.dialog.destroy()

class FloatingMenu:
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.window = tk.Toplevel()
        self.window.title("Menu de Contexto")
        self.window.geometry("250x400")
        self.window.overrideredirect(True)  # Remove window decorations
        self.window.attributes('-topmost', True)  # Always on top
        self.window.configure(bg='lightgray')
        
        # Variables for dragging
        self.start_x = 0
        self.start_y = 0
        self.is_minimized = False
        self.is_processing = False
        
        self.setup_ui()
        self.setup_drag()
        
    def setup_ui(self):
        """Setup the floating menu UI"""
        # Title bar
        title_frame = tk.Frame(self.window, bg='darkgray', height=25)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="📝 Menu de Contexto", 
                              bg='darkgray', fg='white', font=('Arial', 8, 'bold'))
        title_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Status indicator
        self.status_indicator = tk.Label(title_frame, text="●", 
                                        bg='darkgray', fg='#4CAF50', font=('Arial', 10))
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_btn = tk.Button(title_frame, text="×", bg='darkgray', fg='white', 
                             font=('Arial', 10, 'bold'), bd=0, width=2,
                             command=self.close_menu)
        close_btn.pack(side=tk.RIGHT, padx=2, pady=1)
        
        # Minimize button
        min_btn = tk.Button(title_frame, text="−", bg='darkgray', fg='white', 
                           font=('Arial', 10, 'bold'), bd=0, width=2,
                           command=self.minimize_menu)
        min_btn.pack(side=tk.RIGHT, padx=1, pady=1)
        
        # Create scrollable frame for menu buttons
        canvas = tk.Canvas(self.window, bg='lightgray', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='lightgray')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(5, 0), pady=5)
        scrollbar.pack(side="right", fill="y", pady=5)
        
        # Create buttons organized by categories
        categories = [
            ("📝 BÁSICO", [
                ('📝 Encurtar', 'shorten', 'lightblue'),
                ('✨ Melhorar', 'improve', 'lightgreen'),
                ('📋 Resumir', 'summarize', 'lightcyan'),
                ('📖 Expandir', 'expand', 'lightsteelblue')
            ]),
            ("🎭 ESTILO", [
                ('😊 Informal', 'informal', 'lightyellow'),
                ('👔 Formal', 'formal', 'lightcoral'),
                ('🎨 Criativo', 'creative', 'plum'),
                ('🔧 Técnico', 'technical', 'lightgray')
            ]),
            ("🌍 TRADUÇÃO", [
                ('🇺🇸 → Inglês', 'translate_en', 'lightpink'),
                ('🇧🇷 → Português', 'translate_pt', 'lightseagreen')
            ]),
            ("✨ EXTRAS", [
                ('✅ Corrigir', 'spellcheck', 'lightgreen'),
                ('😀 Emojis', 'emojify', 'gold')
            ])
        ]
        
        for category_name, operations in categories:
            # Category label
            category_label = tk.Label(scrollable_frame, text=category_name, 
                                    bg='darkgray', fg='white', font=('Arial', 8, 'bold'))
            category_label.pack(fill=tk.X, pady=(5, 2))
            
            # Category buttons
            for text, operation, color in operations:
                btn = tk.Button(scrollable_frame, text=text, bg=color, 
                               font=('Arial', 7, 'bold'),
                               command=lambda op=operation: self.parent_app.process_text_from_clipboard(op),
                               relief=tk.RAISED, bd=1, height=1)
                btn.pack(fill=tk.X, pady=1, padx=2)
            
    def setup_drag(self):
        """Setup dragging functionality"""
        def start_drag(event):
            self.start_x = event.x_root - self.window.winfo_x()
            self.start_y = event.y_root - self.window.winfo_y()
            
        def drag_window(event):
            x = event.x_root - self.start_x
            y = event.y_root - self.start_y
            self.window.geometry(f"+{x}+{y}")
            
        # Bind drag events to title bar
        title_frame = self.window.winfo_children()[0]
        title_frame.bind("<Button-1>", start_drag)
        title_frame.bind("<B1-Motion>", drag_window)
        
        # Also bind to the title label
        title_label = title_frame.winfo_children()[0]
        title_label.bind("<Button-1>", start_drag)
        title_label.bind("<B1-Motion>", drag_window)
        
    def minimize_menu(self):
        """Minimize the floating menu"""
        if not self.is_minimized:
            self.window.geometry("250x30")
            self.is_minimized = True
        else:
            self.window.geometry("250x400")
            self.is_minimized = False
            
    def set_processing_status(self, is_processing):
        """Set the processing status indicator"""
        self.is_processing = is_processing
        if is_processing:
            self.status_indicator.config(text="⏳", fg='#FF9800')
            self.window.title("⏳ Processando...")
        else:
            self.status_indicator.config(text="●", fg='#4CAF50')
            self.window.title("📝 Menu de Contexto")
            
    def close_menu(self):
        """Close the floating menu"""
        self.window.destroy()
        self.parent_app.floating_menu = None

class TextHelperAI:
    def __init__(self):
        self.setup_logging()
        self.config_file = os.path.expanduser("~/.text_shortener_config.ini")
        self.load_config()
        self.setup_openai()
        self.floating_menu = None
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.expanduser('~/.text_shortener.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Load configuration from file"""
        self.config = configparser.ConfigParser()
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.config['DEFAULT'] = {
                'openai_api_key': '',
                'model': 'gpt-3.5-turbo',
                'max_tokens': '150'
            }
            self.save_config()
            
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            self.config.write(f)
            
    def setup_openai(self):
        """Initialize OpenAI client"""
        api_key = self.config.get('DEFAULT', 'openai_api_key', fallback='')
        if not api_key:
            self.logger.warning("OpenAI API key not configured")
            self.openai_client = None
        else:
            self.openai_client = OpenAI(api_key=api_key)
            
    def configure_api_key(self):
        """Configure OpenAI API key through GUI"""
        root = tk.Tk()
        root.withdraw()
        
        current_key = self.config.get('DEFAULT', 'openai_api_key', fallback='')
        api_key = simpledialog.askstring(
            "Configuration",
            "Enter your OpenAI API Key:",
            initialvalue=current_key,
            show='*'
        )
        
        if api_key:
            self.config.set('DEFAULT', 'openai_api_key', api_key)
            self.save_config()
            self.setup_openai()
            messagebox.showinfo("Success", "API Key configured successfully!")
            self.logger.info("API Key configured")
        else:
            messagebox.showwarning("Warning", "API Key not provided")
            
        root.destroy()
        
    def process_text_with_ai(self, text, operation_type):
        """Send text to ChatGPT for processing based on operation type"""
        if not self.openai_client:
            raise Exception("OpenAI client not configured. Please set up your API key.")
            
        try:
            system_prompts = {
                'shorten': "Você é um assistente útil que encurta textos preservando o significado principal e as informações-chave. Torne o texto mais conciso e claro. SEMPRE responda em português brasileiro.",
                'improve': "Você é um assistente útil que melhora textos tornando-os mais claros, bem estruturados e profissionais. Mantenha o significado original mas torne o texto mais fluido e bem escrito. SEMPRE responda em português brasileiro.",
                'informal': "Você é um assistente útil que transforma textos formais em linguagem informal e descontraída, mantendo o significado original. Use linguagem coloquial, contrações e um tom mais casual. SEMPRE responda em português brasileiro.",
                'formal': "Você é um assistente útil que transforma textos informais em linguagem formal e profissional, mantendo o significado original. Use linguagem culta, estruturas mais elaboradas e um tom respeitoso. SEMPRE responda em português brasileiro.",
                'spellcheck': "Você é um assistente útil que corrige erros ortográficos e gramaticais em textos em português brasileiro. Corrija apenas os erros, mantendo o estilo e tom original. SEMPRE responda em português brasileiro.",
                'summarize': "Você é um assistente útil que cria resumos concisos de textos longos, destacando os pontos principais e informações mais importantes. SEMPRE responda em português brasileiro.",
                'expand': "Você é um assistente útil que expande textos curtos adicionando detalhes relevantes, exemplos e explicações, mantendo a coerência e o tom original. SEMPRE responda em português brasileiro.",
                'translate_en': "Você é um assistente útil que traduz textos do português para o inglês de forma natural e fluida, mantendo o significado e tom original. SEMPRE responda em inglês.",
                'translate_pt': "Você é um assistente útil que traduz textos do inglês para o português brasileiro de forma natural e fluida, mantendo o significado e tom original. SEMPRE responda em português brasileiro.",
                'creative': "Você é um assistente criativo que reescreve textos de forma mais interessante, envolvente e criativa, mantendo o significado original mas tornando-o mais atrativo e dinâmico. SEMPRE responda em português brasileiro.",
                'technical': "Você é um assistente técnico que reescreve textos de forma mais técnica e precisa, usando terminologia adequada e estruturas mais formais, mantendo a clareza. SEMPRE responda em português brasileiro.",
                'emojify': "Você é um assistente divertido que adiciona emojis relevantes ao texto para torná-lo mais expressivo e visualmente atrativo, sem exagerar. SEMPRE responda em português brasileiro."
            }
            
            user_prompts = {
                'shorten': f"Por favor, encurte este texto mantendo as informações essenciais. Responda em português brasileiro:\n\n{text}",
                'improve': f"Por favor, melhore este texto tornando-o mais claro e bem estruturado. Responda em português brasileiro:\n\n{text}",
                'informal': f"Por favor, transforme este texto em linguagem informal e descontraída. Responda em português brasileiro:\n\n{text}",
                'formal': f"Por favor, transforme este texto em linguagem formal e profissional. Responda em português brasileiro:\n\n{text}",
                'spellcheck': f"Por favor, corrija os erros ortográficos e gramaticais deste texto. Responda em português brasileiro:\n\n{text}",
                'summarize': f"Por favor, crie um resumo conciso deste texto destacando os pontos principais. Responda em português brasileiro:\n\n{text}",
                'expand': f"Por favor, expanda este texto adicionando detalhes relevantes e exemplos. Responda em português brasileiro:\n\n{text}",
                'translate_en': f"Por favor, traduza este texto para o inglês de forma natural. Responda em inglês:\n\n{text}",
                'translate_pt': f"Please translate this text to Brazilian Portuguese in a natural way. Responda em português brasileiro:\n\n{text}",
                'creative': f"Por favor, reescreva este texto de forma mais criativa e envolvente. Responda em português brasileiro:\n\n{text}",
                'technical': f"Por favor, reescreva este texto de forma mais técnica e precisa. Responda em português brasileiro:\n\n{text}",
                'emojify': f"Por favor, adicione emojis relevantes a este texto para torná-lo mais expressivo. Responda em português brasileiro:\n\n{text}"
            }
            
            response = self.openai_client.chat.completions.create(
                model=self.config.get('DEFAULT', 'model', fallback='gpt-3.5-turbo'),
                messages=[
                    {
                        "role": "system",
                        "content": system_prompts[operation_type]
                    },
                    {
                        "role": "user",
                        "content": user_prompts[operation_type]
                    }
                ],
                max_tokens=int(self.config.get('DEFAULT', 'max_tokens', fallback='150')),
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error calling OpenAI API: {e}")
            raise Exception(f"Failed to process text: {str(e)}")
    
    def shorten_text(self, text):
        """Send text to ChatGPT for shortening"""
        return self.process_text_with_ai(text, 'shorten')
    
    def improve_text(self, text):
        """Send text to ChatGPT for improvement"""
        return self.process_text_with_ai(text, 'improve')
    
    def make_informal(self, text):
        """Send text to ChatGPT to make it informal"""
        return self.process_text_with_ai(text, 'informal')
    
    def make_formal(self, text):
        """Send text to ChatGPT to make it formal"""
        return self.process_text_with_ai(text, 'formal')
    
    def spellcheck_text(self, text):
        """Send text to ChatGPT for spell checking"""
        return self.process_text_with_ai(text, 'spellcheck')
    
    def summarize_text(self, text):
        """Send text to ChatGPT for summarization"""
        return self.process_text_with_ai(text, 'summarize')
    
    def expand_text(self, text):
        """Send text to ChatGPT for expansion"""
        return self.process_text_with_ai(text, 'expand')
    
    def translate_to_english(self, text):
        """Send text to ChatGPT for translation to English"""
        return self.process_text_with_ai(text, 'translate_en')
    
    def translate_to_portuguese(self, text):
        """Send text to ChatGPT for translation to Portuguese"""
        return self.process_text_with_ai(text, 'translate_pt')
    
    def make_creative(self, text):
        """Send text to ChatGPT to make it creative"""
        return self.process_text_with_ai(text, 'creative')
    
    def make_technical(self, text):
        """Send text to ChatGPT to make it technical"""
        return self.process_text_with_ai(text, 'technical')
    
    def add_emojis(self, text):
        """Send text to ChatGPT to add emojis"""
        return self.process_text_with_ai(text, 'emojify')
    
    def get_selected_text(self):
        """Get selected text by simulating Ctrl+C and checking clipboard"""
        try:
            # Store current clipboard content
            original_clipboard = pyperclip.paste()
            
            # Simulate Ctrl+C to copy selected text
            controller = keyboard.Controller()
            controller.press(keyboard.Key.ctrl)
            controller.press('c')
            controller.release('c')
            controller.release(keyboard.Key.ctrl)
            
            # Wait a bit for the copy operation to complete
            time.sleep(0.1)
            
            # Get the new clipboard content
            new_clipboard = pyperclip.paste()
            
            # Check if something was actually copied (different from original)
            if new_clipboard != original_clipboard and new_clipboard.strip():
                return new_clipboard.strip()
            else:
                # Restore original clipboard if nothing was selected
                pyperclip.copy(original_clipboard)
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting selected text: {e}")
            return None
    
    def get_text_from_source(self):
        """Get text from selected text first, then fallback to clipboard"""
        # Try to get selected text first
        selected_text = self.get_selected_text()
        
        if selected_text:
            self.logger.info("Using selected text")
            return selected_text, "selecionado"
        else:
            # Fallback to clipboard
            try:
                clipboard_text = pyperclip.paste()
                if clipboard_text and clipboard_text.strip():
                    self.logger.info("Using clipboard text")
                    return clipboard_text.strip(), "clipboard"
                else:
                    return None, None
            except Exception as e:
                self.logger.error(f"Error reading clipboard: {e}")
                return None, None
            
    def process_text_from_clipboard(self, operation_type='shorten'):
        """Process text from selected text or clipboard with specified operation"""
        # Get text from selected text first, then fallback to clipboard
        text_result = self.get_text_from_source()
        
        if text_result[0] is None:
            self.logger.warning("No text found in selection or clipboard")
            messagebox.showwarning("Warning", "Nenhum texto encontrado. Selecione um texto ou copie algo para a área de transferência primeiro.")
            return
        
        selected_text, text_source = text_result
        
        # Get parent window for dialogs
        parent_window = None
        if hasattr(self, 'floating_menu') and self.floating_menu:
            parent_window = self.floating_menu.window
        else:
            # Create a temporary root window for dialogs
            parent_window = tk.Tk()
            parent_window.withdraw()
        
        # Show loading dialog with source information
        source_text = "selecionado" if text_source == "selecionado" else "da área de transferência"
        loading_dialog = LoadingDialog(parent_window, f"Processando texto {source_text}...")
        
        # Update floating menu status if available
        if hasattr(self, 'floating_menu') and self.floating_menu:
            self.floating_menu.set_processing_status(True)
        
        # Process in a separate thread to avoid blocking UI
        def process_in_thread():
            try:
                self.logger.info(f"Processing text: {selected_text[:50]}...")
                
                # Update loading status
                loading_dialog.update_status("Conectando com IA...")
                
                # Process the text based on operation type
                operation_functions = {
                    'shorten': self.shorten_text,
                    'improve': self.improve_text,
                    'informal': self.make_informal,
                    'formal': self.make_formal,
                    'spellcheck': self.spellcheck_text,
                    'summarize': self.summarize_text,
                    'expand': self.expand_text,
                    'translate_en': self.translate_to_english,
                    'translate_pt': self.translate_to_portuguese,
                    'creative': self.make_creative,
                    'technical': self.make_technical,
                    'emojify': self.add_emojis
                }
                
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
                    'emojify': 'Com Emojis'
                }
                
                loading_dialog.update_status("Processando com IA...")
                processed_text = operation_functions[operation_type](selected_text)
                
                loading_dialog.update_status("Finalizando...")
                
                # Copy processed text to clipboard
                pyperclip.copy(processed_text)
                
                # Close loading dialog
                loading_dialog.close()
                
                # Reset floating menu status
                if hasattr(self, 'floating_menu') and self.floating_menu:
                    self.floating_menu.set_processing_status(False)
                
                # Show success dialog with source information
                source_info = f" (texto {text_source})" if text_source == "selecionado" else ""
                success_dialog = SuccessDialog(parent_window, operation_names[operation_type] + source_info, 
                                             selected_text, processed_text)
                
                self.logger.info(f"Text successfully {operation_type}")
                
            except Exception as e:
                self.logger.error(f"Error processing text: {e}")
                loading_dialog.close()
                
                # Reset floating menu status
                if hasattr(self, 'floating_menu') and self.floating_menu:
                    self.floating_menu.set_processing_status(False)
                
                # Show error dialog
                error_dialog = tk.Toplevel(parent_window)
                error_dialog.title("❌ Erro")
                error_dialog.geometry("400x200")
                error_dialog.resizable(False, False)
                error_dialog.transient(parent_window)
                error_dialog.grab_set()
                error_dialog.attributes('-topmost', True)
                
                # Center the dialog
                error_dialog.geometry("+%d+%d" % (parent_window.winfo_rootx() + 50, parent_window.winfo_rooty() + 50))
                
                # Error UI
                main_frame = tk.Frame(error_dialog, bg='white')
                main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
                
                error_label = tk.Label(main_frame, text="❌", font=("Arial", 24), bg='white')
                error_label.pack(pady=10)
                
                error_text = tk.Label(main_frame, text="Erro ao processar texto:", 
                                     font=("Arial", 12, "bold"), bg='white', fg='#D32F2F')
                error_text.pack(pady=5)
                
                error_message = tk.Text(main_frame, height=4, wrap=tk.WORD, 
                                       bg='#FFEBEE', relief=tk.SUNKEN, bd=1)
                error_message.pack(fill=tk.BOTH, expand=True, pady=10)
                error_message.insert(tk.END, str(e))
                error_message.config(state=tk.DISABLED)
                
                close_btn = tk.Button(main_frame, text="✖️ Fechar", 
                                     command=error_dialog.destroy,
                                     bg='#F44336', fg='white', font=("Arial", 10, "bold"))
                close_btn.pack(pady=10)
        
        # Start processing in thread
        thread = threading.Thread(target=process_in_thread)
        thread.daemon = True
        thread.start()
    
    def show_floating_menu(self):
        """Show or hide the floating menu"""
        if self.floating_menu is None:
            self.floating_menu = FloatingMenu(self)
            self.logger.info("Floating menu created")
        else:
            self.floating_menu.close_menu()
            self.logger.info("Floating menu closed")
            
    def show_config_dialog(self):
        """Show configuration dialog"""
        root = tk.Tk()
        root.title("Text Helper AI Configuration")
        root.geometry("400x300")
        
        # API Key configuration
        tk.Label(root, text="OpenAI API Key:").pack(pady=5)
        api_key_var = tk.StringVar(value=self.config.get('DEFAULT', 'openai_api_key', fallback=''))
        api_key_entry = tk.Entry(root, textvariable=api_key_var, show='*', width=50)
        api_key_entry.pack(pady=5)
        
        # Model selection
        tk.Label(root, text="Model:").pack(pady=5)
        model_var = tk.StringVar(value=self.config.get('DEFAULT', 'model', fallback='gpt-3.5-turbo'))
        model_combo = ttk.Combobox(root, textvariable=model_var, values=['gpt-3.5-turbo', 'gpt-4'])
        model_combo.pack(pady=5)
        
        # Max tokens
        tk.Label(root, text="Max Tokens:").pack(pady=5)
        tokens_var = tk.StringVar(value=self.config.get('DEFAULT', 'max_tokens', fallback='150'))
        tokens_entry = tk.Entry(root, textvariable=tokens_var, width=10)
        tokens_entry.pack(pady=5)
        
        def save_config():
            self.config.set('DEFAULT', 'openai_api_key', api_key_var.get())
            self.config.set('DEFAULT', 'model', model_var.get())
            self.config.set('DEFAULT', 'max_tokens', tokens_var.get())
            self.save_config()
            self.setup_openai()
            messagebox.showinfo("Success", "Configuration saved!")
            root.destroy()
            
        tk.Button(root, text="Save Configuration", command=save_config).pack(pady=20)
        
        root.mainloop()
        
        
    def show_main_window(self):
        """Show main application window"""
        root = tk.Tk()
        root.title("Text Helper AI")
        root.geometry("600x500")
        
        # Title
        title_label = tk.Label(root, text="Text Helper AI", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Instructions
        instructions = tk.Text(root, height=10, width=70, wrap=tk.WORD)
        instructions.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        instructions_text = """
INSTRUÇÕES DE USO:

1. SELECIONE o texto que você quer processar OU COPIE (Ctrl+C)
2. CLIQUE em "Mostrar Menu Flutuante" para abrir o menu sempre visível
3. ARRASTE o menu flutuante para qualquer lugar da tela
4. ESCOLHA uma das opções organizadas por categoria
5. O texto processado será mostrado e copiado automaticamente
6. COLE o texto processado onde você quiser (Ctrl+V)

💡 DICA: O sistema prioriza texto selecionado sobre a área de transferência!

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

CARACTERÍSTICAS DO MENU FLUTUANTE:
• Sempre visível em cima de outras janelas
• Arrastável para qualquer posição
• Pode ser minimizado ou fechado
• Organizado em categorias com scroll
• Acesso rápido a 12 funcionalidades

DICA: O menu flutuante fica sempre acessível em qualquer aplicativo!
        """
        
        instructions.insert(tk.END, instructions_text)
        instructions.config(state=tk.DISABLED)
        
        # Floating menu button
        floating_frame = tk.Frame(root)
        floating_frame.pack(pady=20)
        
        floating_btn = tk.Button(floating_frame, text="🚀 Mostrar Menu Flutuante", 
                                command=self.show_floating_menu, 
                                bg="gold", font=("Arial", 12, "bold"),
                                relief=tk.RAISED, bd=3)
        floating_btn.pack(pady=10)
        
        # Quick access buttons - Row 1
        button_frame1 = tk.Frame(root)
        button_frame1.pack(pady=5)
        
        tk.Button(button_frame1, text="📝 Encurtar", 
                 command=lambda: self.process_text_from_clipboard('shorten'), 
                 bg="lightblue", font=("Arial", 8, "bold")).pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame1, text="✨ Melhorar", 
                 command=lambda: self.process_text_from_clipboard('improve'), 
                 bg="lightgreen", font=("Arial", 8, "bold")).pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame1, text="✅ Corrigir", 
                 command=lambda: self.process_text_from_clipboard('spellcheck'), 
                 bg="lightgreen", font=("Arial", 8, "bold")).pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame1, text="📋 Resumir", 
                 command=lambda: self.process_text_from_clipboard('summarize'), 
                 bg="lightcyan", font=("Arial", 8, "bold")).pack(side=tk.LEFT, padx=2)
        
        # Quick access buttons - Row 2
        button_frame2 = tk.Frame(root)
        button_frame2.pack(pady=5)
        
        tk.Button(button_frame2, text="😊 Informal", 
                 command=lambda: self.process_text_from_clipboard('informal'), 
                 bg="lightyellow", font=("Arial", 8, "bold")).pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame2, text="👔 Formal", 
                 command=lambda: self.process_text_from_clipboard('formal'), 
                 bg="lightcoral", font=("Arial", 8, "bold")).pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame2, text="🇺🇸 Inglês", 
                 command=lambda: self.process_text_from_clipboard('translate_en'), 
                 bg="lightpink", font=("Arial", 8, "bold")).pack(side=tk.LEFT, padx=2)
        
        tk.Button(button_frame2, text="😀 Emojis", 
                 command=lambda: self.process_text_from_clipboard('emojify'), 
                 bg="gold", font=("Arial", 8, "bold")).pack(side=tk.LEFT, padx=2)
        
        # Configuration button
        config_frame = tk.Frame(root)
        config_frame.pack(pady=10)
        
        tk.Button(config_frame, text="⚙️ Configurar", 
                 command=self.show_config_dialog, 
                 font=("Arial", 10)).pack()
        
        # Status
        status_label = tk.Label(root, text="Status: Pronto para usar - Menu flutuante sempre acessível!", fg="green")
        status_label.pack(pady=10)
        
        root.mainloop()
        
def main():
    """Main function"""
    app = TextHelperAI()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--config':
        app.show_config_dialog()
    else:
        app.show_main_window()
        
if __name__ == "__main__":
    main()
