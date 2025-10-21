# Como Criar Atalho no Menu do Debian

Este guia explica como criar um atalho para o Text Helper IA no menu de aplicações do Debian.

## 📋 Opções de Instalação

### 1. Instalação para Usuário Atual (Recomendado)

Para instalar o atalho apenas para o seu usuário:

```bash
./install_desktop.sh
```

**Vantagens:**
- Não requer privilégios de administrador
- Fácil de desinstalar
- Não afeta outros usuários

### 2. Instalação Global (Para Todos os Usuários)

Para instalar o atalho para todos os usuários do sistema:

```bash
sudo ./install_desktop_global.sh
```

**Vantagens:**
- Disponível para todos os usuários
- Instalação mais "profissional"

**Desvantagens:**
- Requer privilégios de administrador
- Mais difícil de desinstalar

## 🎯 Onde Encontrar o Atalho

Após a instalação, o Text Helper IA aparecerá no menu de aplicações em:

- **Menu de Aplicações > Escritório**
- **Menu de Aplicações > Utilitários** 
- **Menu de Aplicações > Educação**

## 🗑️ Como Desinstalar

### Desinstalar Atalho do Usuário
```bash
./uninstall_desktop.sh
```

### Desinstalar Atalho Global
```bash
sudo ./uninstall_desktop_global.sh
```

## 🔧 Arquivos Criados

### Instalação do Usuário
- `~/.local/share/applications/text-helper-ia.desktop`

### Instalação Global
- `/usr/share/applications/text-helper-ia.desktop`
- `/usr/share/pixmaps/text-helper-ia.png`

## 📝 Estrutura do Arquivo .desktop

O arquivo `text-helper-ia.desktop` contém:

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Text Helper IA
Comment=Assistente de processamento de texto com Inteligência Artificial
Exec=/home/alexandrewada/text-helper-ia/text_helper_ia_launcher.sh
Icon=/home/alexandrewada/text-helper-ia/icon.png
Terminal=false
StartupNotify=true
Categories=Office;TextEditor;Utility;Education;
Keywords=text;ai;openai;processamento;assistente;inteligencia;artificial;
StartupWMClass=TextHelperIA
MimeType=text/plain;
Path=/home/alexandrewada/text-helper-ia
```

## 🚀 Script Launcher

O arquivo `text_helper_ia_launcher.sh` é responsável por:

1. Ativar o ambiente virtual (se existir)
2. Executar a aplicação com o Python correto
3. Passar argumentos para a aplicação

## 🐛 Solução de Problemas

### Atalho não aparece no menu
```bash
# Atualizar banco de dados de aplicações
update-desktop-database ~/.local/share/applications

# Ou para instalação global
sudo update-desktop-database /usr/share/applications
```

### Aplicação não inicia pelo atalho
1. Verifique se o ambiente virtual existe
2. Verifique se o script launcher tem permissão de execução
3. Teste executando diretamente: `./text_helper_ia_launcher.sh`

### Ícone não aparece
1. Verifique se o arquivo `icon.png` existe
2. Para instalação global, verifique se o ícone foi copiado para `/usr/share/pixmaps/`

## 📱 Testando o Atalho

Após a instalação, você pode testar o atalho:

1. Abra o menu de aplicações
2. Procure por "Text Helper IA"
3. Clique no ícone para executar
4. A aplicação deve abrir normalmente

## 🔄 Atualizando o Atalho

Se você modificar o arquivo `.desktop`, reinstale o atalho:

```bash
# Para usuário atual
./install_desktop.sh

# Para instalação global
sudo ./install_desktop_global.sh
```

---

**Nota:** Este processo funciona em todas as distribuições baseadas em Debian, incluindo Ubuntu, Linux Mint, e outras.
