#!/bin/bash

# Text Helper IA - Script de Desinstalação Completa
# Autor: Alexandre Riuti Wada
# Email: alexandre.rwada@gmail.com

echo "🗑️  Text Helper IA - Desinstalação Completa"
echo "==========================================="
echo ""

# Perguntar se quer remover atalho do menu
if [ -f ~/.local/share/applications/text-helper-ia.desktop ] || [ -f /usr/share/applications/text-helper-ia.desktop ]; then
    read -p "🖥️  Remover atalho do menu de aplicações? [S/n]: " remove_desktop
    remove_desktop=${remove_desktop:-S}
    
    if [[ $remove_desktop =~ ^[Ss]$ ]]; then
        if [ -f /usr/share/applications/text-helper-ia.desktop ]; then
            echo "   Removendo atalho global..."
            sudo ./scripts/uninstall_desktop_global.sh
        else
            echo "   Removendo atalho do usuário..."
            ./scripts/uninstall_desktop.sh
        fi
    fi
fi

echo ""

# Perguntar se quer remover ambiente virtual
if [ -d "text_helper_ia_env" ]; then
    read -p "📦 Remover ambiente virtual? [S/n]: " remove_venv
    remove_venv=${remove_venv:-S}
    
    if [[ $remove_venv =~ ^[Ss]$ ]]; then
        echo "📦 Removendo ambiente virtual..."
        rm -rf text_helper_ia_env
        echo "✅ Ambiente virtual removido"
    fi
fi

echo ""

# Perguntar se quer remover pacote Python
read -p "📦 Remover pacote Python instalado? [s/N]: " remove_package
remove_package=${remove_package:-N}

if [[ $remove_package =~ ^[Ss]$ ]]; then
    echo "📦 Removendo pacote Python..."
    
    # Tentar desinstalar com pip
    if command -v pip3 &> /dev/null; then
        pip3 uninstall text-helper-ia -y 2>/dev/null
    fi
    
    # Remover arquivos do usuário
    rm -f ~/.local/bin/text_helper_ia.py
    rm -f ~/.local/bin/text_helper_ia_wrapper.py
    rm -rf ~/.local/lib/python*/site-packages/text_helper_ia*
    rm -rf ~/.local/lib/python*/site-packages/src
    
    echo "✅ Pacote Python removido"
fi

echo ""

# Perguntar se quer remover arquivos de configuração
read -p "⚙️  Remover arquivos de configuração? [s/N]: " remove_config
remove_config=${remove_config:-N}

if [[ $remove_config =~ ^[Ss]$ ]]; then
    echo "⚙️  Removendo arquivos de configuração..."
    rm -f ~/.text_helper_ia_config.ini
    rm -f ~/.text_helper_ia.log*
    echo "✅ Arquivos de configuração removidos"
fi

echo ""

# Perguntar se quer remover todo o projeto
read -p "⚠️  Remover todo o diretório do projeto? [s/N]: " remove_project
remove_project=${remove_project:-N}

if [[ $remove_project =~ ^[Ss]$ ]]; then
    echo "⚠️  Removendo diretório do projeto..."
    cd ..
    rm -rf text-helper-ia
    echo "✅ Projeto removido completamente"
    echo ""
    echo "🎉 Desinstalação completa!"
    exit 0
fi

echo ""
echo "🎉 Desinstalação concluída!"
echo ""
echo "📁 O diretório do projeto foi mantido."
echo "   Você pode removê-lo manualmente se desejar:"
echo "   rm -rf $(pwd)"
echo ""
echo "Obrigado por ter usado o Text Helper IA! 👋"
