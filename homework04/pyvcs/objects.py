import hashlib
import zlib
from pyvcs.repo import repo_find
from os import makedirs
from typing import List
from pathlib import Path

def hash_object(data: bytes, fmt: str, write=False):
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

def resolve_object(hash_part: str, repo_dir: Path):
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


def find_object(obj_name: str, gitdir: Path):
    path = str(gitdir) + "/" + obj_name[:2] + "/" + obj_name[2:]
    return path

def read_object(sha: str, gitdir: Path):
    sha = resolve_object(sha, gitdir)[0]
    path = gitdir / "objects" / sha[:2] / sha[2:]
   
    with open(path, "rb") as f:
        data = zlib.decompress(f.read())

    pos = data.find(b"\x00")
    header = data[:pos]
    type = header[:header.find(b" ")].decode()
    content = data[pos+1:]

    return (type, content)


def read_tree(data: bytes):
    trees = []

    while len(data):
        sha = bytes.hex(data[-20:])
        data = data[:-21]

        obj, _ = read_object(sha, repo_find())
        pos = data.rfind(b" ")
        name = data[pos + 1 :].decode("ascii")
        data = data[:pos]
        if obj == "tree":
            mode = "40000"
        else:
            mode = data[-6:].decode("ascii")
        mode_len = -1 * len(mode)
        data = data[:mode_len]
        mode_int = int(mode)
        trees.insert(0, (mode_int, sha, name))

    return trees


def cat_file(obj_name: str, pretty: bool = True):
    gitdir = repo_find()
    obj_type, content = read_object(obj_name, gitdir)
    if obj_type == "blob":
        if pretty:
            result = content.decode("ascii")
            print(result)
        else:
            result = str(content)
            print(result)
    elif obj_type == "tree":
        tree_entries = read_tree(content)
        result = ""
        for entry in tree_entries:
            mode = str(entry[0])
            if len(mode) != 6:
                mode = "0" + mode
            tree_pointer_type, _ = read_object(entry[1], gitdir)
            print(f"{mode} {tree_pointer_type} {entry[1]}\t{entry[2]}")
    else:
        _, content = read_object(resolve_object(obj_name, repo_find())[0], repo_find())
        print(content.decode())


def find_tree_files( tree_sha: str, gitdir: Path, accumulator: str = "" ):
    tree_files = []
    _, tree = read_object(tree_sha, gitdir)
    tree_entries = read_tree(tree)
    for entry in tree_entries:
        pointer_type, _ = read_object(entry[1], gitdir)
        path = Path(entry[2]).relative_to(gitdir.parent)
        if path.is_dir():
            accumulator += str(path) + "/"
        if pointer_type == "tree":
            tree_files += find_tree_files(entry[1], gitdir, accumulator)
        else:
            tree_files.append((entry[1], accumulator + str(path)))
    return tree_files


def commit_parse(raw: bytes, start: int = 0, dct=None):
    data = raw.decode("ascii")
    data = data[5:]
    author_pos = data.find("author")
    tree = data[: author_pos - 2]
    return tree