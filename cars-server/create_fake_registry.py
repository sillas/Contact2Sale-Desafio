from faker import Faker
import random

fake = Faker()

car_data = {
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

print(car_data)
