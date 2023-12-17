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


def calculate_response_time(email):
    if email.date_received and email.date_replied:
        response_time = email.date_replied - email.date_received
        # Set traffic light color based on response time
        if response_time < timedelta(hours=1):
            email.traffic_light = "green"
        elif response_time < timedelta(hours=24):
            email.traffic_light = "yellow"
        else:
            email.traffic_light = "red"
        email.response_time = response_time
        email.save()
