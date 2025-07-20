from typing import Literal
from mcp.server.fastmcp import FastMCP

from src.config.logger import logger
from src.config.db_config import db
from src.car_service import search_cars

mcp = FastMCP("cars")


@mcp.tool()
async def get_cars(query: dict, limit: int = 0, sort_by: str = '', sort_dir: Literal['asc', 'desc'] = 'asc') -> str:
    """Get cars from MongoDB database.
    Args:
        query (dict): Dict query in JSON format for mongoDB, with -attributes- for search cars.
        limit (int): Limit the number of output. 0 = No limit.
        sort_by (str): Optional. Field name to sort the results by.
        sort_dir (str): Optional. Sorting direction. Use 'asc' for ascending or 'desc' for descending.
    Examples:
        # Correct format with escaped quotes:
        {`query`: `{\"year\": 2025}`}

        # Multiple fields example:
        {`query`: `{\"year\": 2025, \"brand\": \"Toyota\"}`}

        # Sort
        {`query`: `{\"year\": 2025}`, `sort_by`: `price`}
        {`query`: `{\"year\": 2025}`, `sort_by`: `price`, `sort_dir`: `asc`}

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
    """
    logger.info(f"SERVER Limit: {limit}, query: {type(query)} {query}-\n")
    return search_cars(query, limit, sort_by.strip(), sort_dir)


if __name__ == "__main__":

    if (db.collection is None):
        raise Exception("Serviço MongoDB não inicializado!")

    logger.info("SERVER Start MCP Server")
    mcp.run(transport='stdio')
