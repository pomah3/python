from pathlib import Path
from pyvcs.repo import repo_find
import struct
import hashlib
from pyvcs.objects import hash_object
import os

def add(gitdir, files):
    update_index(gitdir, files)

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
        entry_tuple = struct.unpack(">10I20s2s", content[begin:begin+62])
        begin += 62

        filename = b''
        while content[begin:begin+1] != b'\x00':
            filename += content[begin:begin+1]
            begin += 1
        begin += 2 + 8 - len(filename) % 8


        entry = GitIndexEntry(*entry_tuple, filename.decode())

        entries.append(entry)

    return entries

def update_index(gitdir, files, write=True):
    entries = {entry.name: entry for entry in read_index(gitdir)}
    for file in files:
        if not Path(file).exists():
            continue

        with open(file, "rb") as f:
            content = f.read()

        hash = hash_object(content, "blob", write=True)

        stat = os.stat(file)

        entry = GitIndexEntry(
            ctime_s = int(stat.st_mtime),
            ctime_n = 0,
            mtime_s = int(stat.st_mtime),
            mtime_n = 0,
            dev = stat.st_dev,
            ino = stat.st_ino,
            mode = stat.st_mode,
            uid = stat.st_uid,
            gid = stat.st_gid,
            size = stat.st_size,
            sha1 = bytes.fromhex(hash),
            flags = 7,
            name = file
        )

        entries[file] = entry

    write_index(gitdir, entries.values())
 
def write_index(gitdir, entries):
    entries = list(entries)
    entries.sort(key=lambda x: Path(x.name))

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
                (entry.flags if type(entry.flags) == bytes else entry.flags.to_bytes(2, "big")  ),
            )

            file.write(struct.pack(">10I20s2s", *entry_tuple))
            filename = str(entry.name).encode()
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