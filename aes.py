# Group 4
# This file needs a description 


import pyaes
import hashlib

def encyrpt(password, file_to_be_encrypted_path, file_path_for_encrypted):

    # password = "ThisKeyForDemoOnly!"
    h = hashlib.new('sha256')
    h.update(password.encode())
    key = h.digest()

    # Create the mode of operation to encrypt with; Mode is CTR
    mode = pyaes.AESModeOfOperationCTR(key)

    # The input and output files
    # file_in = open('./README.md')
    # file_out = open('./encrypted.bin', 'wb')
    file_in = open(file_to_be_encrypted_path, 'rb')
    file_out = open(file_path_for_encrypted, 'wb')

    # Encrypt the data as a stream
    pyaes.encrypt_stream(mode, file_in, file_out, 16)

    # Close the files
    file_in.close()
    file_out.close()


def decrypt(password, encrypted_file_path, decrypted_file_path):

    # password = "ThisKeyForDemoOnly!"
    h = hashlib.new('sha256')
    h.update(password.encode())
    key = h.digest()

    # Create the mode of operation to decrypt with; Mode is CTR
    mode = pyaes.AESModeOfOperationCTR(key)

    # The input and output files
    # file_in = open('./encrypted.bin')
    # file_out = open('./decrypted.bin', 'wb')
    file_in = open(encrypted_file_path, 'rb')
    file_out = open(decrypted_file_path, 'wb')

    # decrypt the data as a stream
    pyaes.decrypt_stream(mode, file_in, file_out, 16)


# Setup for testing
password = "ThisKeyForDemoOnly!"
file_to_encrypt = './Images/image1.png'
encrypted_file = './encrypted.bin'
decrypted_file = './decrypted.png'


print('encrypting')
encyrpt(password, file_to_encrypt, encrypted_file)
print('encypting is done')


print('decrypting')
decrypt(password, encrypted_file, decrypted_file)
# decrypt(password, decrypted_file, encrypted_file)

print('done')