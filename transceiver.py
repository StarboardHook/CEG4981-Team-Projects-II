import serial
import math
import hashlib
import time

class transceiver:

    ser = None
    baudrate = 460800
    timeout = 1
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE

    xbee_bytes_per_packet = 116
    max_packet_size = xbee_bytes_per_packet * 10
    
    header = b'\x48'
    last_file_true = b'\x0F'
    last_file_false = b'\xF0'
    handshake = b'\x46'
    sync = b'\x53'

    packet_number_bytes = 2

    md5_bytes = 16

    reply_size = len(header) + packet_number_bytes

    min_packet_size = len(header) + packet_number_bytes + md5_bytes
    max_payload_size = max_packet_size - min_packet_size

    file_size_bytes = 3
    max_data_size = 2**(file_size_bytes*8) - 1

    max_packet_number = 2**(packet_number_bytes*8) - 2
    if (max_data_size < max_payload_size*max_packet_number):
        max_data_size = max_payload_size*max_packet_number

    file_info_bytes = 1 + file_size_bytes

    def __init__(self,port):
        self.port = port

    def __get_next_packet(self,packet_number,packet_size):
        
        packet_number = packet_number.to_bytes(self.packet_number_bytes,byteorder='big')
        packet_size = packet_size + self.min_packet_size
        packet_received = False

        while (packet_received == False):

            self.ser.write(self.header + packet_number)

            packet = self.ser.read(packet_size)
            
            connection_established = True

            if ((len(packet) == packet_size) and (packet[len(self.header):(len(self.header) + self.packet_number_bytes)] == packet_number)):
                transmitted_md5 = packet[-self.md5_bytes:]
                payload = packet[len(self.header) + self.packet_number_bytes:-self.md5_bytes]
                packet_received = self.__md5_compare(packet[len(self.header):(len(self.header) + self.packet_number_bytes)] + payload,transmitted_md5)
                if (packet_received == False):
                    print(f'MD5 checksum failed for packet {packet_number}')
            else:
                connection_established = False
            
            while (connection_established == False):
                self.ser.write(self.sync)
                reply = self.ser.read(1)
                if (reply == self.sync):
                    connection_established = True
        
        return payload

    def close(self):
        self.ser.close()

    def open(self):
        self.ser = serial.Serial(
            port = self.port,
            baudrate = self.baudrate,
            timeout = self.timeout,
            parity = self.parity,
            stopbits = self.stopbits)

    def __flush_buffer(self):
        rx_byte = self.ser.read(1)
        while (len(rx_byte) > 0):
            rx_byte = self.ser.read(1)

    def __establish_connection(self):

        connection_established = False

        while (connection_established == False):
            self.ser.write(self.sync)
            reply = self.ser.read(self.reply_size)

            if (len(reply) < self.reply_size):
                connection_established = False
            elif (reply[0] == int.from_bytes(self.header,byteorder='big')):
                    connection_established = True
            else:
                self.__flush_buffer()
                connection_established = False

    def __md5_compare(self,bytes_object,reference_md5):
            return hashlib.md5(bytes_object).digest() == reference_md5


    def __transmit_packet(self,packet_number,packet = bytearray()):
        
        packet_number = packet_number.to_bytes(self.packet_number_bytes,byteorder='big')

        md5 = hashlib.md5(packet_number + packet).digest()

        self.ser.write(self.header + packet_number + packet + md5)

        complete = False
        
        connection_established = True

        while (complete == False):
            reply = self.ser.read(self.reply_size)
            
            if (len(reply) == self.reply_size):
                if (reply[0:len(self.header)] == self.header):
                        next_packet = int.from_bytes(
                            reply[len(self.header):],byteorder='big')
                        complete = True
                else:
                    connection_established = False
                    complete = False
            else:
                connection_established = False
            
            while (connection_established == False):
                if (reply == self.sync):
                    self.ser.write(self.sync)
                    connection_established = True
                else:
                    reply = self.ser.read(1)

        return next_packet

    def transmit(self,bytes_objects):

        begin_transmission = 0
        prepare_next_file = 1
        transmit_file_info_packet = 2
        transmit_file = 3
        file_complete = 4
        transmission_complete = 5

        packets_per_print = 5

        num_files = len(bytes_objects)

        if (num_files > 0):
            current_state = begin_transmission
        else:
            current_state = transmission_complete

        while (current_state != transmission_complete):

            if (current_state == begin_transmission):

                self.__flush_buffer()

                start = time.perf_counter()

                print(f'Transmitting {num_files} files...')

                self.__establish_connection()
                
                next_file = 1

                current_state = prepare_next_file

            if (current_state == prepare_next_file):

                if (next_file == num_files):
                    last_file = self.last_file_true
                else:
                    last_file = self.last_file_false

                file_packets = [bytes_objects[next_file - 1][i:i+self.max_payload_size] \
                    for i in range(0,len(bytes_objects[next_file - 1]),self.max_payload_size)]

                num_packets = len(file_packets)
                num_bytes = len(bytes_objects[next_file - 1])

                file_info = last_file + \
                    num_bytes.to_bytes(self.file_size_bytes,byteorder='big')
                
                current_state = transmit_file_info_packet

            if (current_state == transmit_file_info_packet):

                next_packet = self.__transmit_packet(0,file_info)

                if (next_packet == 0):
                    current_state = transmit_file_info_packet
                elif (num_packets == 0):
                    current_state = file_complete
                else:
                    current_state = transmit_file

            if (current_state == transmit_file):

                next_packet = self.__transmit_packet(next_packet,file_packets[next_packet - 1])
                
                if (((next_packet % packets_per_print) == 0) or (next_packet == num_packets)):
                    percent_complete = round(100*next_packet/num_packets)
                    print(f'Transmitting file {next_file}: {percent_complete}% complete.', end = '\r')
                if (next_packet == 0):
                    current_state = transmit_file_info_packet
                elif (next_packet > num_packets):
                    current_state = file_complete

            if (current_state == file_complete):
                
                if (next_file == num_files):
                    transmission_time = round(time.perf_counter() - start,2)
                    print('\n' + f'{num_files} files transmitted in {transmission_time} seconds.')
                else:
                    print('\n' + f'Transmission of file {next_file} complete.')
                next_packet = self.__transmit_packet(next_packet,self.handshake)

                next_file = next_file + 1

                if (next_file > num_files):
                    current_state = transmission_complete
                else:
                    current_state = prepare_next_file


    def receive(self):

        flush_buffer = 0
        detect_transmission = 1
        receive_file_info_packet = 2
        receive_file = 3
        file_complete = 4
        complete = 5

        current_state = flush_buffer
        list_of_files = []
        
        file_info_packet_number = 0

        while (current_state != complete):

            if (current_state == flush_buffer):
                self.__flush_buffer()
                current_state = detect_transmission

            if (current_state == detect_transmission):
                
                packet = self.ser.read(len(self.sync))
                
                if (packet == self.sync):
                    current_state = receive_file_info_packet
                elif (len(packet) > 0):
                    self.__flush_buffer()
                        
            if (current_state == receive_file_info_packet):
                
                next_packet = 0

                packet = self.__get_next_packet(next_packet,self.file_info_bytes)

                last_file = packet[0:1]
                num_bytes = packet[1:]

                if (last_file == self.last_file_true):
                    last_file = True
                else:
                    last_file = False

                num_bytes = int.from_bytes(num_bytes,byteorder='big')
                num_packets = math.ceil(num_bytes/self.max_payload_size)

                next_packet = 1

                if (num_packets > 0):
                    temp_file = bytearray()
                    current_state = receive_file
                else:
                    current_state = file_complete

            if (current_state == receive_file):

                if (next_packet < num_packets):
                    expected_packet_size = self.max_payload_size
                elif (next_packet == num_packets):
                    expected_packet_size = num_bytes - self.max_payload_size*(num_packets - 1)

                packet = self.__get_next_packet(next_packet,expected_packet_size)

                temp_file.extend(packet)
                if (next_packet == num_packets):
                    list_of_files.append(temp_file)
                    next_packet = next_packet + 1
                    current_state = file_complete
                else:
                    next_packet = next_packet + 1
                   
            if (current_state == file_complete):

                packet = self.__get_next_packet(next_packet,1)
                
                if (packet == self.handshake):
                    if (last_file == True):
                        next_packet = file_info_packet_number
                        current_state = complete
                    else:
                        next_packet = file_info_packet_number
                        current_state = receive_file_info_packet
                else:
                    self.__flush_buffer
                    current_state = file_complete

        self.ser.write(
                self.header + 
                next_packet.to_bytes(
                    self.packet_number_bytes,byteorder='big'))
        
        return list_of_files