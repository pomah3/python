import hashlib
import zlib

def hash_object(data: bytes) -> str:
    hash = hashlib.sha1(data).hexdigest()
    return hash