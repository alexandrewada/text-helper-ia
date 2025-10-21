#!/usr/bin/env python3
"""
Text Helper IA - Suíte completa de processamento de texto com IA
Versão melhorada com arquitetura modular e interface moderna

Author: Alexandre Riuti Wada
Email: alexandre.rwada@gmail.com
GitHub: https://github.com/alexandrewada/text-helper-ia
License: MIT
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import main

if __name__ == "__main__":
    main()