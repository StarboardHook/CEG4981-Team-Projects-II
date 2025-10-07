import transceiver
import aes
import pyaes
import hashlib

port = 'COM3'

t = transceiver.transceiver(port)

t.open()

encrypted_files = t.receive()


password = 'TheKeyForDemoOnly'

for file in encrypted_files:
    
    aes.decrypt_byte_list(password, file, 'f{file}_dec.png')