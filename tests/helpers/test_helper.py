import random
import string


def generate_random_username():
    return "".join(random.choice(string.ascii_letters) for i in range(8))


def generate_random_email():
    return f"{generate_random_username()}@test.test"


def generate_random_password():
    return "".join(
        random.choice(string.ascii_letters + string.digits + string.punctuation)
        for _ in range(8)
    )
