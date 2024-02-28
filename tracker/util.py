from functools import reduce

class Database:
    def __init__(self):
        self.peers_dict = {}
        self.bit_field_dict = {}
        self.downloaded = {}
        self.left = {}
        self.peer_id = ''
        self.torrent_dict = {}

def collapse(data):
    """Concatenates items of a homogenous list."""
    return reduce(lambda x, y: x + y, data)

def slice_string(string, n):
    """Splits a string into sub-strings of a specific size n."""
    temp = []
    i = n
    while i <= len(string):
        temp.append(string[i - n:i])
        i += n
    
    try:
        if string[i - n] != "":
            temp.append(string[i - n:])
    except IndexError:
        pass

    return temp

def convert(byte_dict):
    """Converts keys and values of a dictionary from bytes to strings, except for 'pieces' which is hashed."""
    normal_dict = {}
    normal_info_dict = {}
    
    for key in byte_dict.keys():
        if key != b'info':
            if isinstance(byte_dict[key], bytes):
                normal_dict[key.decode('utf-8')] = byte_dict[key].decode('utf-8')
            else:
                normal_dict[key.decode('utf-8')] = byte_dict[key]
    
    for key in byte_dict[b'info'].keys():
        if key != b'pieces':
            if isinstance(byte_dict[b'info'][key], bytes):
                normal_info_dict[key.decode('utf-8')] = byte_dict[b'info'][key].decode('utf-8')
            else:
                normal_info_dict[key.decode('utf-8')] = byte_dict[b'info'][key]
        else:
            normal_info_dict[key.decode('utf-8')] = byte_dict[b'info'][key]
    
    normal_dict['info'] = normal_info_dict
    return normal_dict
