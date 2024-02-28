# util.py
# A small collection of useful functions
from functools import reduce

class database():
	def __init__(self):
		self.peers_dict={}
		self.bit_field_dict={}
		self.downloaded={}
		self.left={}
		self.peer_id=''
		self.torrent_dict={}
		
def collapse(data):
	""" Given an homogenous list, returns the items of that list
	concatenated together. """

	return reduce(lambda x, y: x + y, data)

def slice(string, n):
	""" Given a string and a number n, cuts the string up, returns a
	list of strings, all size n. """

	temp = []
	i = n
	while i <= len(string):
		temp.append(string[(i-n):i])
		i += n

	try:	# Add on any stragglers
		if string[(i-n)] != "":
			temp.append(string[(i-n):])
	except IndexError:
		pass

	return temp


def convert(byte_dict):
	""" after we decode the dictionary we read from metinfo file
	 	we need to convert keys and values of this dictionary from bytes
		into string exept pieces which is ah1 output
		"""
	normal_dict={}
	normal_info_dict={}
	
	for key in byte_dict.keys():
		if key!=b'info':
			if type(byte_dict[key]) is bytes:
				normal_dict[str(key , 'utf-8')]=str(byte_dict[key], 'utf-8')
			else:
				normal_dict[str(key , 'utf-8')] = byte_dict[key]

	for key in byte_dict[b'info'].keys():
		if key!=b'pieces':
			if type(byte_dict[b'info'][key]) is bytes:
				normal_info_dict[str(key , 'utf-8')]=str(byte_dict[b'info'][key], 'utf-8')
			else:
				normal_info_dict[str(key , 'utf-8')] = byte_dict[b'info'][key]		
		else:
			normal_info_dict[str(key , 'utf-8')] = byte_dict[b'info'][key]
	normal_dict['info']=normal_info_dict
	return normal_dict

