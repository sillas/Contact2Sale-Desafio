# Cliente MCP \[Cars] – Contact 2 Sale

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)

## Sumário

* [Pré-requisitos](#pré-requisitos)
* [Descrição](#descrição)
* [Instalação](#instalação)
* [Estrutura do Projeto](#estrutura-do-projeto)

## Pré-requisitos

* Python 3.10 ou superior
* Chave de API válida da Anthropic com créditos disponíveis:
  [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

## Descrição

Este projeto é um cliente MCP que atua como um agente inteligente (chatbot) para simular o atendimento de uma concessionária de veículos.
O agente é integrado com um modelo de linguagem natural (LLM) da Anthropic para fornecer respostas contextualizadas e realistas.

Por padrão, o modelo utilizado nos testes foi o `Claude-Haiku-3.5`, mas é possível utilizar qualquer outro modelo da Anthropic alterando a variável no arquivo `.env`.

Também é possível integrar com APIs de outros provedores de IA, desde que seja implementado o provedor correspondente na arquitetura do projeto.

## Instalação

### 1. Preparação do servidor MCP

Certifique-se de que o servidor MCP esteja corretamente configurado, com o MongoDB em execução e devidamente populado com os dados necessários.
Consulte o README do servidor para mais detalhes.

### 2. Ambiente do cliente

No diretório do cliente:

```bash
# 2.1 Ative o ambiente virtual
$ source .venv/Scripts/activate  # (Linux/macOS: .venv/bin/activate)

# 2.2 Instale as dependências
$ uv sync --locked

# 2.3 Execute o cliente
$ uv run main.py
```

### 3. Logs

Os logs da execução serão salvos em um arquivo localizado na raiz do projeto, permitindo a análise posterior das interações.

## Estrutura do Projeto
```
cars-server/
├── src/
│   ├── client/
│   │   ├── providers/
│   │   │   └──antropic_llm_provider.py
│   │   ├── strings/
│   │   │   ├── messages.py
│   │   │   └──prompts.py
│   │   ├── chat_handler.py
│   │   ├── llm.py
│   │   ├── mcp_client.py
│   │   └── message.py
│   ├── interfaces/
│   │   └── llm_interface.py
│   └── config/
│       └── settings.py
├── main.py
└── README.md
```