# Text Helper IA

Uma suíte completa de processamento de texto com inteligência artificial, oferecendo 14 funções diferentes para melhorar, transformar e analisar textos usando a API do OpenAI.

## 🚀 Características

- **14 Funções de Processamento**: Encurtar, melhorar, corrigir, resumir, traduzir e muito mais
- **Interface Moderna**: Interface gráfica intuitiva e responsiva
- **Processamento Inteligente**: Detecta automaticamente texto selecionado ou usa área de transferência
- **Substituição Automática**: Substitui texto selecionado automaticamente quando possível
- **Configuração Flexível**: Configurações personalizáveis para modelo, tokens e comportamento
- **Logging Completo**: Sistema de logs para monitoramento e debugging
- **Arquitetura Modular**: Código bem estruturado e fácil de manter

## 🛠️ Funções Disponíveis

| Função | Descrição | Emoji |
|--------|-----------|-------|
| **Encurtar** | Reduz o texto mantendo informações essenciais | 📝 |
| **Melhorar** | Melhora clareza e estrutura do texto | ✨ |
| **Corrigir** | Corrige erros ortográficos e gramaticais | ✅ |
| **Resumir** | Cria resumos concisos destacando pontos principais | 📋 |
| **Informal** | Transforma em linguagem casual e descontraída | 😊 |
| **Formal** | Transforma em linguagem formal e profissional | 👔 |
| **Traduzir (EN)** | Traduz do português para inglês | 🇺🇸 |
| **Traduzir (PT)** | Traduz do inglês para português | 🇧🇷 |
| **Expandir** | Adiciona detalhes e exemplos ao texto | 📈 |
| **Criativo** | Reescreve de forma mais envolvente | 🎨 |
| **Técnico** | Transforma em linguagem técnica e precisa | 🔧 |
| **Emojis** | Adiciona emojis relevantes ao texto | 😀 |
| **Analisar** | Fornece insights sobre tom e estrutura | 🔍 |
| **Reescrever** | Reescreve com abordagem diferente | ✏️ |

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Chave de API do OpenAI
- Sistema operacional Linux (testado em Debian/Ubuntu)

## 🔧 Instalação

### Instalação como Aplicativo do Sistema (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/text-helper-ia.git
cd text-helper-ia

# Execute o script de instalação do aplicativo
chmod +x install_app.sh
./install_app.sh
```

Este método irá:
- Instalar todas as dependências do sistema
- Configurar o ambiente virtual Python
- Criar um atalho no menu de aplicações
- Criar um atalho na área de trabalho (se disponível)
- Integrar o aplicativo com o sistema operacional

### Instalação Manual

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/text-helper-ia.git
cd text-helper-ia

# Crie um ambiente virtual
python3 -m venv text_helper_ia_env
source text_helper_ia_env/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Desinstalação

```bash
# Para remover o aplicativo do sistema
./uninstall_app.sh
```

## ⚙️ Configuração

### 1. Configurar Chave da API OpenAI

```bash
# Execute o aplicativo em modo de configuração
python3 text_helper_ia.py --config
```

Ou use a interface gráfica:
1. Execute o aplicativo
2. Clique em "⚙️ Configurações"
3. Insira sua chave de API do OpenAI
4. Configure outros parâmetros conforme necessário

### 2. Configurações Disponíveis

- **Modelo**: gpt-3.5-turbo (padrão) ou gpt-4
- **Max Tokens**: Limite de tokens por resposta (padrão: 300)
- **Temperatura**: Criatividade da IA (padrão: 0.3)
- **Timeout**: Tempo limite para requisições (padrão: 30s)
- **Auto-cópia**: Copia resultado automaticamente para área de transferência
- **Auto-substituição**: Substitui texto selecionado automaticamente

## 🚀 Como Usar

### Método 1: Menu de Aplicações (Recomendado)

Após a instalação, você pode executar o aplicativo de três formas:

1. **Menu de Aplicações**: Procure por "Text Helper IA" no menu de aplicações do seu sistema
2. **Atalho da Área de Trabalho**: Clique no ícone na área de trabalho
3. **Linha de Comando**: Execute `./launcher.sh` no diretório do projeto

### Método 2: Interface Gráfica

1. **Selecione texto** em qualquer aplicativo
2. **Clique na função desejada** na interface
3. **Aguarde o processamento** (diálogo de carregamento)
4. **Visualize o resultado** no diálogo de sucesso
5. **O texto processado** será copiado automaticamente ou substituído

### Método 3: Linha de Comando

```bash
# Configurar
python3 text_helper_ia.py --config

# Executar
python3 text_helper_ia.py
```

## 📁 Estrutura do Projeto

```
text-helper-ia/
├── src/                    # Código fonte principal
│   ├── app.py             # Classe principal da aplicação
│   ├── config.py          # Gerenciamento de configurações
│   ├── ia_client.py       # Cliente OpenAI
│   ├── text_processor.py  # Processamento de texto e clipboard
│   ├── logger.py          # Sistema de logging
│   └── ui/                # Interface gráfica
│       ├── main_window.py # Janela principal
│       └── dialogs.py     # Diálogos modais
├── tests/                 # Testes unitários
├── requirements.txt       # Dependências Python
├── install_app.sh        # Script de instalação do aplicativo
├── uninstall_app.sh      # Script de desinstalação
├── launcher.sh           # Script launcher para execução
├── text-helper-ia.desktop # Arquivo .desktop para integração
├── icon.png              # Ícone do aplicativo
├── text_helper_ia.py     # Ponto de entrada
└── README.md             # Este arquivo
```

## 🔧 Dependências

- **pynput**: Captura de teclado e mouse
- **openai**: Cliente oficial da API OpenAI
- **pyperclip**: Gerenciamento da área de transferência
- **typing-extensions**: Extensões de tipagem

## 🧪 Testes

```bash
# Execute os testes
python3 run_tests.py
```

## 📝 Logs

Os logs são salvos em `~/.text_helper_ia.log` e incluem:
- Informações de inicialização
- Processamento de textos
- Erros e avisos
- Configurações aplicadas

## 🎯 Casos de Uso

- **Escritores**: Melhorar clareza e estilo de textos
- **Estudantes**: Resumir e traduzir materiais de estudo
- **Profissionais**: Corrigir e formalizar comunicações
- **Desenvolvedores**: Documentar código de forma técnica
- **Criadores de Conteúdo**: Adicionar emojis e tornar textos mais envolventes

## 🐛 Solução de Problemas

### Erro: "OpenAI client not configured"
- Execute `python3 text_helper_ia.py --config` para configurar sua chave de API

### Erro: "No text found"
- Selecione texto antes de usar o aplicativo ou copie algo para a área de transferência

### Erro: "Text processing already in progress"
- Aguarde o processamento atual terminar antes de iniciar uma nova operação

### Problemas de Permissão
- Certifique-se de que o aplicativo tem permissão para acessar a área de transferência
- Em alguns sistemas, pode ser necessário executar com privilégios elevados

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- OpenAI pela API GPT
- Comunidade Python pelos pacotes utilizados
- Contribuidores e usuários do projeto

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/text-helper-ia/issues)
- **Discussions**: [GitHub Discussions](https://github.com/seu-usuario/text-helper-ia/discussions)

---

**Desenvolvido com ❤️ para facilitar o processamento de texto com IA**