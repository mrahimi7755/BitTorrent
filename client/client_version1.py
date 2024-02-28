import socket
from hashlib import sha1
from random import choice
from urllib.parse import urlencode
import time
import bencodepy

CLIENT_ID = "PY"
CLIENT_VERSION = "VER1"
CLIENT_PORT = 111


def read_torrent_file(torrent_file):
    """Given a .torrent file, returns its decoded dictionary."""
    with open(torrent_file, "rb") as file:
        bc = bencodepy.Bencode(encoding='utf-8')
        return bc.decode(file.read())


def generate_peer_id():
    """Returns a 20-byte peer id."""
    random_string = "".join(choice("1234567890") for _ in range(12))
    return f"-{CLIENT_ID}{CLIENT_VERSION}-{random_string}"


def make_HTTPgetRequest(params):
    """Given parameters dictionary, returns HTTP request string."""
    params_str = urlencode(params)
    request_body = f'GET /?{params_str} HTTP/1.1\r\nHost: 127.0.0.5:8080\r\n\r\n'.encode('utf-8')
    return request_body


def Main():
    torrent_dict = read_torrent_file("mysample1.txt")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((torrent_dict['announce'], 8080))

        info_hash = sha1(bencodepy.encode(torrent_dict["info"])).hexdigest().encode('utf-8')
        peer_id = generate_peer_id()

        params = {
            "info_hash": info_hash,
            "peer_id": peer_id,
            "port": 6881,
            "uploaded": 0,
            "downloaded": 0,
            "left": 1000,
            "compact": 1
        }
        request_body = make_HTTPgetRequest(params)

        while True:
            s.sendall(request_body)
            data = s.recv(2048)
            time.sleep(5)


if __name__ == 'main':
    Main()
