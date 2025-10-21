# Text Helper AI - Suíte Completa de Processamento de Texto

Um aplicativo Python avançado que oferece 12 funcionalidades de processamento de texto usando ChatGPT, com interface gráfica moderna e menu flutuante sempre visível.

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

## 🎨 Interface Moderna

- **Menu Flutuante**: Sempre visível em cima de outras janelas
- **Arrastável**: Pode ser movido para qualquer posição
- **Organizado por Categorias**: Interface intuitiva com scroll
- **Loading Animado**: Feedback visual durante processamento
- **Diálogos Ricos**: Comparação entre texto original e resultado
- **Captura Inteligente**: Prioriza texto selecionado sobre clipboard

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

### 2. Abrir Menu Flutuante

- Clique em **"🚀 Mostrar Menu Flutuante"** na interface principal
- O menu aparecerá sempre visível em cima de outras janelas
- Arraste o menu para qualquer posição da tela

### 3. Processar Texto

**Opção A - Texto Selecionado (Recomendado):**
1. **Selecione** o texto que deseja processar em qualquer aplicativo
2. **Clique** na função desejada no menu flutuante
3. **Aguarde** o processamento com feedback visual
4. **Cole** o resultado onde quiser (Ctrl+V)

**Opção B - Clipboard:**
1. **Copie** o texto (Ctrl+C) em qualquer aplicativo
2. **Clique** na função desejada no menu flutuante
3. **Aguarde** o processamento com feedback visual
4. **Cole** o resultado onde quiser (Ctrl+V)

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
scripts/
├── text_shortener.py    # Aplicativo principal
├── requirements.txt     # Dependências Python
├── install.sh          # Script de instalação
└── README.md           # Documentação
```

### Dependências

- `pynput`: Captura de atalhos globais
- `openai`: Integração com API do ChatGPT
- `pyperclip`: Manipulação do clipboard
- `tkinter`: Interface gráfica (incluído no Python)
- `configparser`: Gerenciamento de configurações

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação
