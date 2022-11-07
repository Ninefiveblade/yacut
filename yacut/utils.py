import random

from .constants import HASH_SIZE, CUSTOM_ID_FORM_CHECK


def gen_id(size=HASH_SIZE, chars=CUSTOM_ID_FORM_CHECK):
    return ''.join(random.choice(chars) for _ in range(size))
