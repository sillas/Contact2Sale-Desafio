import os
from os.path import dirname, abspath
from typing import Any, Literal

from src.car_repository import find_cars, create_pdf
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


def save_as_pdf(title: str, content: str) -> str:
    """Generates a PDF file with the specified title and content, saving it to a designated path.

    Args:
        title (str): The title for the document and file, with a maximum of 150 characters.
        content (str): The pure text content to be saved in the file.

    Return:
        str: Returns a message indicating the location where the PDF was saved.
    """
    save_path = os.getenv('SAVE_PATH')

    if (not save_path):
        save_path = dirname(dirname(abspath(__file__)))

    result_path = create_pdf(title, content, save_path)

    return f"PDF file saved to {result_path}"
