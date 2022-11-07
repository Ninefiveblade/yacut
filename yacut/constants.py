import string

HASH_SIZE = 6
MAX_LENGHT = 16
SHORT_CHECK = f'^[{string.ascii_letters + string.digits}]{{1,16}}'
CUSTOM_ID_FORM_CHECK = f'[{string.ascii_letters + string.digits}]'