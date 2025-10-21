#!/bin/bash

# Launcher script for Text Helper IA
# This script ensures the application runs with the correct Python environment

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the application directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "text_helper_ia_env" ]; then
    echo "Ativando ambiente virtual..."
    source text_helper_ia_env/bin/activate
    python text_helper_ia.py "$@"
else
    echo "Ambiente virtual não encontrado. Executando com Python do sistema..."
    python3 text_helper_ia.py "$@"
fi
