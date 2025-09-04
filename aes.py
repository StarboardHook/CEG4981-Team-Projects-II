# This file needs a description 


import pyaes
import hashlib



password = "ThisKeyForDemoOnly!"
h = hashlib.new('sha256')
h.update(password.encode())
key = h.digest()

# Create the mode of operation to encrypt with; Mode is CTR
mode = pyaes.AESModeOfOperationCTR(key)

# The input and output files
file_in = open('./README.md')
file_out = open('./encrypted.bin', 'wb')

# Encrypt the data as a stream
pyaes.encrypt_stream(mode, file_in, file_out, 16)

# Close the files
file_in.close()
file_out.close()


