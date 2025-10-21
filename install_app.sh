#!/bin/bash

# Script de Instalação do Text Helper IA
# Este script instala o aplicativo no sistema Debian/Ubuntu

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_message() {
    echo -e "${2}${1}${NC}"
}

# Função para verificar se o comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para verificar se o usuário é root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_message "Este script não deve ser executado como root!" $RED
        print_message "Execute como usuário normal. O script pedirá senha quando necessário." $YELLOW
        exit 1
    fi
}

# Função para instalar dependências do sistema
install_system_dependencies() {
    print_message "Instalando dependências do sistema..." $BLUE
    
    # Atualizar lista de pacotes
    sudo apt update
    
    # Instalar dependências necessárias
    sudo apt install -y \
        python3 \
        python3-pip \
        python3-venv \
        imagemagick \
        desktop-file-utils \
        xdg-utils
    
    print_message "Dependências do sistema instaladas com sucesso!" $GREEN
}

# Função para criar ambiente virtual
setup_virtual_environment() {
    print_message "Configurando ambiente virtual Python..." $BLUE
    
    # Verificar se o ambiente virtual já existe
    if [ -d "text_helper_ia_env" ]; then
        print_message "Ambiente virtual já existe. Removendo..." $YELLOW
        rm -rf text_helper_ia_env
    fi
    
    # Criar novo ambiente virtual
    python3 -m venv text_helper_ia_env
    
    # Ativar ambiente virtual
    source text_helper_ia_env/bin/activate
    
    # Atualizar pip
    pip install --upgrade pip
    
    # Instalar dependências Python
    pip install -r requirements.txt
    
    print_message "Ambiente virtual configurado com sucesso!" $GREEN
}

# Função para instalar o aplicativo no sistema
install_application() {
    print_message "Instalando aplicativo no sistema..." $BLUE
    
    # Tornar o launcher executável
    chmod +x launcher.sh
    
    # Obter diretório atual
    APP_DIR=$(pwd)
    
    # Atualizar caminhos no arquivo .desktop
    sed -i "s|/home/alexandrewada/text-helper-ia|$APP_DIR|g" text-helper-ia.desktop
    
    # Copiar arquivo .desktop para aplicações do usuário
    mkdir -p ~/.local/share/applications
    cp text-helper-ia.desktop ~/.local/share/applications/
    
    # Atualizar cache de aplicações
    update-desktop-database ~/.local/share/applications
    
    # Tornar o arquivo .desktop executável
    chmod +x ~/.local/share/applications/text-helper-ia.desktop
    
    print_message "Aplicativo instalado no sistema!" $GREEN
}

# Função para criar atalho na área de trabalho
create_desktop_shortcut() {
    print_message "Criando atalho na área de trabalho..." $BLUE
    
    # Verificar se o diretório Desktop existe
    if [ -d "$HOME/Desktop" ]; then
        cp text-helper-ia.desktop "$HOME/Desktop/"
        chmod +x "$HOME/Desktop/text-helper-ia.desktop"
        print_message "Atalho criado na área de trabalho!" $GREEN
    else
        print_message "Diretório Desktop não encontrado. Pulando criação de atalho." $YELLOW
    fi
}

# Função para verificar instalação
verify_installation() {
    print_message "Verificando instalação..." $BLUE
    
    # Verificar se o ambiente virtual existe
    if [ ! -d "text_helper_ia_env" ]; then
        print_message "ERRO: Ambiente virtual não foi criado!" $RED
        return 1
    fi
    
    # Verificar se o arquivo .desktop foi instalado
    if [ ! -f "$HOME/.local/share/applications/text-helper-ia.desktop" ]; then
        print_message "ERRO: Arquivo .desktop não foi instalado!" $RED
        return 1
    fi
    
    # Verificar se o launcher é executável
    if [ ! -x "launcher.sh" ]; then
        print_message "ERRO: Launcher não é executável!" $RED
        return 1
    fi
    
    print_message "Instalação verificada com sucesso!" $GREEN
    return 0
}

# Função para mostrar informações pós-instalação
show_post_install_info() {
    print_message "" $NC
    print_message "===============================================" $GREEN
    print_message "    INSTALAÇÃO CONCLUÍDA COM SUCESSO!" $GREEN
    print_message "===============================================" $GREEN
    print_message "" $NC
    print_message "O Text Helper IA foi instalado com sucesso!" $GREEN
    print_message "" $NC
    print_message "Como usar:" $BLUE
    print_message "1. Procure por 'Text Helper IA' no menu de aplicações" $NC
    print_message "2. Ou clique no atalho na área de trabalho" $NC
    print_message "3. Ou execute: ./launcher.sh" $NC
    print_message "" $NC
    print_message "Primeira execução:" $YELLOW
    print_message "- Configure sua chave de API do OpenAI quando solicitado" $NC
    print_message "- O aplicativo criará os arquivos de configuração automaticamente" $NC
    print_message "" $NC
    print_message "Para desinstalar:" $BLUE
    print_message "- Execute: ./uninstall_app.sh" $NC
    print_message "" $NC
}

# Função principal
main() {
    print_message "===============================================" $BLUE
    print_message "    INSTALADOR DO TEXT HELPER IA" $BLUE
    print_message "===============================================" $BLUE
    print_message "" $NC
    
    # Verificar se não é root
    check_root
    
    # Verificar se estamos no diretório correto
    if [ ! -f "text_helper_ia.py" ] || [ ! -f "requirements.txt" ]; then
        print_message "ERRO: Execute este script no diretório do Text Helper IA!" $RED
        print_message "Certifique-se de que os arquivos text_helper_ia.py e requirements.txt estão presentes." $RED
        exit 1
    fi
    
    # Instalar dependências do sistema
    install_system_dependencies
    
    # Configurar ambiente virtual
    setup_virtual_environment
    
    # Instalar aplicativo
    install_application
    
    # Criar atalho na área de trabalho
    create_desktop_shortcut
    
    # Verificar instalação
    if verify_installation; then
        show_post_install_info
    else
        print_message "ERRO: Falha na verificação da instalação!" $RED
        exit 1
    fi
}

# Executar função principal
main "$@"
