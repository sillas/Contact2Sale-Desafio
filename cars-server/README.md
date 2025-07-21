# Servidor MCP \[Cars] – Contact 2 Sale

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)

## Sumário

* [Pré-requisitos](#pré-requisitos)
* [Descrição](#descrição)
* [Instalação](#instalação)
* [Testes](#testes)
* [Exemplos de Queries](#exemplos-de-queries)
* [Estrutura do Projeto](#estrutura-do-projeto)

## Pré-requisitos

* Python 3.10 ou superior
* MongoDB instalado e em execução
* Claude Desktop (opcional, apenas para Windows)
* Chave de API da Anthropic com créditos disponíveis:
  [https://console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)

## Descrição

Este servidor MCP é responsável por consultar registros de automóveis armazenados em um banco de dados MongoDB e retornar os resultados ao cliente, seguindo o protocolo MCP.

### Parâmetros de entrada:

* `query` (dict): critérios de busca
* `limit` (int, opcional): número máximo de resultados
* `sort_by` (str, opcional): campo para ordenação
* `sort_dir` (`asc` | `desc`): direção da ordenação

## Instalação

### 0 - Instalar e iniciar o MongoDB

* Guia oficial de instalação:
  [https://www.mongodb.com/pt-br/docs/manual/installation/](https://www.mongodb.com/pt-br/docs/manual/installation/)

No Windows, para iniciar o serviço via terminal com permissões de administrador:

```bash
net start MongoDB
```

### 1 - Configurar ambiente Python

```bash
# Criar ambiente virtual
uv venv

# Ativar ambiente virtual
source .venv/bin/activate
```

### 2 - Instalar dependências

```bash
uv sync --locked
```

### 3 - Criar e popular o banco de dados

```bash
# Popular o banco de dados com dados de teste
uv run populate_db.py p

# Verificar dados no banco
uv run populate_db.py c
```

## Testes

### Integração com Claude Desktop (opcional – Windows)

> Para outros sistemas operacionais, veja:
> [https://modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)

1. Inicie o Claude Desktop. Vá em **Busca e Ferramentas** > **Gerenciar conectores** > **Desenvolvedor** > **Edit Config**.
2. Edite o arquivo `claude_desktop_config.json`, inserindo o seguinte conteúdo, substituindo `path/to` pelo caminho real da pasta `cars-server`:

```json
{
  "mcpServers": {
    "cars": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\c2s\\cars-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

3. Execute o servidor MCP:

```bash
uv run main.py
```

> Os logs serão salvos em `server_app.log`.

4. Reinicie o Claude Desktop. O servidor `cars` deve aparecer na aba de ferramentas.
5. Realize uma busca no chat relacionada a automóveis e confira os logs.

## Exemplos de Queries

```json
// Buscar carros da Toyota do ano de 2025
{
  "query": { "brand": "Toyota", "year": 2025 }
}

// Buscar carros elétricos ordenados por preço ascendente
{
  "query": { "fuel_type": "Electric" },
  "sort_by": "price",
  "sort_dir": "asc"
}
```

## Estrutura do Projeto

```
cars-server/
├── src/
│   ├── car_service.py
│   ├── car_repository.py
│   └── config/
│       ├── db_config.py
│       ├── logger.py
│       └── __init__.py
├── tests/
├── main.py
├── populate_db.py
└── README.md
```