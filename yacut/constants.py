import string
import re

HASH_SIZE = 6
MAX_LENGHT_SHORT = 16
MAX_LENGHT_ORIGINAL = 2000
MAX_CUSTOM_ID_CREATE_TRYIES = 10
CHARACTER_SET = string.ascii_letters + string.digits
PATTERN = f'^[{re.escape(CHARACTER_SET)}]+'
CUSTOM_ID_FORM_CHECK = f'[{re.escape(CHARACTER_SET)}]'
