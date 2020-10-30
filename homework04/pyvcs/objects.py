import hashlib
import zlib
from pyvcs.repo import repo_find
from os import makedirs

def hash_object(data: bytes, fmt: str, write=False) -> str:
    header = f"blob {len(data)}\0".encode()
    store = header + data
    
    object_id = hashlib.sha1(store).hexdigest()
    object_content = zlib.compress(store)

    if not write:    
        return object_id

    repo = repo_find()

    object_dir = repo / "objects" / object_id[0:2]
    makedirs(object_dir, exist_ok=True)

    object_file = object_dir / object_id[2:]

    with open(object_file, "wb") as file:
        file.write(object_content)

    return object_id
