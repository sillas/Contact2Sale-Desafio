import os
from typing import Any, Literal

from pymongo import ASCENDING, DESCENDING
from pymongo.errors import OperationFailure, InvalidOperation, ConnectionFailure

from fpdf import FPDF
from fpdf.enums import XPos, YPos

from src.config.logger import logger
from src.config.db_config import db


SORT_DIR = {
    'asc': ASCENDING,
    'desc': DESCENDING
}


def find_cars(query: dict[str, Any], limit: int, sort_by: str, sort_dir: Literal['asc', 'desc']) -> list[dict[str, Any]]:
    """
    Retrieves cars from the database based on the provided query.
    Returns:
        list: A list containing the retrieved cars.
    """

    try:
        cars = db.collection.find(query)

        if (sort_by):
            cars = cars.sort(sort_by, SORT_DIR[sort_dir])

        if (limit > 0):
            cars = cars.limit(limit)

        return cars

    except ConnectionFailure as e:
        raise ConnectionFailure(
            f"Falha na conexão com o banco de dados: {str(e)}")

    except OperationFailure as e:
        raise OperationFailure(f"Erro ao acessar o banco de dados: {str(e)}")

    except InvalidOperation as e:
        raise InvalidOperation(
            f"Operação inválida no banco de dados: {str(e)}")

    except ValueError as e:
        raise ValueError(f"Erro de validação: {str(e)}")

    except Exception as e:
        raise Exception(
            f"Erro inesperado ao consultar o banco de dados: {str(e)}")


def create_pdf(title: str, content: str, save_path: str) -> str:
    """
    Create a PDF file with the given title and content at the specified path.

    The PDF is saved to the path specified in the environment variable 'SAVE_PATH'.
    If 'SAVE_PATH' is not set, the PDF is saved to the project's root directory.
    The title is used as the filename for the PDF, with non-alphanumeric characters replaced by underscores.

    Args:
        title (str): The title of the PDF.
        content (str): The content of the PDF.
        save_path (str): The path where the PDF should be saved.
    Returns:
        str: A message indicating the path to which the PDF was saved.
    """

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)

        pdf.set_font(size=16, style='B')
        pdf.cell(
            w=0, h=10,
            text=title,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
            align='C'
        )
        pdf.ln(10)
        pdf.set_font(size=12)
        pdf.multi_cell(
            w=0, h=10,
            text=content,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT
        )

        safe_title = "".join(c if c.isalnum() else "_" for c in title)
        pdf_path = os.path.join(save_path, f"{safe_title}.pdf")
        pdf.output(pdf_path)

        return f"Saved to {pdf_path}"

    except Exception as e:
        err = f"Falha ao salvar em PDF. ERROR: {str(e)}"
        logger.exception(err, exc_info=e)
        return err
