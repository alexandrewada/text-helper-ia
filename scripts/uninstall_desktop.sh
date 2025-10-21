#!/bin/bash

# Script para desinstalar o atalho do Text Helper IA do menu do Debian

echo "Desinstalando atalho do Text Helper IA do menu do sistema..."

# Remover o arquivo .desktop do diretório de aplicações do usuário
if [ -f ~/.local/share/applications/text-helper-ia.desktop ]; then
    echo "Removendo atalho de ~/.local/share/applications/..."
    rm ~/.local/share/applications/text-helper-ia.desktop
    
    # Atualizar o banco de dados de aplicações
    echo "Atualizando banco de dados de aplicações..."
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database ~/.local/share/applications
    fi
    
    echo "✅ Atalho removido com sucesso!"
    echo "O Text Helper IA não aparece mais no menu de aplicações."
else
    echo "ℹ️  Atalho não encontrado. Pode já ter sido removido."
fi
