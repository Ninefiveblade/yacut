import random

from .constants import HASH_SIZE, PATTERN_CONST


def gen_id(size=HASH_SIZE, chars=PATTERN_CONST):
    return ''.join(random.choice(chars) for _ in range(size))
