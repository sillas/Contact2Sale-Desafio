# Desafio – Contact 2 Sale

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)

### Demonstração:
https://youtu.be/Bhy6K45URcE

## Descrição

Este projeto consiste na implementação de um sistema de atendimento via chat utilizando o padrão **Cliente-Servidor com o protocolo MCP (Model Context Protocol)**.

O sistema simula o atendimento de uma concessionária, permitindo que um agente de IA converse com o usuário, consulte uma base de dados de veículos e forneça informações relevantes.

A estrutura é composta por dois componentes principais:

* `cars-client`: Cliente MCP (chatbot)
* `cars-server`: Servidor MCP (consulta e geração de relatórios)

A comunicação entre cliente e servidor é feita via **MCP utilizando o transporte `stdio`**, ideal para ambiente local e seguro durante o desenvolvimento.

O projeto foi baseado na documentação oficial do protocolo MCP:
👉 [https://modelcontextprotocol.io](https://modelcontextprotocol.io)


OBSERVAÇÃO: Embora eu tenha adicionado alguns testes unitários, é evidente que eles não cobrem todo o projeto, pois isso levaria um tempo mais longo do que o aceitável para um Desafio para vaga de emprego.

## LLM utilizado

O modelo padrão utilizado nos testes foi o `Claude-Haiku-3.5` da Anthropic. Outros modelos podem ser utilizados, desde que seja implementado o provedor correspondente em:

```bash
cars-client/src/client/providers/
```

O prompt que instrui o agente a agir como um vendedor está localizado em:

```bash
cars-client/src/strings/prompts.py
```

## Logs

Logs de execução são gravados na raiz de cada serviço:

* Cliente: `cars-client/client_app.log`
* Servidor: `cars-server/server_app.log`

---

## Servidor MCP

### Ferramentas implementadas

#### 1. `get_cars`

Recebe queries estruturadas via MCP, realiza a busca no MongoDB e retorna os dados serializados.

* Banco de dados: **MongoDB** (pode ser substituído com modificações mínimas)
* Script de povoamento: `populate_db.py`

```bash
# Comandos disponíveis
uv run populate_db.py p  # Popula com 100 registros aleatórios
uv run populate_db.py c  # Exibe o número de registros
uv run populate_db.py e  # Apaga todos os registros
uv run populate_db.py d  # Remove a coleção inteira
```

#### 2. `save_to_file`

Gera um arquivo PDF com o conteúdo recebido e salva em um diretório definido no `.env` ou na raiz do projeto.

* Biblioteca usada: `fpdf`

---

## Cliente MCP

Simula um atendimento de concessionária, onde o usuário conversa com um agente que:

* Realiza consultas ao banco de dados via protocolo MCP
* Pode solicitar a geração de relatórios em PDF

> *Em um ambiente real, esses relatórios poderiam ser enviados por e-mail (funcionalidade não implementada).*

---

## Instalação

Instale a ferramenta [**uv**](https://astral.sh/blog/uv-intro/):

```bash
# MacOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Configuração dos ambientes

Em cada serviço (`cars-client` e `cars-server`), siga os passos descritos em seus respectivos `README.md`.

---

## Execução

Após configurar os ambientes virtuais:

```bash
# Ativar ambiente virtual (em cada diretório)
source .venv/Scripts/activate  # Linux/macOS: .venv/bin/activate
```

### Servidor MCP:

```bash
uv run main.py
```

### Cliente MCP:

```bash
uv run main.py
```