import socket
import threading
from urllib.parse import parse_qsl
from logging import basicConfig, info, INFO
import bencodepy

LOCALHOST = "127.0.0.5"
PORT = 8080
interested_peers = {}

class Tracker:
    def __init__(self, host="", port=8080, interval=5, log="tracker.log"):
        """Initialize Tracker settings."""
        self.host = host
        self.port = port
        self.interval = interval
        self.threads = []
        self.database = {}
        self.number_of_seeders = {}  # Number of seeders for each info_hash
        
        basicConfig(format='%(asctime)s %(message)s', filename=log, level=INFO)
        self.running = False
        self.server = create_socket(self.host, self.port)

    def run(self):
        """Start the Tracker."""
        self.running = True
        while self.running:
            self.server.listen(1)
            clientsock, clientAddress = self.server.accept()
            self.threads.append(ClientThread(self, clientAddress, clientsock))
            self.threads[-1].start()

class ClientThread(threading.Thread):
    """ClientThread for handling each client"""
    
    def __init__(self, Tracker_object, clientAddress, clientsocket):
        """Initialize the ClientThread with the Tracker object and socket details."""
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.csocket.settimeout(Tracker_object.interval + 1)
        self.thread_IP = clientAddress[0]
        self.thread_port = clientAddress[1]
        self.Tracker_object = Tracker_object
        info("New connection added: %s", clientAddress)
    
    def save_peer(self, params):
        """Save the peer's information such as peer_id, port, uploaded, downloaded, left, and event."""
        self.info_hash = params['info_hash']
        self.peer_id = params['peer_id']
        self.port = params['port']
        self.uploaded = params['uploaded']
        self.downloaded = params['downloaded']
        self.left = params['left']
    
    def make_peer_list(self):
        """Return an expanded list of peers suitable for the client."""
        interested_peers = self.Tracker_object.database[self.info_hash]
        peers = [{"peer id": peer[0], "ip": peer[1], "port": int(peer[2])} for peer in interested_peers]
        return peers
    
    def peer_list(self):
        """Placeholder for further improvements in peer list handling."""
        return self.make_peer_list()
    
    def make_HTTPResponse(self):
        """Create an HTTP response based on tracker information and peer list."""
        response = {
            "interval": self.Tracker_object.interval,
            "complete": 0,  # To be updated later
            "incomplete": 0,  # To be updated later
            "peers": self.peer_list()
        }
        response_data = bencodepy.encode(response).decode('utf-8')
        response_body = 'HTTP/1.1 200 OK\r\n' + response_data + '\r\n\r\n'
        return response_body
    
    def run(self):
        """Parse client's request, send response, and manage the client connection."""
        info("Connection from: (%s, %s)", self.thread_IP, self.thread_port)
        
        while True:
            try:
                data = self.csocket.recv(2048)
            except socket.timeout:
                self.client_timeout()
                break
            
            msg = data.decode()
            if len(msg) == 0:
                break
            
            self.save_peer(decode_request(msg))
            add_peer(self.Tracker_object, self.info_hash, self.peer_id, self.thread_IP, self.port)
            
            self.csocket.send(bytes(self.make_HTTPResponse(), 'UTF-8'))
            
            info("REQUEST: %s", decode_request(msg))
            info("RESPONSE: %s", self.make_HTTPResponse())
        
        self.client_timeout()
        info("Client at (%s, %s) disconnected...", self.thread_IP, self.thread_port)
    
    def client_timeout(self):
        """Remove the client from timeout and close the connection."""
        info("CLIENT_TIMEOUT: peer_id=%s, ip=%s, port=%s", self.peer_id, self.thread_IP, self.thread_port)
        
        for key in self.Tracker_object.database.keys():
            self.Tracker_object.database[key].remove((self.peer_id, self.thread_IP, self.port))

def read_torrent_file(torrent_file):
    """Reads a .torrent file and returns its decoded dictionary."""
    with open(torrent_file, "rb") as file:
        bc = bencodepy.Bencode(encoding='utf-8')
        return bc.decode(file.read())
    
def decode_request(msg):
    """Decode the client's request string."""
    # Strip off the start characters
    if msg[:4] == 'GET ':
        msg = msg[4:]
    else:
        print("Error: This is not a GET request.")
    
    if msg[:1] == '?' or msg[:2] == '/?':
        msg = msg.lstrip('?')
    
    path = ''
    for x in range(len(msg) - 10):
        if msg[x:x+11] == ' HTTP/1.1\r\n':
            path = msg[:x]
            break
    else:
        print("Error: Invalid GET request format.")
    
    return dict(parse_qsl(path))

def add_peer(Thread_object, info_hash, peer_id, ip, port):
    """Add a peer to the torrent database and update the tracker's database."""
    if info_hash in Thread_object.database:
        if (peer_id, ip, port) not in Thread_object.database[info_hash]:
            Thread_object.database[info_hash].append((peer_id, ip, port))
    else:
        Thread_object.database[info_hash] = [(peer_id, ip, port)]
        Thread_object.number_of_seeders[info_hash] = 0

def create_socket(LOCALHOST, PORT):
    """Create a socket and bind it to the specified address and port."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))
    return server

def Main():
    myTracker = Tracker(LOCALHOST)
    info('Server started ...')
    info('Waiting for client request...')
    myTracker.run()

if __name__ == '__main__':
    Main()
