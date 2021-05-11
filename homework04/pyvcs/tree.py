from pyvcs.index import GitIndexEntry
from pyvcs.objects import hash_object
import typing as tp
import struct
import os
import time

def commit_tree(gitdir, tree_sha, message, parent, author):
    ts = int(time.mktime(time.localtime()))
    tz = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    tz = int(tz / 60 / 60 * -1)
    if tz > 0:
        tzz = f"+0{tz}00"
    elif tz < 0:
        tzz = f"-0{tz}00"
    else:
        tzz = "0000"
    
    output = b''
    output += b'tree ' + tree_sha.encode() + b'\n'
    if parent:
        output += bytes.fromhex(parent) + b'\n'
    output += (f"author {author} {ts} {tzz}\ncommitter {author} {ts} {tzz}\n\n{message}\n").encode()
    
    return hash_object(output, "commit", write=True)

def write_tree(gitdir, entries: tp.List[GitIndexEntry]):
    
    outputs = []

    subtrees = dict()

    for entry in entries:
        if '/' in entry.name:
            subname = entry.name[:entry.name.find('/')]
            
            if subname not in subtrees.keys():
                subtrees[subname] = []

            entry.name = entry.name[entry.name.find('/')+1:]
            subtrees[subname].append(entry)
        else:
            output = b''
            output += str(oct(entry.mode))[2:].encode()
            output += b' ' + entry.name.encode() + b'\0'
            output += struct.pack("20s", entry.sha1)

            outputs.append((entry.name, output))

    for (subname, subentries) in subtrees.items():
        output = b''
        output += b'40000'
        output += b' ' + subname.encode() + b'\0'
        output += bytes.fromhex(write_tree(gitdir, subentries))

        outputs.append((subname, output))

    outputs.sort()

    return hash_object(b''.join(data for (name, data) in outputs), "tree", write=True)
