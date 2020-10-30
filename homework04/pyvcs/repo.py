from pathlib import Path
from os import makedirs, getenv


def repo_create(path: Path) -> Path:
    DIRNAME = getenv("GIT_DIR") or ".git"

    if path.is_file():
        raise Exception(f"{path} is not a directory")

    gitdir = path / DIRNAME
    
    dirs = [
        gitdir / "refs" / "heads",
        gitdir / "refs" / "tags",
        gitdir / "objects"
    ]

    for dir in dirs:
        makedirs(dir)

    with open(gitdir / "HEAD", "w") as file:
        file.write("ref: refs/heads/master\n")

    with open(gitdir / "config", "w") as file:
        file.write("[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n")

    with open(gitdir / "description", "w") as file:
        file.write("Unnamed pyvcs repository.\n")

    return gitdir

def repo_find(path: Path = Path(".")) -> Path:
    DIRNAME = getenv("GIT_DIR") or ".git"
    
    path = path.absolute()
    while True:
        if DIRNAME in (x.name for x in path.iterdir()):
            return path / DIRNAME
        
        if path == path.parent:
            break

        path = path.parent

    raise Exception("Not a git repository")