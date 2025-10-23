#!/bin/bash

# Text Helper IA - Script de Instalação Completo
# Autor: Alexandre Riuti Wada
# Email: alexandre.rwada@gmail.com

echo "🚀 Text Helper IA - Instalação Completa"
echo "========================================"
echo ""

# Verificar se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Erro: Python 3 é necessário mas não está instalado."
    echo "   Instale Python 3 e tente novamente."
    exit 1
fi

# Verificar se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ Erro: pip3 é necessário mas não está instalado."
    echo "   Instale pip3 e tente novamente."
    exit 1
fi

echo "✅ Python 3 e pip3 encontrados"
echo ""

# Verificar e instalar dependências do sistema para notificações
echo "🔍 Verificando dependências do sistema para notificações..."

# Detectar distribuição Linux
if command -v apt &> /dev/null; then
    # Debian/Ubuntu
    if ! dpkg -l | grep -q libnotify-bin; then
        echo "📦 Instalando libnotify-bin..."
        sudo apt update && sudo apt install -y libnotify-bin
    fi
    if ! dpkg -l | grep -q python3-dbus; then
        echo "📦 Instalando python3-dbus..."
        sudo apt install -y python3-dbus
    fi
elif command -v dnf &> /dev/null; then
    # Fedora/CentOS
    if ! rpm -q libnotify &> /dev/null; then
        echo "📦 Instalando libnotify..."
        sudo dnf install -y libnotify
    fi
    if ! rpm -q python3-dbus &> /dev/null; then
        echo "📦 Instalando python3-dbus..."
        sudo dnf install -y python3-dbus
    fi
elif command -v pacman &> /dev/null; then
    # Arch Linux
    if ! pacman -Q libnotify &> /dev/null; then
        echo "📦 Instalando libnotify..."
        sudo pacman -S --noconfirm libnotify
    fi
    if ! pacman -Q python-dbus &> /dev/null; then
        echo "📦 Instalando python-dbus..."
        sudo pacman -S --noconfirm python-dbus
    fi
else
    echo "⚠️  Distribuição Linux não reconhecida. Certifique-se de instalar:"
    echo "   • libnotify-bin (ou libnotify)"
    echo "   • python3-dbus (ou python-dbus)"
fi

echo "✅ Dependências do sistema verificadas"
echo ""

# Perguntar se quer criar ambiente virtual
read -p "📦 Criar ambiente virtual? (recomendado) [S/n]: " create_venv
create_venv=${create_venv:-S}

if [[ $create_venv =~ ^[Ss]$ ]]; then
    echo "🔧 Criando ambiente virtual..."
    python3 -m venv text_helper_ia_env
    
    if [ $? -eq 0 ]; then
        echo "✅ Ambiente virtual criado com sucesso"
        echo "🔧 Ativando ambiente virtual..."
        source text_helper_ia_env/bin/activate
        
        echo "📥 Instalando dependências..."
        pip install -r requirements.txt
        
        if [ $? -eq 0 ]; then
            echo "✅ Dependências instaladas com sucesso"
        else
            echo "❌ Erro ao instalar dependências"
            exit 1
        fi
    else
        echo "❌ Erro ao criar ambiente virtual"
        exit 1
    fi
else
    echo "⚠️  Instalando dependências no Python do sistema..."
    pip3 install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✅ Dependências instaladas com sucesso"
    else
        echo "❌ Erro ao instalar dependências"
        exit 1
    fi
fi

echo ""

# Perguntar se quer instalar atalho no menu
read -p "🖥️  Instalar atalho no menu de aplicações? [S/n]: " install_desktop
install_desktop=${install_desktop:-S}

if [[ $install_desktop =~ ^[Ss]$ ]]; then
    echo "🖥️  Instalando atalho no menu..."
    
    # Perguntar tipo de instalação
    read -p "   Instalar para todos os usuários? (requer sudo) [s/N]: " global_install
    global_install=${global_install:-N}
    
    if [[ $global_install =~ ^[Ss]$ ]]; then
        echo "   Instalando globalmente..."
        sudo ./scripts/install_desktop_global.sh
    else
        echo "   Instalando para usuário atual..."
        ./scripts/install_desktop.sh
    fi
fi

echo ""

# Perguntar se quer instalar como pacote Python
read -p "📦 Instalar como pacote Python? [s/N]: " install_package
install_package=${install_package:-N}

if [[ $install_package =~ ^[Ss]$ ]]; then
    echo "📦 Instalando pacote Python..."
    
    if [[ $create_venv =~ ^[Ss]$ ]]; then
        source text_helper_ia_env/bin/activate
    fi
    
    python setup.py install --user
    
    if [ $? -eq 0 ]; then
        echo "✅ Pacote instalado com sucesso"
    else
        echo "❌ Erro ao instalar pacote"
    fi
fi

echo ""
echo "🎉 Instalação concluída!"
echo ""
echo "📋 Como usar:"
echo "   • Executar diretamente: python3 text_helper_ia.py"
if [[ $create_venv =~ ^[Ss]$ ]]; then
    echo "   • Com ambiente virtual: source text_helper_ia_env/bin/activate && python text_helper_ia.py"
fi
if [[ $install_desktop =~ ^[Ss]$ ]]; then
    echo "   • Pelo menu: Menu de Aplicações > Escritório > Text Helper IA"
fi
echo ""
echo "⚙️  Configuração:"
echo "   • Configure sua chave OpenAI: python3 text_helper_ia.py --config"
echo ""
echo "📚 Documentação:"
echo "   • README.md - Documentação principal"
echo "   • INSTALACAO_ATALHO.md - Como gerenciar atalhos"
echo "   • CONTRIBUTING.md - Como contribuir"
echo ""
echo "🗑️  Desinstalação:"
if [[ $install_desktop =~ ^[Ss]$ ]]; then
    if [[ $global_install =~ ^[Ss]$ ]]; then
        echo "   • Atalho: sudo ./scripts/uninstall_desktop_global.sh"
    else
        echo "   • Atalho: ./scripts/uninstall_desktop.sh"
    fi
fi
echo "   • Ambiente virtual: rm -rf text_helper_ia_env"
echo ""
echo "Obrigado por usar o Text Helper IA! 🚀"