from faker import Faker
import json


if __name__ == "__main__":
    fake = Faker()

    data = []
    for _ in range(100_000):
        obj = {
            "name": fake.name(),
            "address": fake.address(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "age": fake.random_int(min=18, max=99),
            "job": fake.job(),
            "company": fake.company(),
            "country": fake.country(),
            "credit_card": fake.credit_card_number(),
        }
        data.append(obj)

    json_data = json.dumps(data)

    with open("large_data.json", "w") as f:
        f.write(json_data)
