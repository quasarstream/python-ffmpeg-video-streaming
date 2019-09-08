import tempfile
from secrets import token_bytes, token_hex


def generate_key_info_file(url, path, length=16):
    with open(path, 'wb') as key:
        key.write(token_bytes(length))
    key_info = tempfile.NamedTemporaryFile(mode='w', delete=False)
    key_info.write("\n".join([url, path, token_hex(length)]))
    key_info.close()
    return key_info.name
