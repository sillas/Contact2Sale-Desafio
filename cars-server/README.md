# Servidor MCP [Cars] - Contact 2 Sale

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)

## Sumário
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Descrição](#descrição)
- [Instalação](#instalação)
- [Exemplos de Queries](#exemplos-de-queries)
- [Estrutura do Projeto](#estrutura-do-projeto)

## Pré-requisitos
- Python 3.10+
- MongoDB
- Claude Desktop (Opcional)

## Descrição
Este servidor MCP é responsável por buscar os registros de automóveis no banco de dados [MongoDB] 
de acordo com a query fornecida, e retornar para o cliente em uma string estruturada.

- Input: 
    query: dicioná'rio, 
    limit: inteiro = 0, 
    sort_by: string = '', 
    sort_dir: 'asc' | 'desc'

## Instalação
### 0 - Se ainda não tiver, instale o MongoDB localmente:

- MongoDB
[https://www.mongodb.com/pt-br/docs/manual/installation/]

E o ative no terminal como administrador, (se estiver no Windows), e se ainda não foi ativado:
`$ net start MongoDB` 

### 1 - Inicie um ambiente virtual e o ative:
`$ uv venv`
`$ source .venv/bin/activate`

### 2 - Instale as dependêcias do projeto (do servidor):
`$ uv pip install -r requirements.txt`

### 3 - Crie e popule o banco de dados MongoDB para testes:
`uv run populate_db.py p`

### 4 - Testes iniciais (opcional) com o servidor MCP e cliente Claude Desktop (Se estiver no Windows):
- [https://modelcontextprotocol.io/quickstart/server]

1. Inicie o Claude Desktop, acesse a opção `Busca e Ferramentas`, ao lado do botão para incluir anexos.
2. Selecione a opção `gerenciar conectores` e depois, acesse a aba `Desenvolvedor`, e depois, `Edit Config`;
3. Vai abrir o explorador de arquivos, e você deve localizar e abrir o arquivo `claude_desktop_config.json` para edição.
4. Insira o JSON abaixo neste arquivo, substituindo `path/to` pelo caminho absoluto até o diretório `cars-server`.
```Json
{
    "mcpServers": {
        "cars": {
            "command": "wsl.exe",
            "args": [
                "-d", "Ubuntu",
                "bash", "-lc",
                "cd path/to/c2s_test/cars-server && source .venv/bin/activate && uv run main.py"
            ]
        }
    }
}
```
5. Inicie o servidor MCP: No diretório rais do servidor (/cars-server), execute `$ uv run main.py`. Os logs aparecerão em `server_app.log`
6. Feche o cliente Claude (se estiver aberto) e abra novamente.
7. Se tudo correr bem, ao clicar novamente em `Busca e Ferramentas`, deve aparecer o nome do servidor nesta lista. No caso, [cars]
8. Para verificar o funcionamento, faça uma pesquisa aleatória no chat da Claude sobre os carros, e verifique nos logs se está de fato funcionando como o esperado.

## Exemplos de Queries
```json
// Buscar carros da Toyota de 2025
{
    "query": {"brand": "Toyota", "year": 2025}
}

// Buscar carros ordenados por preço
{
    "query": {"fuel_type": "Electric"},
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
├── tests/
├── main.py
├── populate_db.py
└── README.md
```