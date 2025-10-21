#!/bin/bash

# Script para instalar o atalho do Text Helper IA no menu do Debian

echo "Instalando atalho do Text Helper IA no menu do sistema..."

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

# Copiar para o diretório de aplicações do usuário
echo "Copiando atalho para ~/.local/share/applications/..."
mkdir -p ~/.local/share/applications
cp text-helper-ia.desktop ~/.local/share/applications/

# Atualizar o banco de dados de aplicações
echo "Atualizando banco de dados de aplicações..."
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications
fi

# Verificar se o atalho foi instalado
if [ -f ~/.local/share/applications/text-helper-ia.desktop ]; then
    echo "✅ Atalho instalado com sucesso!"
    echo ""
    echo "O Text Helper IA agora aparece no menu de aplicações."
    echo "Você pode encontrá-lo em:"
    echo "  - Menu de aplicações > Escritório"
    echo ""
    echo "Para desinstalar, execute: ./uninstall_desktop.sh"
else
    echo "❌ Erro ao instalar o atalho."
    exit 1
fi
