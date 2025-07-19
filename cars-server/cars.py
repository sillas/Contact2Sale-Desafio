import logging
from typing import Any
# import httpx
from mcp.server.fastmcp import FastMCP
from database import filter_cars

logging.basicConfig(
    filename='server_output.log', 
    level=logging.INFO)

# Initialize FastMCP server
mcp = FastMCP("cars")

@mcp.tool()
async def get_cars(query: str) -> str:
    """Get cars from database.
    Args:
        query (str): query for search cars
    query components:
        attributes:
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
        operators: '==', '!=', '>=', '<=', '>', '<', in', '|', '&'
        format: 
            query: 'attribute operator value'
            query: 'attribute in [list or string]'
            query: 'query & query' or 'query | query'
    """

    logging.info(f"SERVER query: -{query}-")

    # get from DB
    return filter_cars(query)

if __name__ == "__main__":
    # Initialize and run the server
    logging.info("SERVER Start MCP Server")
    mcp.run(transport='stdio')

# uv run cars.py
# https://mariofilho.com/claude-anthropic-api-python/#gere-uma-api-key