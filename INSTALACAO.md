# 🚀 Instalação Rápida - Text Helper IA

## Instalação como Aplicativo do Sistema

### 1. Execute o Script de Instalação

```bash
./install_app.sh
```

Este script irá:
- ✅ Instalar todas as dependências do sistema
- ✅ Configurar o ambiente virtual Python
- ✅ Criar atalho no menu de aplicações
- ✅ Criar atalho na área de trabalho (se disponível)
- ✅ Integrar com o sistema operacional

### 2. Como Executar

Após a instalação, você pode executar o aplicativo de três formas:

1. **Menu de Aplicações**: Procure por "Text Helper IA"
2. **Atalho da Área de Trabalho**: Clique no ícone
3. **Linha de Comando**: Execute `./launcher.sh`

### 3. Primeira Execução

1. Execute o aplicativo
2. Configure sua chave de API do OpenAI quando solicitado
3. O aplicativo criará os arquivos de configuração automaticamente

### 4. Desinstalação

```bash
./uninstall_app.sh
```

## Arquivos Criados

- `install_app.sh` - Script de instalação completo
- `uninstall_app.sh` - Script de desinstalação
- `launcher.sh` - Script launcher para execução
- `text-helper-ia.desktop` - Arquivo .desktop para integração
- `icon.png` - Ícone do aplicativo

## Verificação da Instalação

Para verificar se a instalação foi bem-sucedida:

```bash
# Verificar se o arquivo .desktop foi criado
ls -la ~/.local/share/applications/text-helper-ia.desktop

# Testar o launcher
./launcher.sh
```

## Solução de Problemas

### Erro: "Ambiente virtual não encontrado"
- Execute `./install_app.sh` novamente

### Erro: "Arquivo .desktop não encontrado"
- Verifique se o script de instalação foi executado com sucesso
- Execute `./install_app.sh` novamente

### Aplicativo não aparece no menu
- Execute: `update-desktop-database ~/.local/share/applications`
- Reinicie o sistema ou faça logout/login

## Suporte

Para mais informações, consulte o arquivo `README.md` completo.
