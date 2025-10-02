import transceiver
import aes
import pyaes
import hashlib

port = 'COM3'

t = transceiver.transceiver(port)

t.open()

encrypted_files = t.receive()

h = hashlib.new('sha256')
h.update("TheKeyForDemoOnly!".encode())
key = h.digest()

# Create the mode of operation to decrypt with; Mode is CTR
mode = pyaes.AESModeOfOperationCTR(key)
for file in encrypted_files:
    
    pyaes.decrypt_stream(mode, file, 'f{file}_dec.png')
    # aes.decrypt('ThisKeyForDemoOnly!', file, 'f{file}_dec.png')