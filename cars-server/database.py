from typing import List, Dict, Any
import operator
import re

from faker import Faker
import random

fake = Faker()

def car_data_gen():
    return {
        "brand": fake.company(),
        "model": fake.word().capitalize() + " " + fake.lexify(text='??'),
        "year": random.randint(2018, 2024),
        "engine": random.choice(["1.6L", "2.0L", "3.0L"]) + " " + random.choice(["Turbocharged Inline-4", "V6", "Inline-6"]),
        "fuel_type": random.choice(["Gasoline", "Diesel", "Ethanol", "Electric", "Hybrid"]),
        "color": fake.color_name(),
        "mileage_km": random.randint(0, 100000),
        "doors": random.choice([2, 3, 4, 5]),
        "transmission": random.choice(["4-Speed Manual", "5-Speed Manual", "6-Speed Manual", "8-Speed Automatic", "CVT"]),
        "segment": random.choice(["Sedan", "SUV", "Hatchback", "Coupe", "Pickup"]),
        "cargo_capacity_liters": random.randint(300, 700),
        "suspension": random.choice([
            "Independent MacPherson front, Multi-link rear",
            "Double wishbone front, Multi-link rear"
        ]),
        "drivetrain": random.choice(["Front-Wheel Drive", "Rear-Wheel Drive", "All-Wheel Drive"]),
        "fuel_consumption_km_per_l": round(random.uniform(8.0, 20.0), 1),
        "horsepower_hp": random.randint(100, 400),
        "price": random.randint(50000, 200000)
    }

cars_list = cars = [car_data_gen() for _ in range(10)]

def format(item: Any) -> str:
    return 'não informado' if item is None else item

def format_data(result:dict[str, Any]) -> str:
    if(not result):
        return 'sem resultados'
    
    response = ""
    for item in result:
        response += "---\n" \
            f"Modelo: {format(item['model'])}\n" \
            f"Marca {format(item['brand'])}\n" \
            f"Ano: {format(item['year'])}\n" \
            f"Preço R$: {format(item['price'])}\n" \
            f"Motorização: {format(item['engine'])}\n" \
            f"Combustível: {format(item['fuel_type'])}\n" \
            f"Cor: {format(item['color'])}\n" \
            f"Quilometragem: {format(item['mileage_km'])}\n" \
            f"Número de portas: {format(item['doors'])}\n" \
            f"Transmissão:  {format(item['transmission'])}\n" \
            f"Segmento: {format(item['segment'])}\n" \
            f"Capacidade de carga: {format(item['cargo_capacity_liters'])}\n" \
            f"Tipo de Suspensão: {item['suspension']}\n" \
            f"Tipo de Tração: {format(item['drivetrain'])}\n" \
            f"Consumo: {format(item['fuel_consumption_km_per_l'])}\n" \
            f"Potência do motor: {format(item['horsepower_hp'])}\n"
    
    response += "---\n"
    return response

def filter_cars(query: str) -> List[Dict[str, Any]]:
    # Operadores de comparação
    comparison_ops = {
        '==': operator.eq,
        '!=': operator.ne,
        '>=': operator.ge,
        '<=': operator.le,
        '>': operator.gt,
        '<': operator.lt,
        'in': lambda x, y: x in y
    }

    # Separadores lógicos
    logic_ops = {
        '|': lambda x, y: x or y,
        '&': lambda x, y: x and y,
    }

    # Divide a query em subcondições e operadores lógicos
    parts = re.split(r'(\s+[|&]\s+)', query)  # Mantém os operadores como partes separadas
    conditions = []

    for part in parts:
        part = part.strip()
        if part in logic_ops:
            conditions.append(part)
        else:
            # Identifica o operador de comparação
            for symbol in comparison_ops:
                if symbol in part:
                    field, value = map(str.strip, part.split(symbol, 1))
                    op = comparison_ops[symbol]

                    # Converte o valor
                    if value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    elif value.lower() == 'null':
                        value = None
                    else:
                        try:
                            value = float(value) if '.' in value else int(value)
                        except ValueError:
                            pass

                    # Função de verificação individual
                    def condition(car, field=field, value=value, op=op):
                        return op(car.get(field), value)

                    conditions.append(condition)
                    break
            else:
                raise ValueError(f"Invalid subquery: {part}")

    # Aplica as condições aos carros
    filtered = []
    for car in cars_list:
        result = conditions[0](car) if callable(conditions[0]) else None
        i = 1
        while i < len(conditions):
            op = logic_ops[conditions[i]]
            right = conditions[i + 1](car)
            result = op(result, right)
            i += 2
        if result:
            filtered.append(car)

    return format_data(filtered)

if __name__ == '__main__':
    res = filter_cars("year <= 2022")
    print(len(res), res)