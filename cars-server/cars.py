from typing import Any
from config.db_config import db


def format_output(result: list[dict[str, Any]]) -> str:
    """
    Formats a list of car dictionaries into a human-readable string.

    Args:
        result: A list of dictionaries, where each dictionary represents a car.
    Returns:
        A string containing the formatted car information, with each car
        separated by '---'.  If a value is None, it is formatted as
        'não informado'.
    """

    def format(
        item, unidade=''): return 'não informado' if item is None else f"{item} {unidade}"

    response = ""
    for item in result:
        response += "---\n" \
            f"Modelo: {format(item['model'])}\n" \
            f"Marca {format(item['brand'])}\n" \
            f"Ano: {format(item['year'])}\n" \
            f"Preço R${format(item['price'])}\n" \
            f"Motorização: {format(item['engine'])}\n" \
            f"Combustível: {format(item['fuel_type'])}\n" \
            f"Cor: {format(item['color'])}\n" \
            f"Quilometragem: {format(item['mileage_km'], 'km')}\n" \
            f"Número de portas: {format(item['doors'], 'portas')}\n" \
            f"Transmissão:  {format(item['transmission'])}\n" \
            f"Segmento: {format(item['segment'])}\n" \
            f"Capacidade de carga: {format(item['cargo_capacity_liters'], 'kg')}\n" \
            f"Tipo de Suspensão: {item['suspension']}\n" \
            f"Tipo de Tração: {format(item['drivetrain'])}\n" \
            f"Consumo: {format(item['fuel_consumption_km_per_l'], 'L/h')}\n" \
            f"Potência do motor: {format(item['horsepower_hp'], 'hp')}\n"

    response += "---\n"
    return response


def query_cars(query: dict) -> str:
    """Retrieves cars from the database based on the provided query.
        Args:
            query (dict): A dictionary representing the query to filter cars.
        Returns:
            str: A formatted string containing the retrieved cars.
        """

    cars = db.collection.find(query)

    return format_output(cars)


# To test
if __name__ == "__main__":

    if (db.collection is None):
        raise Exception("MongoDB não inicializado!")

    q = {"year": {"$gte": 2020}}
    result = format_output(q)
    print(result)
