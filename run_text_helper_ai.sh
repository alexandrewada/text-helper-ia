#!/bin/bash

# Script para executar o Text Helper AI

cd "$(dirname "$0")"

# Ativar ambiente virtual
source text_helper_ai_env/bin/activate

# Executar o aplicativo
python text_helper_ai.py "$@"
