import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree

import shutil

def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths, write=True)

def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    tree = write_tree(gitdir, read_index(gitdir))
    return commit_tree(gitdir, tree, message, parent=None, author=author)

def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    update_ref(gitdir, "HEAD", obj_name)

    names = []
    for entry in read_index(gitdir):
        names.append(entry.name)
        
    files = find_tree_files(commit_parse(read_object(obj_name, gitdir)[1]), gitdir)

    update_index(gitdir, list(pathlib.Path(file[1]) for file in files), write=True)
    
    for name in names:
        p = pathlib.Path(name.split("/")[0])

        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            os.remove(p)

    for sha, name in files:
        if name.find("/") != -1:
            p = os.path.split(name)[0]
            if not pathlib.Path(p).exists():
                os.makedirs(p)

        with open(name, "wb") as f:
            f.write(read_object(sha, gitdir)[1])