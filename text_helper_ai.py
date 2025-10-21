#!/usr/bin/env python3
"""
Text Helper AI - Suíte completa de processamento de texto com IA
Versão melhorada com arquitetura modular e interface moderna
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import main

if __name__ == "__main__":
    main()