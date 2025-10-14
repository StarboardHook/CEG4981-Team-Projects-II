import transceiver
import aes

port = 'COM3'

t = transceiver.transceiver(port)

t.open()

encrypted_files = t.receive()

i = 1
for file in encrypted_files:
    with open(f'{i}_enc.bin', "wb") as wfile:
        wfile.write(file)
    i += 1

password = "ThisKeyForDemoOnly!"
i = 1
for file in encrypted_files:
    aes.decrypt(password, f'{i}_enc.bin', f'{i}_dec.png')
    i += 1