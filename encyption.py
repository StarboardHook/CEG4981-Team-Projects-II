# This file 


# All keys may be 128 bits (16 bytes), 192 bits (24 bytes) or 256 bits (32 bytes) long.
# To generate a random key use:
'''

import os

# 128 bit, 192 bit and 256 bit keys
key_128 = os.urandom(16)
key_192 = os.urandom(24)
key_256 = os.urandom(32)

'''

import pyaes
import os
import hashlib

# A 256 bit (32 byte) key
#key = os.urandom(32)

# For some modes of operation we need a random initialization vector of 16 bytes
iv = "InitializationVe"

# Counter Mode of Operation

password = "This_key_for_demo_purposes_only!"
# The SHA256 hash algorithm returns a 32-byte string
#key = hashlib.sha256(password).digest()


h = hashlib.new('sha256')
h.update(password.encode())
key = h.digest()

# Create the mode of operation to encrypt with
mode = pyaes.AESModeOfOperationCTR(key)

# The input and output files
file_in = os.open('../Images/image9.png')
file_out = os.open('./encrypted.bin')

# Encrypt the data as a stream, the file is read in 8kb chunks, be default
pyaes.encrypt_stream(mode, file_in, file_out)

# Close the files
os.close(file_in)
os.close(file_out)