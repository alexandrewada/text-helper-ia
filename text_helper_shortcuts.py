#!/usr/bin/env python3
"""
Text Helper AI - Script de Atalhos
Facilita o uso dos atalhos de teclado
"""
import sys
import os

def show_help():
    """Mostra ajuda sobre os atalhos"""
    print("🤖 Text Helper AI - Atalhos de Teclado")
    print("=" * 50)
    print()
    print("📋 Como usar:")
    print("1. Selecione um texto em qualquer aplicação")
    print("2. Execute um dos comandos abaixo:")
    print()
    print("⌨️  Atalhos disponíveis:")
    print("   python3 text_helper_shortcuts.py shorten     # Encurtar texto")
    print("   python3 text_helper_shortcuts.py improve     # Melhorar texto")
    print("   python3 text_helper_shortcuts.py informal    # Tornar informal")
    print("   python3 text_helper_shortcuts.py formal      # Tornar formal")
    print("   python3 text_helper_shortcuts.py spellcheck  # Corrigir ortografia")
    print("   python3 text_helper_shortcuts.py summarize   # Resumir texto")
    print("   python3 text_helper_shortcuts.py expand      # Expandir texto")
    print("   python3 text_helper_shortcuts.py translate_en # Traduzir para inglês")
    print("   python3 text_helper_shortcuts.py translate_pt # Traduzir para português")
    print("   python3 text_helper_shortcuts.py creative    # Versão criativa")
    print("   python3 text_helper_shortcuts.py technical   # Versão técnica")
    print("   python3 text_helper_shortcuts.py emojify     # Adicionar emojis")
    print("   python3 text_helper_shortcuts.py analyze     # Analisar texto")
    print("   python3 text_helper_shortcuts.py rewrite     # Reescrever texto")
    print()
    print("💡 Dicas:")
    print("   - Você pode criar aliases no seu shell:")
    print("     alias encurtar='python3 text_helper_shortcuts.py shorten'")
    print("     alias melhorar='python3 text_helper_shortcuts.py improve'")
    print("   - Ou usar atalhos personalizados no seu sistema")
    print()

def trigger_operation(operation):
    """Dispara uma operação específica"""
    trigger_file = os.path.expanduser("~/.text_helper_ai_trigger")
    
    try:
        with open(trigger_file, 'a') as f:
            f.write(f"{operation}\n")
        
        print(f"✅ Operação '{operation}' disparada!")
        print("👀 Verifique se o texto foi processado")
        
    except Exception as e:
        print(f"❌ Erro ao disparar operação: {e}")
        print("💡 Certifique-se de que o Text Helper AI está rodando")

def main():
    """Função principal"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    operation = sys.argv[1].lower()
    
    valid_operations = [
        'shorten', 'improve', 'informal', 'formal', 'spellcheck',
        'summarize', 'expand', 'translate_en', 'translate_pt',
        'creative', 'technical', 'emojify', 'analyze', 'rewrite'
    ]
    
    if operation in valid_operations:
        trigger_operation(operation)
    elif operation in ['help', '--help', '-h']:
        show_help()
    else:
        print(f"❌ Operação '{operation}' não reconhecida")
        print("💡 Use 'python3 text_helper_shortcuts.py help' para ver as opções")

if __name__ == "__main__":
    main()
