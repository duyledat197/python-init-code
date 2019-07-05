import random
import string


def get_crypto_rand_string(length: int = 32) -> str:
    return "".join(
        random.SystemRandom().choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
        for _ in range(length)
    )


def get_flavor_isense_id() -> str:
    chars = "".join(
        random.SystemRandom().choice(string.ascii_uppercase)
        for _ in range(2)
    )

    digits = "".join(
        random.SystemRandom().choice(string.digits)
        for _ in range(5)
    )

    return chars + digits
