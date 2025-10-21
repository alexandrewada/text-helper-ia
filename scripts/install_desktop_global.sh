#!/bin/bash

# Script para instalar o atalho do Text Helper IA globalmente no menu do Debian
# Requer privilégios de administrador (sudo)

echo "Instalando atalho do Text Helper IA globalmente no menu do sistema..."

# Verificar se está executando como root ou com sudo
if [ "$EUID" -ne 0 ]; then
    echo "Este script requer privilégios de administrador."
    echo "Execute com: sudo ./install_desktop_global.sh"
    exit 1
fi

# Verificar se o arquivo .desktop existe
if [ ! -f "text-helper-ia.desktop" ]; then
    echo "Erro: Arquivo text-helper-ia.desktop não encontrado!"
    exit 1
fi

# Verificar se o ícone existe
if [ ! -f "icon.png" ]; then
    echo "Aviso: Arquivo icon.png não encontrado. O atalho será criado sem ícone."
fi

# Tornar o arquivo .desktop executável
chmod +x text-helper-ia.desktop

# Copiar para o diretório de aplicações do sistema
echo "Copiando atalho para /usr/share/applications/..."
cp text-helper-ia.desktop /usr/share/applications/

# Copiar o ícone para o diretório de ícones do sistema
if [ -f "icon.png" ]; then
    echo "Copiando ícone para /usr/share/pixmaps/..."
    cp icon.png /usr/share/pixmaps/text-helper-ia.png
    
    # Atualizar o arquivo .desktop para usar o ícone do sistema
    sed -i 's|Icon=/home/alexandrewada/text-helper-ia/icon.png|Icon=text-helper-ia|' /usr/share/applications/text-helper-ia.desktop
fi

# Atualizar o banco de dados de aplicações
echo "Atualizando banco de dados de aplicações..."
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications
fi

# Verificar se o atalho foi instalado
if [ -f /usr/share/applications/text-helper-ia.desktop ]; then
    echo "✅ Atalho instalado globalmente com sucesso!"
    echo ""
    echo "O Text Helper IA agora aparece no menu de aplicações para todos os usuários."
    echo "Você pode encontrá-lo em:"
    echo "  - Menu de aplicações > Escritório"
    echo "  - Menu de aplicações > Utilitários"
    echo "  - Menu de aplicações > Educação"
    echo ""
    echo "Para desinstalar, execute: sudo ./uninstall_desktop_global.sh"
else
    echo "❌ Erro ao instalar o atalho."
    exit 1
fi
