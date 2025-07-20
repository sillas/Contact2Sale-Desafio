from typing import Any, Literal
from src.car_repository import find_cars
from src.utils import format_output
from src.config.logger import logger


def search_cars(query: dict[str, Any], limit: int, sort_by: str, sort_dir: Literal['asc', 'desc']) -> str:
    """
    Executes a car query based on the provided input.

    If the query are successful, returns the result of the car query.
    If any error occurs during the process, returns an error message.

    Returns:
        str: The result of the car query, or an error message if the input is invalid or an error occurs.
    """
    try:
        cars = find_cars(query, limit, sort_by, sort_dir)
        return format_output(cars)

    except Exception as e:
        logger.exception(
            f"search_cars ERROR: {str(e)}, Input: {query}", exc_info=e)
        return f"Error! Input: {query}. Error: {str(e)}"
