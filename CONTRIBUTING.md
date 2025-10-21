# Guia de Contribuição

Obrigado por considerar contribuir com o Text Helper IA! Este documento fornece diretrizes para contribuir com o projeto.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Padrões de Código](#padrões-de-código)
- [Processo de Pull Request](#processo-de-pull-request)
- [Reportando Bugs](#reportando-bugs)
- [Sugerindo Melhorias](#sugerindo-melhorias)

## 🤝 Código de Conduta

Este projeto segue um código de conduta para garantir um ambiente acolhedor para todos os contribuidores. Ao participar, você concorda em manter este código.

### Nossos Compromissos

- Usar linguagem acolhedora e inclusiva
- Respeitar diferentes pontos de vista e experiências
- Aceitar críticas construtivas graciosamente
- Focar no que é melhor para a comunidade
- Demonstrar empatia com outros membros da comunidade

## 🚀 Como Contribuir

### Tipos de Contribuições

1. **🐛 Correção de Bugs**
   - Identificar e corrigir problemas existentes
   - Melhorar tratamento de erros
   - Otimizar performance

2. **✨ Novas Funcionalidades**
   - Adicionar novos tipos de processamento de texto
   - Melhorar interface do usuário
   - Adicionar atalhos de teclado

3. **📚 Documentação**
   - Melhorar README e documentação
   - Adicionar exemplos de uso
   - Traduzir documentação

4. **🧪 Testes**
   - Adicionar testes unitários
   - Melhorar cobertura de testes
   - Testes de integração

## 🛠️ Configuração do Ambiente

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub, depois clone
git clone https://github.com/SEU_USUARIO/text-helper-ia.git
cd text-helper-ia

# Adicione o repositório original como upstream
git remote add upstream https://github.com/alexandrewada/text-helper-ia.git
```

### 2. Ambiente de Desenvolvimento

```bash
# Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Instale dependências de desenvolvimento
pip install pytest pytest-cov black flake8 mypy
```

### 3. Configuração

```bash
# Configure sua chave de API OpenAI para testes
export OPENAI_API_KEY="sua_chave_de_teste"
```

## 📝 Padrões de Código

### Convenções de Nomenclatura

- **Funções e variáveis**: `snake_case`
- **Classes**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Arquivos**: `snake_case.py`

### Estrutura de Commits

Use commits semânticos seguindo o padrão:

```
tipo(escopo): descrição

Corpo do commit (opcional)

Rodapé (opcional)
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação
- `refactor`: Refatoração
- `test`: Testes
- `chore`: Manutenção

**Exemplos:**
```bash
feat(ui): adicionar modo escuro
fix(api): corrigir timeout de requisições
docs(readme): atualizar instruções de instalação
```

### Formatação de Código

```bash
# Formatar código com black
black src/ tests/

# Verificar estilo com flake8
flake8 src/ tests/

# Verificar tipos com mypy
mypy src/
```

### Estrutura de Arquivos

```
src/
├── app.py              # Classe principal
├── config.py           # Configurações
├── ia_client.py        # Cliente IA
├── text_processor.py   # Processamento
├── logger.py           # Logs
└── ui/                 # Interface
    ├── main_window.py
    └── dialogs.py

tests/
├── test_config.py
├── test_text_processor.py
└── test_ia_client.py
```

## 🔄 Processo de Pull Request

### 1. Criar Branch

```bash
# Atualize sua branch main
git checkout main
git pull upstream main

# Crie uma nova branch
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b fix/correcao-bug
```

### 2. Desenvolver

- Faça commits pequenos e frequentes
- Escreva testes para novas funcionalidades
- Mantenha o código limpo e documentado
- Execute testes antes de commitar

```bash
# Executar testes
python -m pytest tests/

# Verificar formatação
black --check src/ tests/
flake8 src/ tests/
```

### 3. Submeter Pull Request

1. Push sua branch para seu fork
```bash
git push origin feature/nova-funcionalidade
```

2. Abra um Pull Request no GitHub
3. Preencha o template de PR
4. Aguarde revisão e feedback

### Template de Pull Request

```markdown
## Descrição
Breve descrição das mudanças.

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Documentação

## Como Testar
Passos para testar as mudanças.

## Checklist
- [ ] Código segue padrões do projeto
- [ ] Testes foram adicionados/atualizados
- [ ] Documentação foi atualizada
- [ ] Não há conflitos de merge
```

## 🐛 Reportando Bugs

### Antes de Reportar

1. Verifique se o bug já foi reportado
2. Teste com a versão mais recente
3. Verifique se não é um problema de configuração

### Template de Bug Report

```markdown
**Descrição do Bug**
Descrição clara do problema.

**Passos para Reproduzir**
1. Vá para '...'
2. Clique em '...'
3. Veja o erro

**Comportamento Esperado**
O que deveria acontecer.

**Screenshots**
Se aplicável.

**Ambiente:**
- OS: [ex: Ubuntu 20.04]
- Python: [ex: 3.9.0]
- Versão: [ex: 1.0.0]

**Logs**
Cole logs de erro aqui.
```

## 💡 Sugerindo Melhorias

### Template de Feature Request

```markdown
**Funcionalidade Solicitada**
Descrição clara da funcionalidade.

**Problema que Resolve**
Qual problema esta funcionalidade resolve?

**Solução Proposta**
Como você imagina que deveria funcionar?

**Alternativas Consideradas**
Outras soluções que você considerou.

**Contexto Adicional**
Qualquer contexto adicional.
```

## 🧪 Testes

### Executando Testes

```bash
# Todos os testes
python -m pytest

# Com cobertura
python -m pytest --cov=src

# Teste específico
python -m pytest tests/test_config.py

# Com verbose
python -m pytest -v
```

### Escrevendo Testes

```python
import pytest
from src.config import Config

def test_config_initialization():
    """Testa inicialização da configuração."""
    config = Config()
    assert config is not None
    assert isinstance(config.get_api_key(), str)
```

## 📚 Documentação

### Atualizando Documentação

- README.md: Informações principais do projeto
- CONTRIBUTING.md: Este arquivo
- Docstrings: Documentação inline do código
- Comentários: Explicações complexas

### Padrão de Docstrings

```python
def process_text(self, text: str, operation: str) -> str:
    """
    Processa texto usando IA.
    
    Args:
        text: Texto a ser processado
        operation: Tipo de operação ('shorten', 'improve', etc.)
        
    Returns:
        Texto processado
        
    Raises:
        ValueError: Se texto for inválido
        APIError: Se houver erro na API
    """
```

## 🏷️ Versionamento

O projeto segue [Semantic Versioning](https://semver.org/):

- **MAJOR**: Mudanças incompatíveis
- **MINOR**: Funcionalidades compatíveis
- **PATCH**: Correções compatíveis

## 📞 Contato

- **Autor**: Alexandre Riuti Wada
- **Email**: alexandre.rwada@gmail.com
- **GitHub**: [@alexandrewada](https://github.com/alexandrewada)

## 🙏 Agradecimentos

Obrigado por contribuir com o Text Helper IA! Sua contribuição ajuda a tornar esta ferramenta melhor para todos os usuários.

---

**Lembre-se**: Contribuições não precisam ser apenas código. Relatórios de bugs, sugestões de melhorias, documentação e feedback são igualmente valiosos!
