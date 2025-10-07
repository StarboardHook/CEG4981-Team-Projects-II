# Group 4
# Author: Nicholas Largent
# This is to meet the requirment of "All communication must be encrypted"
# This is done with AES encryption, mode CTR


import pyaes
import hashlib

def encyrpt(password, file_to_be_encrypted_path, file_path_for_encrypted):
    # all args are strings
    # This function uses the CTR mode of AES to encrypt a stream of data from a file and save that encryption into a file
    
    h = hashlib.new('sha256')
    h.update(password.encode())
    key = h.digest()

    # Create the mode of operation to encrypt with; Mode is CTR
    mode = pyaes.AESModeOfOperationCTR(key)

    # The input and output files
    file_in = open(file_to_be_encrypted_path, 'rb')
    file_out = open(file_path_for_encrypted, 'wb')

    # Encrypt the data as a stream
    pyaes.encrypt_stream(mode, file_in, file_out, 16)

    # Close the files
    file_in.close()
    file_out.close()


def decrypt(password, encrypted_file_path, decrypted_file_path):
    # all args are strings
    # This function uses the CTR mode of AES to decrypt a stream of data from a file and save that into a file
    
    h = hashlib.new('sha256')
    h.update(password.encode())
    key = h.digest()

    # Create the mode of operation to decrypt with; Mode is CTR
    mode = pyaes.AESModeOfOperationCTR(key)

    # The input and output files
    file_in = open(encrypted_file_path, 'rb')
    file_out = open(decrypted_file_path, 'wb')

    # decrypt the data as a stream
    pyaes.decrypt_stream(mode, file_in, file_out, 16)


def decrypt_byte_list(password, encrypted_file_path, output_file_path):
    h = hashlib.new('sha256')
    h.update(password.encode())
    key = h.digest()

    # Create the mode of operation to decrypt with; Mode is CTR
    mode = pyaes.AESModeOfOperationCTR(key)

    file_out = open(output_file_path, 'wb')

    pyaes.decrypt_stream(mode, encrypted_file_path, file_out)

# Setup for testing
# password = "ThisKeyForDemoOnly!"
# # file_to_encrypt = './Images/image2.png'
# encrypted_file = './1_enc.bin'
# decrypted_file = './1_dec.png'


# # print('encrypting')
# # encyrpt(password, file_to_encrypt, encrypted_file)
# # print('encypting is done')


# print('decrypting')
# decrypt(password, encrypted_file, decrypted_file)
# # decrypt(password, decrypted_file, encrypted_file)

# print('done')