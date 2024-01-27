from datetime import timedelta
from random import randint


def generate_number(num_digits: int = 6) -> int:
    """
    Generate a pin. of specified length.
    """
    number = 0

    while len(str(number)) != num_digits:
        number = randint(1, (10**num_digits) - 1)

    return number



