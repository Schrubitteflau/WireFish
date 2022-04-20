def add_space_and_encode_to_bytes(string: str) -> bytes:
    return "{} ".format(string).encode()
