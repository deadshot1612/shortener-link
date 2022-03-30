from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from random import choice
from string import digits


SIZE = getattr(settings, "MAXIMUM_URL_CHARS", 6)
AVAIABLE_CHARS = digits


from account.models import Account

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: Account, timestamp: int):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

generate_token = TokenGenerator()

def create_random_code(chars=AVAIABLE_CHARS):
    """
    Creates a random string with the predetermined size
    """
    return "".join(
        [choice(chars) for _ in range(SIZE)]
    )