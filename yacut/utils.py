""" Yacut utils module """

import random

from .constants import HASH_LENGTH, RANDOM_BIT_SIZE


def get_unique_short_id():
    "Generate unique element for url"

    hash = random.getrandbits(RANDOM_BIT_SIZE)
    return ("%x" % hash)[:HASH_LENGTH]
