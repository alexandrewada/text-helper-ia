#!/bin/bash

# Text Helper IA Installation Script

echo "Installing Text Helper IA..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv text_helper_ia_env

# Install Python dependencies
echo "Installing Python dependencies..."
source text_helper_ia_env/bin/activate
pip install -r requirements.txt

# Make the scripts executable
chmod +x text_helper_ia.py
chmod +x run_text_helper_ia.sh

# Create desktop entry for easy access
DESKTOP_ENTRY="$HOME/.local/share/applications/text-helper-ai.desktop"
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_ENTRY" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Text Helper IA
Comment=IA-powered text processing suite with 14 functions using ChatGPT
Exec=$(pwd)/run_text_helper_ia.sh
Icon=accessories-text-editor
Terminal=false
Categories=Utility;TextEditor;
StartupNotify=true
EOF

echo "Installation completed!"
echo ""
echo "Usage:"
echo "1. Run './run_text_helper_ia.sh --config' to configure your OpenAI API key"
echo "2. Run './run_text_helper_ia.sh' to start the application"
echo "3. Select text or copy (Ctrl+C), then use the interface to process it"
echo ""
echo "The application offers 14 text processing functions with a modern interface."
