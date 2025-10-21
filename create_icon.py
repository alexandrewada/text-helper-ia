#!/usr/bin/env python3
"""
Script para criar ícone do Text Helper IA
"""

import os

def create_icon():
    """Cria um ícone SVG simples para o aplicativo"""
    
    # Conteúdo do ícone SVG
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo circular -->
  <circle cx="32" cy="32" r="30" fill="#4A90E2" stroke="#2E5BBA" stroke-width="2"/>
  
  <!-- Ícone de texto/documento -->
  <rect x="18" y="16" width="28" height="32" rx="2" fill="white" stroke="#2E5BBA" stroke-width="1"/>
  
  <!-- Linhas de texto -->
  <line x1="22" y1="22" x2="42" y2="22" stroke="#2E5BBA" stroke-width="2" stroke-linecap="round"/>
  <line x1="22" y1="28" x2="38" y2="28" stroke="#2E5BBA" stroke-width="2" stroke-linecap="round"/>
  <line x1="22" y1="34" x2="40" y2="34" stroke="#2E5BBA" stroke-width="2" stroke-linecap="round"/>
  <line x1="22" y1="40" x2="36" y2="40" stroke="#2E5BBA" stroke-width="2" stroke-linecap="round"/>
  
  <!-- Símbolo de IA (círculo com pontos) -->
  <circle cx="50" cy="14" r="8" fill="#FF6B6B" stroke="white" stroke-width="2"/>
  <circle cx="47" cy="11" r="1.5" fill="white"/>
  <circle cx="53" cy="11" r="1.5" fill="white"/>
  <circle cx="50" cy="16" r="1" fill="white"/>
</svg>'''
    
    # Salvar o arquivo SVG
    with open('icon.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print("Ícone SVG criado: icon.svg")
    
    # Tentar converter para PNG se o ImageMagick estiver disponível
    try:
        import subprocess
        result = subprocess.run(['convert', 'icon.svg', 'icon.png'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("Ícone PNG criado: icon.png")
            os.remove('icon.svg')  # Remover SVG após conversão
        else:
            print("ImageMagick não disponível. Mantendo ícone SVG.")
    except FileNotFoundError:
        print("ImageMagick não encontrado. Mantendo ícone SVG.")
        # Criar um ícone PNG simples usando Python
        try:
            from PIL import Image, ImageDraw
            create_simple_png_icon()
        except ImportError:
            print("PIL não disponível. Usando ícone SVG.")

def create_simple_png_icon():
    """Cria um ícone PNG simples usando PIL"""
    from PIL import Image, ImageDraw
    
    # Criar imagem 64x64
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Fundo circular azul
    draw.ellipse([2, 2, 62, 62], fill=(74, 144, 226, 255), outline=(46, 91, 186, 255), width=2)
    
    # Retângulo branco (documento)
    draw.rounded_rectangle([18, 16, 46, 48], radius=2, fill=(255, 255, 255, 255), outline=(46, 91, 186, 255))
    
    # Linhas de texto
    for y in [22, 28, 34, 40]:
        draw.line([22, y, 42, y], fill=(46, 91, 186, 255), width=2)
    
    # Círculo vermelho (IA)
    draw.ellipse([42, 6, 58, 22], fill=(255, 107, 107, 255), outline=(255, 255, 255, 255), width=2)
    
    # Pontos no círculo IA
    draw.ellipse([45, 9, 47, 11], fill=(255, 255, 255, 255))
    draw.ellipse([51, 9, 53, 11], fill=(255, 255, 255, 255))
    draw.ellipse([49, 15, 51, 17], fill=(255, 255, 255, 255))
    
    # Salvar
    img.save('icon.png')
    print("Ícone PNG criado: icon.png")

if __name__ == "__main__":
    create_icon()
