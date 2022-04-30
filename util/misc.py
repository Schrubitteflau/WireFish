import string
import random

def add_space_and_encode_to_bytes(string: str) -> bytes:
    return "{} ".format(string).encode()

def get_random_string(length: int = 10, charset: str = string.ascii_lowercase) -> str:
    return "".join(random.choice(charset) for i in range(length))
