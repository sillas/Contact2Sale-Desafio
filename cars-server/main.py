from json import loads
from mcp.server.fastmcp import FastMCP
from config.logger import logger
from config.db_config import db

from cars import query_cars

# Initialize FastMCP server
mcp = FastMCP("cars")


@mcp.tool()
async def get_cars(query: str) -> str:
    """Get cars from MongoDB database.
    Args:
        query (str): String query in JSON format for mongoDB, with -attributes- for search cars.
    Examples:
        # Correct format with escaped quotes:
        {`query`: `{\\\"year\\\": 2025}`}

        # Multiple fields example:
        {`query`: `{\\\"year\\\": 2025, \\\"brand\\\": \\\"Toyota\\\"}`}

    Attributes:
        brand (str),
        model (str),
        year (int),
        price (float),
        engine (str),
        fuel_type (str),
        color (str),
        mileage_km (int),
        doors (int),
        transmissio (str),
        segment (str),
        cargo_capacity_liters (int),
        suspension (str),
        drivetrain (str),
        fuel_consumption_km_per_l (float),
        horsepower_hp (int)

    Note:
        The query must be properly escaped with double backslashes (\\\\) before quotes.
        Invalid format: {`query`: `{\"year\": 2025}`}
        Valid format: {`query`: `{\\\"year\\\": 2025}`}
    """
    logger.info(f"SERVER pre-query: -{type(query)} | {query}-\n")

    if ("'" in query):
        query = query.replace("'", '"')

    if ('\\' in query):
        query = query.replace('\\', '')

    try:
        query_dict = loads(query)
        logger.info(f"SERVER pos-query: -{type(query_dict)} | {query_dict}-\n")
        return query_cars(query_dict)

    except Exception as e:
        return f"O formato de entrada está inválido. Input: {query}. Erro: {str(e)}"


if __name__ == "__main__":

    if (db.collection is None):
        raise Exception("MongoDB não inicializado!")

    logger.info("SERVER Start MCP Server")
    mcp.run(transport='stdio')

# uv run main.py
# https://mariofilho.com/claude-anthropic-api-python/#gere-uma-api-key

# {
#     "mcpServers": {
#         "cars": {
#             "command": "wsl.exe",
#             "args": [
#                 "-d", "Ubuntu",
#                 "bash", "-lc",
#                 "cd ~/c2s_test/cars-server && source .venv/bin/activate && uv run main.py"
#             ]
#         }
#     }
# }
