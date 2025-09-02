# This file needs a description 


import pyaes
#import os
import hashlib

# Counter Mode of Operation

password = "ThisKeyForDemoOnly!"
# The SHA256 hash algorithm returns a 32-byte string
#key = hashlib.sha256(password).digest()


h = hashlib.new('sha256')
h.update(password.encode())
key = h.digest()

# Create the mode of operation to encrypt with
mode = pyaes.AESModeOfOperationCTR(key)

# The input and output files
file_in = open('./Images/image9.png', 'r')
file_out = open('./encrypted.bin', 'w')

# Encrypt the data as a stream, the file is read in 8kb chunks, be default
pyaes.encrypt_stream(mode, file_in, file_out, 16)

# Close the files
file_in.close()
file_out.close()


