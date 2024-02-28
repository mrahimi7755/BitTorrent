from hashlib import sha1
import json
import bencodepy
from util import collapse, slice
from time import time
TrackerURL = "127.0.0.5"
CLIENT_NAME = "Mohammad"

def make_torrent_file(file=None, tracker=None, comment=None):
    """Returns the bencoded contents of a torrent file in bytes."""
    if not file or not tracker:
        raise TypeError("make_torrent_file requires at least one file and one tracker.")

    torrent = {}
    
    if isinstance(tracker, list):
        torrent["announce"] = tracker[0]
        torrent["announce-list"] = [[t] for t in tracker]
    else:
        torrent["announce"] = tracker

    torrent["creation date"] = int(time())
    torrent["created by"] = CLIENT_NAME
    if comment:
        torrent["comment"] = comment

    torrent["info"] = make_info_dict(file)
    return bencodepy.encode(torrent)

def write_torrent_file(torrent=None, file=None, tracker=None, comment=None):
    """Similar to make_torrent_file, but writes the torrent data to a file."""
    if not torrent:
        raise TypeError("write_torrent_file() requires a torrent filename to write to.")
    
    data = make_torrent_file(file=file, tracker=tracker, comment=comment)
    with open(torrent, "wb") as torrent_file:
        torrent_file.write(data)

def make_info_dict(file):
    """Returns the info dictionary for a torrent file."""
    with open(file, 'rb') as f:
        contents = f.read()

    piece_length = 524288
    info = {
        "piece length": piece_length,
        "length": len(contents),
        "name": file
    }

    pieces = slice(contents, piece_length)
    pieces = [sha1(p).digest() for p in pieces]
    info["pieces"] = collapse(pieces)

    return info

def Main():
    write_torrent_file(torrent="mysample2.txt", file="DN_Project(Phase1).pdf", tracker=TrackerURL)

if __name__ == '__main__':
    Main()
