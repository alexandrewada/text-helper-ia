# Text Helper IA

Uma aplicação desktop moderna para processamento de texto com inteligência artificial, desenvolvida em Python com interface gráfica intuitiva.

## 🚀 Funcionalidades

- **Encurtar Texto**: Reduz o tamanho mantendo o significado
- **Melhorar Texto**: Aprimora gramática e clareza
- **Tornar Informal**: Converte para linguagem casual
- **Tornar Formal**: Converte para linguagem formal
- **Corrigir Ortografia**: Corrige erros de escrita
- **Resumir**: Cria resumos concisos
- **Traduzir para Inglês**: Tradução automática
- **Adicionar Emojis**: Enriquece texto com emojis apropriados

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Chave de API do OpenAI
- Sistema operacional Linux, Windows ou macOS

## 🛠️ Instalação

### Instalação Automática (Recomendado)
```bash
# Clone o repositório
git clone https://github.com/alexandrewada/text-helper-ia.git
cd text-helper-ia

# Execute o script de instalação
chmod +x install.sh
./install.sh
```

O script de instalação irá:
- ✅ Verificar dependências do sistema
- ✅ Criar ambiente virtual (opcional)
- ✅ Instalar dependências Python
- ✅ Instalar atalho no menu (opcional)
- ✅ Instalar como pacote Python (opcional)

### Instalação Manual
```bash
# Clone o repositório
git clone https://github.com/alexandrewada/text-helper-ia.git
cd text-helper-ia

# Crie um ambiente virtual
python3 -m venv text_helper_ia_env
source text_helper_ia_env/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure sua chave de API
python text_helper_ia.py --config
```

## 🎯 Como Usar

### Executar a aplicação
```bash
python text_helper_ia.py
```

### Interface Principal
1. **Digite ou cole o texto** que deseja processar
2. **Selecione a operação** desejada
3. **Clique em "Processar"**
4. O resultado será **copiado automaticamente** para a área de transferência

### Atalhos de Teclado
- `Ctrl+Enter`: Processar texto
- `Ctrl+C`: Copiar resultado
- `Ctrl+V`: Colar texto

## 🏗️ Arquitetura

```
text-helper-ia/
├── src/                           # Código fonte principal
│   ├── app.py                    # Classe principal da aplicação
│   ├── config.py                 # Gerenciamento de configurações
│   ├── ia_client.py              # Cliente OpenAI
│   ├── text_processor.py         # Processamento de texto
│   ├── logger.py                 # Sistema de logs
│   └── ui/                       # Interface do usuário
│       ├── main_window.py        # Janela principal
│       └── dialogs.py            # Diálogos modais
├── tests/                        # Testes unitários
├── scripts/                      # Scripts de instalação
│   ├── install_desktop.sh        # Instalar atalho (usuário)
│   ├── install_desktop_global.sh # Instalar atalho (global)
│   ├── uninstall_desktop.sh      # Remover atalho (usuário)
│   └── uninstall_desktop_global.sh # Remover atalho (global)
├── .github/                      # Configurações do GitHub
│   ├── ISSUE_TEMPLATE/           # Templates de issues
│   ├── workflows/                # GitHub Actions
│   └── pull_request_template.md  # Template de PR
├── requirements.txt              # Dependências Python
├── setup.py                     # Script de instalação do pacote
├── text_helper_ia.py            # Script principal
├── text_helper_ia_launcher.sh   # Launcher para atalho
├── text-helper-ia.desktop       # Arquivo de atalho
├── install.sh                   # Script de instalação completa
├── uninstall.sh                 # Script de desinstalação completa
├── README.md                    # Documentação principal
├── CONTRIBUTING.md              # Guia de contribuição
├── LICENSE                      # Licença MIT
└── CHANGELOG.md                 # Histórico de mudanças
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
export OPENAI_API_KEY="sua_chave_aqui"
```

### Arquivo de Configuração
A aplicação salva configurações em `~/.config/text-helper-ia/config.json`

## 🧪 Testes

```bash
# Execute os testes
python -m pytest tests/

# Com cobertura
python -m pytest tests/ --cov=src
```

## 🗑️ Desinstalação

### Desinstalação Automática
```bash
# Execute o script de desinstalação
./uninstall.sh
```

### Desinstalação Manual
```bash
# Remover atalho do menu
./scripts/uninstall_desktop.sh

# Remover ambiente virtual
rm -rf text_helper_ia_env

# Remover pacote Python
pip uninstall text-helper-ia

# Remover arquivos de configuração
rm -f ~/.text_helper_ia_config.ini
rm -f ~/.text_helper_ia.log*
```

## 📦 Dependências

- **openai**: Cliente para API OpenAI
- **tkinter**: Interface gráfica (incluído no Python)
- **pyperclip**: Manipulação da área de transferência
- **plyer**: Notificações do sistema
- **pynput**: Captura de eventos do teclado

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia nosso [Guia de Contribuição](CONTRIBUTING.md) antes de enviar pull requests.

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Alexandre Riuti Wada**
- Email: alexandre.rwada@gmail.com
- GitHub: [@alexandrewada](https://github.com/alexandrewada)

## 🙏 Agradecimentos

- OpenAI pela API GPT
- Comunidade Python pelos recursos e bibliotecas
- Contribuidores e usuários do projeto

## 📊 Status do Projeto

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🐛 Reportar Bugs

Se encontrar algum bug, por favor:
1. Verifique se já existe uma [issue](https://github.com/alexandrewada/text-helper-ia/issues) sobre o problema
2. Se não existir, crie uma nova issue com:
   - Descrição detalhada do problema
   - Passos para reproduzir
   - Sistema operacional e versão do Python
   - Logs de erro (se houver)

## 💡 Sugestões de Melhorias

Tem uma ideia para melhorar o projeto? Abra uma [issue](https://github.com/alexandrewada/text-helper-ia/issues) com a tag "enhancement"!

## 📈 Roadmap

- [ ] Suporte a mais idiomas
- [ ] Integração com outras APIs de IA
- [ ] Modo escuro/claro
- [ ] Plugins personalizados
- [ ] API REST para integração
- [ ] Versão web

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub!
