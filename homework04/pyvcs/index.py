from pathlib import Path
from pyvcs.repo import repo_find
import struct
import hashlib

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

def write_index(gitdir, entries):
    index = Path(gitdir) / "index"

    dirc = b"DIRC"
    version = 2
    entries_count = len(entries)

    with open(index, "wb") as file:
        header = struct.pack(">4sII", dirc, version, entries_count)
        file.write(header)

        for entry in entries:
            entry_tuple = (
                entry.ctime_s,
                entry.ctime_n,
                entry.mtime_s,
                entry.mtime_n,
                entry.dev,
                entry.ino,
                entry.mode,
                entry.uid,
                entry.gid,
                entry.size,
                entry.sha1,
                entry.flags.to_bytes(2, "big"),
            )
            file.write(struct.pack(">10I20s2s", *entry_tuple))
            filename = entry.name.encode() 
            file.write(filename + b'\x00' * (2 + 8 - len(filename) % 8))
    with open(index, "rb") as file:
        hash = hashlib.sha1(file.read()).digest()
    with open(index, "ab") as file:
        file.write(hash)

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