from typing import Any, Literal
from pymongo import ASCENDING, DESCENDING
from src.config.db_config import db
from src.utils import format_output

SORT_DIR = {
    'asc': ASCENDING,
    'desc': DESCENDING
}


def find_cars(query: dict[str, Any], limit: int, sort_by: str, sort_dir: Literal['asc', 'desc']) -> str:
    """Retrieves cars from the database based on the provided query.
        Args:
            query (dict): A dictionary representing the query to filter cars.
        Returns:
            str: A formatted string containing the retrieved cars.
        """

    cars = db.collection.find(query)

    if (sort_by):
        cars = cars.sort(sort_by, SORT_DIR[sort_dir])

    if (limit > 0):
        cars = cars.limit(limit)

    return format_output(cars)
