
from random import randint
from django.core.mail import EmailMessage


def generate_number(num_digits: int = 6) -> int:
    """
    Generate a pin. of specified length.
    """
    number = 0

    while len(str(number)) != num_digits:
        number = randint(1, (10**num_digits) - 1)

    return number


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["email_subject"],
            body=data["email_body"],
            to=[data["to_email"]],
        )
        email.send()
