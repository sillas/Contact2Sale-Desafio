import sys
import random
from datetime import date
from pymongo.errors import CollectionInvalid
from faker import Faker
from src.config.db_config import db as mongo

fake = Faker()
today = date.today()
year = today.year
register_count = 10

alowed_colors = ["Red", "Blue", "Black", "White", "Silver", "Gray"]
alowed_fuel_type = ["Gasoline", "Diesel", "Ethanol", "Electric", "Hybrid"]
alowed_segment = ["Sedan", "SUV", "Hatchback", "Coupe", "Pickup"]
transmission = ["4-Speed Manual", "5-Speed Manual",
                "6-Speed Manual", "8-Speed Automatic", "CVT"]
suspension = ["McPherson", "Double Wishbone", "Multilink", "Solid Axle", "Torsion Bar",
              "Air Suspension", "Active Suspension", "Leaf Spring", "Semi-Independent", "Hydropneumatic"]
drivetrain = ["Front-Wheel Drive", "Rear-Wheel Drive", "All-Wheel Drive"]
brands = [
    "Buick", "Cadillac", "Chevrolet", "Dodge", "Ford", "GMC", "Jeep", "Lincoln", "Ram", "Tesla",
    "Fisker", "Rivian", "Lucid", "Honda", "Acura", "Toyota", "Lexus", "Nissan", "Infiniti",
    "Mazda", "Subaru", "Mitsubishi", "Suzuki", "Daihatsu", "Audi", "BMW", "Mercedes-Benz",
    "Porsche", "Volkswagen", "Opel", "Mini", "Smart", "Hyundai", "Kia", "Genesis", "Alfa Romeo",
    "Ferrari", "Fiat", "Lamborghini", "Maserati", "Pagani", "Jaguar", "Land Rover", "Bentley",
    "McLaren", "Lotus", "Aston Martin", "Rolls-Royce", "Citroën", "Peugeot", "Renault",
    "DS Automobiles", "Alpine", "Volvo", "Polestar", "BYD", "Geely", "Chery", "Great Wall",
    "NIO", "Xpeng", "Li Auto", "GAC", "VinFast", "Tata Motors", "Mahindra", "Skoda", "SEAT",
    "Cupra", "Lada", "Koenigsegg", "Bugatti", "Rimac"
]


def db_create():

    try:
        mongo.db.create_collection("cars_catalog", validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["brand", "model", "year", "price"],
                "properties": {
                    "brand": {"bsonType": "string"},
                    "model": {"bsonType": "string"},
                    "year": {"bsonType": "int", "minimum": 2018, "maximum": year + 1},
                    "price": {"bsonType": "double", "minimum": 50000},
                    "engine": {"bsonType": "string"},
                    "fuel_type": {"bsonType": "string", "enum": alowed_fuel_type},
                    "color": {"bsonType": "string", "enum": alowed_colors},
                    "segment": {"bsonType": "string", "enum": alowed_segment},
                    "transmission": {"bsonType": "string"},
                    "suspension": {"bsonType": "string"},
                    "drivetrain": {"bsonType": "string"},
                    "mileage_km": {"bsonType": "int"},
                    "doors": {"bsonType": "int"},
                    "cargo_capacity_liters": {"bsonType": "int"},
                    "fuel_consumption_km_per_l": {"bsonType": "double"},
                    "horsepower_hp": {"bsonType": "int"}
                }
            }
        })
    except CollectionInvalid as e:
        if "already exists" not in str(e):
            raise


def car_data_gen():

    return {
        "brand": random.choice(brands),
        "model": fake.word().capitalize() + " " + fake.lexify(text='??'),
        "year": random.randint(year - 5, year),
        "price": round(random.uniform(50000.0, 200000.0), 2),
        "engine": random.choice(["1.6L", "2.0L", "3.0L"]) + " " + random.choice(["Turbocharged Inline-4", "V6", "Inline-6"]),
        "fuel_type": random.choice(alowed_fuel_type),
        "color": random.choice(alowed_colors),
        "mileage_km": random.randint(0, 100000),
        "doors": random.choice([2, 3, 4, 5]),
        "transmission": random.choice(transmission),
        "segment": random.choice(alowed_segment),
        "cargo_capacity_liters": random.randint(300, 700),
        "suspension": random.choice(suspension),
        "drivetrain": random.choice(drivetrain),
        "fuel_consumption_km_per_l": round(random.uniform(8.0, 20.0), 1),
        "horsepower_hp": random.randint(100, 400)
    }


def populate_db():

    total_cars = mongo.collection.count_documents({})
    if (total_cars > 0):
        print("Banco já populado com os carros.")
        return

    db_create()
    cars_batch = [car_data_gen() for _ in range(register_count)]
    mongo.collection.insert_many(cars_batch)


def main():
    if len(sys.argv) < 2:
        print("Usage: python populate_db.py <p (populate), e (erase) or d (delete db)>")
        return

    user_input = sys.argv[1].lower()

    if (user_input == "p"):
        populate_db()
        return

    if (user_input == "e"):
        mongo.delete_many({})
        return

    if (user_input == "d"):
        mongo.collection.drop()
        return

    print(f"Comando {user_input} não encontrado.")


if __name__ == "__main__":

    if (mongo.collection is None):
        raise Exception("MongoDB não inicializado!")

    main()
