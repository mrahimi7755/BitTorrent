import bencodepy

# Encoding a dictionary
encoded_dict = bencodepy.encode({'title': 'Example'})
# Output: b'd5:title7:Examplee'
print(encoded_dict)

# Encoding an integer
encoded_int = bencodepy.encode(12)
# Output: b'i12e'
print(encoded_int)
