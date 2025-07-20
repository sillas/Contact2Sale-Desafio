from typing import Any, Literal
from pymongo import ASCENDING, DESCENDING
from pymongo.errors import OperationFailure, InvalidOperation, ConnectionFailure
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
