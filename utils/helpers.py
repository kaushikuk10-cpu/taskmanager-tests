from faker import Faker

fake = Faker()


def generate_user():
    return {
        "username": fake.user_name() + str(fake.random_int(100, 999)),
        "password": fake.password(length=10)
    }


def generate_task(priority="HIGH"):
    return {
        "title": fake.sentence(nb_words=4).rstrip("."),
        "description": fake.paragraph(nb_sentences=2),
        "priority": priority,
        "completed": False
    }