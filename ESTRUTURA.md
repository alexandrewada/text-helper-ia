# Estrutura do Projeto - Text Helper IA

## 📁 Organização dos Arquivos

### 🎯 **Arquivos Principais**
- `text_helper_ia.py` - Script principal da aplicação
- `text_helper_ia_launcher.sh` - Launcher para atalho do menu
- `text-helper-ia.desktop` - Arquivo de atalho do menu
- `icon.png` - Ícone da aplicação

### 📦 **Scripts de Instalação**
- `install.sh` - **Script principal de instalação completa**
- `uninstall.sh` - **Script principal de desinstalação completa**
- `setup.py` - Script de instalação do pacote Python

### 📂 **Diretório `scripts/`**
- `install_desktop.sh` - Instalar atalho (usuário atual)
- `install_desktop_global.sh` - Instalar atalho (todos os usuários)
- `uninstall_desktop.sh` - Remover atalho (usuário atual)
- `uninstall_desktop_global.sh` - Remover atalho (todos os usuários)

### 🏗️ **Código Fonte (`src/`)**
- `app.py` - Classe principal da aplicação
- `config.py` - Gerenciamento de configurações
- `ia_client.py` - Cliente OpenAI
- `text_processor.py` - Processamento de texto
- `logger.py` - Sistema de logs
- `ui/` - Interface do usuário
  - `main_window.py` - Janela principal
  - `dialogs.py` - Diálogos modais

### 🧪 **Testes (`tests/`)**
- `test_config.py` - Testes de configuração
- `test_text_processor.py` - Testes de processamento

### 📚 **Documentação**
- `README.md` - Documentação principal
- `CONTRIBUTING.md` - Guia de contribuição
- `CHANGELOG.md` - Histórico de mudanças
- `CODE_OF_CONDUCT.md` - Código de conduta
- `LICENSE` - Licença MIT
- `INSTALACAO_ATALHO.md` - Guia de instalação de atalhos
- `ESTRUTURA.md` - Este arquivo

### ⚙️ **Configuração**
- `requirements.txt` - Dependências Python
- `.gitignore` - Exclusões do Git
- `.github/` - Configurações do GitHub
  - `ISSUE_TEMPLATE/` - Templates de issues
  - `workflows/` - GitHub Actions
  - `pull_request_template.md` - Template de PR

### 🔧 **Ambiente de Desenvolvimento**
- `text_helper_ia_env/` - Ambiente virtual Python (criado durante instalação)

## 🚀 **Como Usar**

### Instalação Rápida
```bash
./install.sh
```

### Desinstalação Completa
```bash
./uninstall.sh
```

### Execução Direta
```bash
python3 text_helper_ia.py
```

### Com Ambiente Virtual
```bash
source text_helper_ia_env/bin/activate
python text_helper_ia.py
```

## 📋 **Fluxo de Instalação**

1. **Verificação** - Checa Python 3 e pip
2. **Ambiente Virtual** - Cria ambiente virtual (opcional)
3. **Dependências** - Instala pacotes Python
4. **Atalho** - Instala atalho no menu (opcional)
5. **Pacote** - Instala como pacote Python (opcional)

## 🗑️ **Fluxo de Desinstalação**

1. **Atalho** - Remove atalho do menu
2. **Ambiente Virtual** - Remove ambiente virtual
3. **Pacote** - Remove pacote Python
4. **Configuração** - Remove arquivos de configuração
5. **Projeto** - Remove diretório completo (opcional)

## ✅ **Arquivos Limpos**

- ❌ Removidos arquivos temporários de build
- ❌ Removidos arquivos duplicados
- ❌ Removidos scripts desnecessários
- ✅ Organizados scripts em diretório `scripts/`
- ✅ Criados scripts principais de instalação/desinstalação
- ✅ Documentação atualizada
- ✅ Estrutura clara e profissional

## 🎯 **Próximos Passos**

1. **Testar instalação**: `./install.sh`
2. **Testar aplicação**: Executar pelo menu ou terminal
3. **Configurar API**: `python3 text_helper_ia.py --config`
4. **Usar aplicação**: Processar textos com IA

---

**Status**: ✅ Projeto organizado e pronto para uso!
