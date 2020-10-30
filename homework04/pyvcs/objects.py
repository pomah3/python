import hashlib
import zlib
from pyvcs.repo import repo_find
from os import makedirs
from typing import List
from pathlib import Path

def hash_object(data: bytes, fmt: str, write=False) -> str:
    header = f"{fmt} {len(data)}\0".encode()
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

def resolve_object(hash_part: str, repo_dir: Path) -> List[str]:
    if not 4 <= len(hash_part) <= 40:
        raise Exception(f"Not a valid object name {hash_part}") 
    
    objects_dir = repo_dir / "objects"
    
    objects_dirs = objects_dir.iterdir()
    suitable_dirs = (x for x in objects_dirs if x.name.startswith(hash_part[:2]))

    arr = []
    for dir in suitable_dirs:
        for file in dir.iterdir():
            file_name = dir.name + file.name
            if file_name.startswith(hash_part):
                arr.append(file_name)
    
    if len(arr) == 0:
        raise Exception(f"Not a valid object name {hash_part}")  

    return arr

def read_object(hash: str, repo_dir: Path) -> bytes:
    file_name = repo_dir / "objects" / hash[:2] / hash[2:]
    
    with open(file_name, 'rb') as file:
        content = zlib.decompress(file.read())

    null = content.find(b"\x00")
    space = content.find(b" ")

    fmt = content[:space].decode()
    size = int(content[space+1:null])
    data = content[null+1:]

    return fmt, data

def cat_file(hash_part: str, pretty: bool = False) -> None:
    repo = repo_find()

    [object_id] = resolve_object(hash_part, repo)

    fmt, content = read_object(object_id, repo)
    print(content.decode())