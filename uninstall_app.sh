#!/bin/bash

# Script de Desinstalação do Text Helper IA
# Este script remove o aplicativo do sistema

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

# Função para confirmar desinstalação
confirm_uninstall() {
    print_message "===============================================" $RED
    print_message "    DESINSTALADOR DO TEXT HELPER IA" $RED
    print_message "===============================================" $RED
    print_message "" $NC
    print_message "Este script irá remover o Text Helper IA do sistema." $YELLOW
    print_message "" $NC
    print_message "Os seguintes itens serão removidos:" $BLUE
    print_message "- Arquivo .desktop do menu de aplicações" $NC
    print_message "- Atalho da área de trabalho (se existir)" $NC
    print_message "- Cache de aplicações" $NC
    print_message "" $NC
    print_message "Os seguintes itens NÃO serão removidos:" $YELLOW
    print_message "- Arquivos do aplicativo (pasta atual)" $NC
    print_message "- Ambiente virtual Python" $NC
    print_message "- Configurações do usuário" $NC
    print_message "" $NC
    
    read -p "Deseja continuar com a desinstalação? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        print_message "Desinstalação cancelada." $YELLOW
        exit 0
    fi
}

# Função para remover arquivo .desktop
remove_desktop_file() {
    print_message "Removendo arquivo .desktop..." $BLUE
    
    if [ -f "$HOME/.local/share/applications/text-helper-ia.desktop" ]; then
        rm "$HOME/.local/share/applications/text-helper-ia.desktop"
        print_message "Arquivo .desktop removido!" $GREEN
    else
        print_message "Arquivo .desktop não encontrado." $YELLOW
    fi
}

# Função para remover atalho da área de trabalho
remove_desktop_shortcut() {
    print_message "Removendo atalho da área de trabalho..." $BLUE
    
    if [ -f "$HOME/Desktop/text-helper-ia.desktop" ]; then
        rm "$HOME/Desktop/text-helper-ia.desktop"
        print_message "Atalho da área de trabalho removido!" $GREEN
    else
        print_message "Atalho da área de trabalho não encontrado." $YELLOW
    fi
}

# Função para atualizar cache de aplicações
update_desktop_cache() {
    print_message "Atualizando cache de aplicações..." $BLUE
    
    if command -v update-desktop-database >/dev/null 2>&1; then
        update-desktop-database ~/.local/share/applications
        print_message "Cache de aplicações atualizado!" $GREEN
    else
        print_message "Comando update-desktop-database não encontrado." $YELLOW
    fi
}

# Função para verificar desinstalação
verify_uninstall() {
    print_message "Verificando desinstalação..." $BLUE
    
    local errors=0
    
    # Verificar se o arquivo .desktop foi removido
    if [ -f "$HOME/.local/share/applications/text-helper-ia.desktop" ]; then
        print_message "AVISO: Arquivo .desktop ainda existe!" $YELLOW
        errors=$((errors + 1))
    fi
    
    # Verificar se o atalho da área de trabalho foi removido
    if [ -f "$HOME/Desktop/text-helper-ia.desktop" ]; then
        print_message "AVISO: Atalho da área de trabalho ainda existe!" $YELLOW
        errors=$((errors + 1))
    fi
    
    if [ $errors -eq 0 ]; then
        print_message "Desinstalação verificada com sucesso!" $GREEN
        return 0
    else
        print_message "Desinstalação concluída com avisos." $YELLOW
        return 1
    fi
}

# Função para mostrar informações pós-desinstalação
show_post_uninstall_info() {
    print_message "" $NC
    print_message "===============================================" $GREEN
    print_message "    DESINSTALAÇÃO CONCLUÍDA!" $GREEN
    print_message "===============================================" $GREEN
    print_message "" $NC
    print_message "O Text Helper IA foi removido do sistema!" $GREEN
    print_message "" $NC
    print_message "O que foi removido:" $BLUE
    print_message "- Entrada no menu de aplicações" $NC
    print_message "- Atalho da área de trabalho" $NC
    print_message "- Cache de aplicações atualizado" $NC
    print_message "" $NC
    print_message "O que permaneceu:" $YELLOW
    print_message "- Arquivos do aplicativo (pasta atual)" $NC
    print_message "- Ambiente virtual Python" $NC
    print_message "- Configurações do usuário" $NC
    print_message "" $NC
    print_message "Para remover completamente:" $BLUE
    print_message "- Delete a pasta do projeto" $NC
    print_message "- Delete a pasta text_helper_ia_env" $NC
    print_message "- Delete arquivos de configuração em ~/.config/text-helper-ia/" $NC
    print_message "" $NC
}

# Função principal
main() {
    # Confirmar desinstalação
    confirm_uninstall
    
    # Remover arquivo .desktop
    remove_desktop_file
    
    # Remover atalho da área de trabalho
    remove_desktop_shortcut
    
    # Atualizar cache de aplicações
    update_desktop_cache
    
    # Verificar desinstalação
    if verify_uninstall; then
        show_post_uninstall_info
    else
        print_message "Desinstalação concluída com avisos." $YELLOW
    fi
}

# Executar função principal
main "$@"
