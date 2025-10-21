#!/bin/bash
# Script para configurar atalhos de teclado no sistema

echo "🤖 Text Helper AI - Configuração de Atalhos"
echo "=============================================="
echo

# Diretório do projeto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHORTCUTS_SCRIPT="$PROJECT_DIR/text_helper_shortcuts.py"

echo "📁 Diretório do projeto: $PROJECT_DIR"
echo "📄 Script de atalhos: $SHORTCUTS_SCRIPT"
echo

# Verificar se o script existe
if [ ! -f "$SHORTCUTS_SCRIPT" ]; then
    echo "❌ Script de atalhos não encontrado!"
    exit 1
fi

echo "🔧 Configurando atalhos de teclado..."
echo

# Criar aliases para o shell
echo "📝 Adicionando aliases ao ~/.bashrc..."
cat >> ~/.bashrc << EOF

# Text Helper AI - Atalhos
alias encurtar='python3 $SHORTCUTS_SCRIPT shorten'
alias melhorar='python3 $SHORTCUTS_SCRIPT improve'
alias informal='python3 $SHORTCUTS_SCRIPT informal'
alias formal='python3 $SHORTCUTS_SCRIPT formal'
alias corrigir='python3 $SHORTCUTS_SCRIPT spellcheck'
alias resumir='python3 $SHORTCUTS_SCRIPT summarize'
alias expandir='python3 $SHORTCUTS_SCRIPT expand'
alias traduzir-en='python3 $SHORTCUTS_SCRIPT translate_en'
alias traduzir-pt='python3 $SHORTCUTS_SCRIPT translate_pt'
alias criativo='python3 $SHORTCUTS_SCRIPT creative'
alias tecnico='python3 $SHORTCUTS_SCRIPT technical'
alias emojis='python3 $SHORTCUTS_SCRIPT emojify'
alias analisar='python3 $SHORTCUTS_SCRIPT analyze'
alias reescrever='python3 $SHORTCUTS_SCRIPT rewrite'
EOF

echo "✅ Aliases adicionados ao ~/.bashrc"
echo

# Criar script para atalhos globais (se suportado)
echo "🌐 Configurando atalhos globais..."

# Verificar se o sistema suporta atalhos globais
if command -v xbindkeys >/dev/null 2>&1; then
    echo "📋 Sistema suporta xbindkeys - configurando atalhos..."
    
    # Criar configuração do xbindkeys
    cat > ~/.xbindkeysrc << EOF
# Text Helper AI - Atalhos Globais
# Ctrl+Ç para encurtar
"python3 $SHORTCUTS_SCRIPT shorten"
  c:51

# Ctrl+Shift+Ç para melhorar
"python3 $SHORTCUTS_SCRIPT improve"
  c:51 + shift

# Ctrl+Alt+Ç para corrigir
"python3 $SHORTCUTS_SCRIPT spellcheck"
  c:51 + alt

# Ctrl+Ç+1 para informal
"python3 $SHORTCUTS_SCRIPT informal"
  c:51 + 1

# Ctrl+Ç+2 para formal
"python3 $SHORTCUTS_SCRIPT formal"
  c:51 + 2

# Ctrl+Ç+3 para resumir
"python3 $SHORTCUTS_SCRIPT summarize"
  c:51 + 3

# Ctrl+Ç+4 para expandir
"python3 $SHORTCUTS_SCRIPT expand"
  c:51 + 4

# Ctrl+Ç+5 para traduzir para inglês
"python3 $SHORTCUTS_SCRIPT translate_en"
  c:51 + 5

# Ctrl+Ç+6 para traduzir para português
"python3 $SHORTCUTS_SCRIPT translate_pt"
  c:51 + 6
EOF

    echo "✅ Configuração do xbindkeys criada"
    echo "💡 Para ativar: xbindkeys -f ~/.xbindkeysrc"
    
elif command -v gsettings >/dev/null 2>&1; then
    echo "📋 Sistema suporta gsettings - configurando atalhos..."
    echo "💡 Configure manualmente no 'Configurações do Sistema > Teclado > Atalhos'"
    echo "   Use os comandos abaixo como ações:"
    echo "   - Encurtar: python3 $SHORTCUTS_SCRIPT shorten"
    echo "   - Melhorar: python3 $SHORTCUTS_SCRIPT improve"
    echo "   - Corrigir: python3 $SHORTCUTS_SCRIPT spellcheck"
    
else
    echo "⚠️  Sistema não suporta atalhos globais automáticos"
    echo "💡 Configure manualmente no seu gerenciador de janelas"
fi

echo
echo "🎉 Configuração concluída!"
echo
echo "📋 Como usar:"
echo "1. Reinicie o terminal ou execute: source ~/.bashrc"
echo "2. Selecione um texto em qualquer aplicação"
echo "3. Use os aliases: encurtar, melhorar, corrigir, etc."
echo "4. Ou use: python3 $SHORTCUTS_SCRIPT [operação]"
echo
echo "⌨️  Atalhos disponíveis:"
echo "   encurtar, melhorar, informal, formal, corrigir"
echo "   resumir, expandir, traduzir-en, traduzir-pt"
echo "   criativo, tecnico, emojis, analisar, reescrever"
echo
echo "💡 Para ver todas as opções: python3 $SHORTCUTS_SCRIPT help"
