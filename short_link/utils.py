from django.conf import settings
from random import choice
from string import ascii_lowercase


SIZE = getattr(settings, "MAXIMUM_URL_CHARS", 5)
AVAIABLE_CHARS = ascii_lowercase


def create_random_code(chars=AVAIABLE_CHARS):
    """
    Creates a random string with the predetermined size
    """
    return "".join(
        [choice(chars) for _ in range(SIZE)]
    )

def create_shortened_url(model_instance):
    random_code = create_random_code()
    model_class = model_instance.__class__

    if model_class.objects.filter(short_url=random_code).exists():
        return create_shortened_url(model_instance)

    return random_code