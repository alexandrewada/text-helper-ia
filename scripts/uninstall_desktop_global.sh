#!/bin/bash

# Script para desinstalar o atalho global do Text Helper IA do menu do Debian
# Requer privilégios de administrador (sudo)

echo "Desinstalando atalho global do Text Helper IA do menu do sistema..."

# Verificar se está executando como root ou com sudo
if [ "$EUID" -ne 0 ]; then
    echo "Este script requer privilégios de administrador."
    echo "Execute com: sudo ./uninstall_desktop_global.sh"
    exit 1
fi

# Remover o arquivo .desktop do diretório de aplicações do sistema
if [ -f /usr/share/applications/text-helper-ia.desktop ]; then
    echo "Removendo atalho de /usr/share/applications/..."
    rm /usr/share/applications/text-helper-ia.desktop
else
    echo "ℹ️  Atalho não encontrado em /usr/share/applications/."
fi

# Remover o ícone do diretório de ícones do sistema
if [ -f /usr/share/pixmaps/text-helper-ia.png ]; then
    echo "Removendo ícone de /usr/share/pixmaps/..."
    rm /usr/share/pixmaps/text-helper-ia.png
else
    echo "ℹ️  Ícone não encontrado em /usr/share/pixmaps/."
fi

# Atualizar o banco de dados de aplicações
echo "Atualizando banco de dados de aplicações..."
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications
fi

echo "✅ Atalho global removido com sucesso!"
echo "O Text Helper IA não aparece mais no menu de aplicações para todos os usuários."
