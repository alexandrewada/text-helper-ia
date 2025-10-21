#!/bin/bash

# Text Helper IA Launcher Script
# Este script inicia o aplicativo Text Helper IA

# Diretório do aplicativo
APP_DIR="/home/alexandrewada/text-helper-ia"
VENV_DIR="$APP_DIR/text_helper_ia_env"

# Verificar se o ambiente virtual existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Erro: Ambiente virtual não encontrado em $VENV_DIR"
    echo "Execute o script de instalação primeiro: ./install.sh"
    exit 1
fi

# Ativar ambiente virtual
source "$VENV_DIR/bin/activate"

# Verificar se o Python está funcionando
if ! python3 --version > /dev/null 2>&1; then
    echo "Erro: Python3 não está disponível"
    exit 1
fi

# Navegar para o diretório do aplicativo
cd "$APP_DIR"

# Executar o aplicativo
echo "Iniciando Text Helper IA..."
python3 text_helper_ia.py

# Desativar ambiente virtual quando o aplicativo fechar
deactivate
