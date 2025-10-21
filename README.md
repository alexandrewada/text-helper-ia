# Text Helper AI - Suíte Completa de Processamento de Texto

Um aplicativo Python avançado que oferece **14 funcionalidades** de processamento de texto usando ChatGPT, com interface gráfica moderna, arquitetura modular e menu flutuante sempre visível.

## 🆕 Versão 2.0 - Melhorias Implementadas

### ✨ **Novas Funcionalidades**
- **🔍 Analisar**: Fornece insights sobre tom, estrutura e clareza do texto
- **🔄 Reescrever**: Reescreve textos com abordagem diferente e mais envolvente
- **⌨️ Atalhos de Teclado**: Sistema completo de atalhos para todas as operações
- **🚀 Auto-substituição**: Substitui automaticamente texto selecionado

### 🏗️ **Arquitetura Melhorada**
- **Código Modular**: Organização em módulos separados para melhor manutenibilidade
- **Tratamento de Erros**: Sistema robusto de tratamento de erros e validações
- **Logging Avançado**: Sistema de logs com rotação automática e diferentes níveis
- **Configuração Flexível**: Sistema de configuração mais robusto e extensível
- **Sistema de Hotkeys**: Gerenciador de atalhos com suporte a múltiplas operações

### 🎨 **Interface Modernizada**
- **Design Atualizado**: Interface mais moderna com cores e estilos aprimorados
- **Melhor UX**: Diálogos mais informativos e responsivos
- **Animações**: Loading animations e feedback visual melhorados
- **Interface Simplificada**: Removido menu flutuante, foco na janela principal
- **Responsividade**: Interface que se adapta melhor a diferentes tamanhos de tela

### ⚡ **Performance e Qualidade**
- **Processamento Assíncrono**: Suporte para operações assíncronas
- **Validação de Texto**: Validação robusta de entrada com limpeza automática
- **Testes Unitários**: Suite de testes para garantir qualidade do código
- **Documentação**: Documentação completa e atualizada

## 🚀 Funcionalidades Principais

### 📝 **BÁSICO**
- **Encurtar**: Reduz texto mantendo informações essenciais
- **Melhorar**: Melhora clareza e estrutura do texto
- **Resumir**: Cria resumos concisos de textos longos
- **Expandir**: Adiciona detalhes e exemplos ao texto

### 🎭 **ESTILO**
- **Informal**: Transforma em linguagem casual e descontraída
- **Formal**: Transforma em linguagem profissional e culta
- **Criativo**: Reescreve de forma mais envolvente e dinâmica
- **Técnico**: Reescreve com terminologia técnica e precisa

### 🌍 **TRADUÇÃO**
- **→ Inglês**: Traduz do português para inglês
- **→ Português**: Traduz do inglês para português

### ✨ **EXTRAS**
- **Corrigir**: Corrige erros ortográficos e gramaticais
- **Emojis**: Adiciona emojis relevantes ao texto
- **Analisar**: Fornece insights sobre tom, estrutura e clareza
- **Reescrever**: Reescreve com abordagem diferente e mais envolvente

## 🎨 Interface Moderna

- **Menu Flutuante**: Sempre visível em cima de outras janelas
- **Arrastável**: Pode ser movido para qualquer posição
- **Organizado por Categorias**: Interface intuitiva com scroll
- **Loading Animado**: Feedback visual durante processamento
- **Diálogos Ricos**: Comparação entre texto original e resultado
- **Captura Inteligente**: Prioriza texto selecionado sobre clipboard
- **Design Responsivo**: Interface que se adapta a diferentes tamanhos
- **Temas**: Suporte para temas claro e escuro
- **Animações Suaves**: Transições e efeitos visuais aprimorados

## Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip3
- Chave de API do OpenAI

### Instalação Automática

```bash
# Execute o script de instalação
./install.sh
```

### Instalação Manual

```bash
# Instalar dependências
pip3 install -r requirements.txt

# Tornar o script executável
chmod +x text_shortener.py
```

## Configuração

### 1. Configurar API Key

```bash
./run_text_helper_ai.sh --config
```

Isso abrirá uma interface gráfica onde você pode:
- Inserir sua chave de API do OpenAI
- Escolher o modelo (gpt-3.5-turbo ou gpt-4)
- Definir o número máximo de tokens

### 2. Obter Chave de API

