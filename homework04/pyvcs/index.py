from pathlib import Path
from pyvcs.repo import repo_find
import struct

def add():
    pass

def read_index(gitdir):
    index = Path(gitdir) / "index"
    if not index.is_file():
        return []

    with open(index, "rb") as file:
        content = file.read()

    dirc, version, entries_count = struct.unpack(">4sII", content[0:12])
    assert dirc == b'DIRC'
    entries = []

    begin = 12
    for i in range(entries_count):
        entry_tuple = struct.unpack(">10I20s2s", content[12:12+62])
        begin += 62

        filename = b''
        while content[begin:begin+1] != b'\x00':
            filename += content[begin:begin+1]
            begin += 1
        begin += 2 + 8 - len(filename) % 8


        entry = GitIndexEntry(*entry_tuple, filename.decode())
        entries.append(entry)

    return entries

def update_index():
    pass

def write_index():
    pass

class GitIndexEntry:
    def __init__(self, ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags, name):
        self.ctime_s = ctime_s
        self.ctime_n = ctime_n
        self.mtime_s = mtime_s
        self.mtime_n = mtime_n
        self.dev = dev
        self.ino = ino
        self.mode = mode
        self.uid = uid
        self.gid = gid
        self.size = size
        self.sha1 = sha1
        self.flags = flags
        self.name = name