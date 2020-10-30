from pathlib import Path
from os import makedirs, getenv

def repo_create(path: Path) -> Path:
    if path.is_file():
        raise Exception(f"{path} is not a directory")

    dirname = getenv("GIT_DIR") or ".git"
    gitdir = path / dirname
    
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