1. Acesse [OpenAI Platform](https://platform.openai.com/)
2. Crie uma conta ou faça login
3. Vá para "API Keys" no menu
4. Clique em "Create new secret key"
5. Copie a chave gerada

## 🎯 Como Usar

### 1. Executar o Aplicativo

```bash
./run_text_helper_ai.sh
```

### 2. Processar Texto

**Opção A - Texto Selecionado (Recomendado):**
1. **Selecione** o texto que deseja processar em qualquer aplicativo
2. **Use atalho** ou clique na função desejada na interface
3. **Aguarde** o processamento com feedback visual
4. **Texto é substituído** automaticamente

**Opção B - Clipboard:**
1. **Copie** o texto (Ctrl+C) em qualquer aplicativo
2. **Use atalho** ou clique na função desejada na interface
3. **Aguarde** o processamento com feedback visual
4. **Cole** o resultado onde quiser (Ctrl+V)

### 3. Atalhos de Teclado

```bash
# Encurtar texto selecionado
python3 text_helper_shortcuts.py shorten

# Melhorar texto selecionado
python3 text_helper_shortcuts.py improve

# Corrigir ortografia
python3 text_helper_shortcuts.py spellcheck

# Ver todas as opções
python3 text_helper_shortcuts.py help
```

### 4. Configurar Atalhos do Sistema

```bash
# Configurar atalhos globais
./setup_shortcuts.sh
```

### 4. Funcionalidades Disponíveis

- **📝 Encurtar**: Para textos longos
- **✨ Melhorar**: Para textos mal estruturados
- **✅ Corrigir**: Para textos com erros
- **📋 Resumir**: Para documentos extensos
- **😊 Informal**: Para tornar mais casual
- **👔 Formal**: Para tornar mais profissional
- **🇺🇸 Inglês**: Para traduzir para inglês
- **😀 Emojis**: Para tornar mais expressivo
- **E muito mais...**

## Configurações

O arquivo de configuração é salvo em `~/.text_shortener_config.ini`:

```ini
[DEFAULT]
openai_api_key = sua_chave_aqui
model = gpt-3.5-turbo
max_tokens = 150
```

### Parâmetros Configuráveis

- **openai_api_key**: Sua chave de API do OpenAI
- **model**: Modelo a ser usado (gpt-3.5-turbo, gpt-4)
- **max_tokens**: Número máximo de tokens na resposta (padrão: 150)

## Logs

Os logs são salvos em `~/.text_shortener.log` e também exibidos no terminal.

## Solução de Problemas

### Erro: "OpenAI client not configured"
- Execute `./run_text_shortener.sh --config` para configurar sua API key

### Atalho não funciona
- Certifique-se de que o aplicativo está rodando
- Verifique se não há conflitos com outros atalhos do sistema
- Teste em diferentes aplicativos

### Erro de API
- Verifique se sua chave de API está correta
- Confirme se você tem créditos disponíveis na conta OpenAI
- Verifique sua conexão com a internet

## Desenvolvimento

### Estrutura do Projeto

```
text-helper-ia/
├── src/                    # Código fonte modular
│   ├── __init__.py
│   ├── app.py             # Aplicativo principal
│   ├── config.py          # Gerenciamento de configuração
│   ├── logger.py          # Sistema de logging
│   ├── ai_client.py       # Cliente OpenAI
│   ├── text_processor.py  # Processamento de texto
│   └── ui/                # Interface do usuário
│       ├── __init__.py
│       ├── main_window.py # Janela principal
│       ├── floating_menu.py # Menu flutuante
│       └── dialogs.py     # Diálogos da interface
├── tests/                 # Testes unitários
│   ├── __init__.py
│   ├── test_config.py
│   └── test_text_processor.py
├── text_helper_ai.py      # Ponto de entrada
├── requirements.txt       # Dependências Python
├── install.sh            # Script de instalação
├── run_tests.py          # Executor de testes
└── README.md             # Documentação
```

### Dependências

- `pynput`: Captura de atalhos globais
- `openai`: Integração com API do ChatGPT
- `pyperclip`: Manipulação do clipboard
- `tkinter`: Interface gráfica (incluído no Python)
- `configparser`: Gerenciamento de configurações
- `typing-extensions`: Suporte para type hints avançados

### Executando Testes

```bash
# Executar todos os testes
python run_tests.py

# Executar testes específicos
python -m unittest tests.test_config
python -m unittest tests.test_text_processor
```

### Configurações Avançadas

O arquivo de configuração agora suporta mais opções:

```ini
[DEFAULT]
openai_api_key = sua_chave_aqui
model = gpt-3.5-turbo
max_tokens = 300
temperature = 0.3
timeout = 30
auto_copy = true
show_notifications = true
theme = light

[UI]
window_width = 600
window_height = 500
floating_menu_width = 250
floating_menu_height = 400
auto_close_delay = 10

[LOGGING]
level = INFO
file = ~/.text_helper_ai.log
max_size = 10485760
backup_count = 3
```

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação
