# This is to be the main script to transmit and receive between the rpi and server

import os

import aes
import transceiver
import Team_4_v3 

def setup_transceiver() -> transceiver:
    port = '/dev/ttyUSB0'
    return transceiver.transceiver(port)

def get_image_files(directory_path):
    # Takes the directory path as a string
    # Returns a list of the byte data of all the files in the directory
    files = []
    images = []
    try:
        entries = os.listdir(directory_path)
        for entry in entries:
            full_path = os.path.join(directory_path, entry)
            # Check if the entry is a file
            if os.path.isfile(full_path):
                files.append(entry)
    except FileNotFoundError:
        print(f"Error: Directory not found at '{directory_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    for file in files:
        with open(file, 'rb'):
            images.append(file.read())

    return images

def main():
    print('Starting')

    print('Setting up the transceiver')
    t = setup_transceiver()
    print('Transceiver ready')

    print('Setting up images')
    images = get_image_files('./Images')
    print('Images ready')


main()