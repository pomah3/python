from pathlib import Path

def get_ref(gitdir):
    path = Path(gitdir) / 'HEAD'

    with path.open("r") as f:
        return f.read()[5:-1]

def is_detached(gitdir, ref = 'HEAD'):
    path = Path(gitdir) / ref

    with path.open("r") as f:
        return f.read()[:3] != 'ref'

def ref_resolve(gitdir, ref):
    path = Path(gitdir) / ref

    if not path.exists():
        return None

    with path.open('r') as f:
        content = f.read()

    if is_detached(gitdir, ref):
        return content
    
    return ref_resolve(gitdir, content[5:-1])

def resolve_head(gitdir):
    return ref_resolve(gitdir, 'HEAD')

def update_ref(gitdir, ref, sha):
    path = Path(gitdir) / ref

    with path.open('w') as f:
        f.write(sha)
    
