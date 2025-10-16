# This is to be the main script to transmit and receive between the rpi and server
# Works with Team_4_v4.py that does the heavy lifting
import Team_4_v4 


def main():
    print('Starting Team4 main script')

    flash_drive_file_path = input('Input the file path for the images on the flash drive: ')
   
    print('Running Team_4_v4.py')
    Team_4_v4.run(flash_drive_file_path)


main()