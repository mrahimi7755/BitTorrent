import bencodepy

# Encoding a dictionary
a = bencodepy.encode({'title': 'Example'})
print(a)  # Output: b'd5:title7:Examplee'

# Encoding an integer
b = bencodepy.encode(12)
print(b)  # Output: b'i12e'
