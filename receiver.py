import socket
import sys
import os.path
from server import Server
from client import Client
from file import File
from packet import Packet
import pickle

#py receiver.py 8085 8084 8087 file.txt

IP = 'localhost'
ACKNOWLEDGMENT_PACKET = 1
DATA_PACKET = 0
MAGIC_NO = 0x497E
PORT_RANGE_UPPER = 64000
PORT_RANGE_LOWER = 1024
BUFFER_SIZE = 1024

def checkCommandArgs():
    """Checks the validity of the command line arguements"""
    try:
        int(sys.argv[1]) #rin
        int(sys.argv[2]) #rout
        int(sys.argv[3]) #crin
    except (ValueError, IndexError) as e:
        print ("One or more port numbers are not ints or were not entered")
        sys.exit()
        
    for i in range(3):
        if int(sys.argv[i+1]) > PORT_RANGE_UPPER or int(sys.argv[i+1]) < PORT_RANGE_LOWER:
            print("One or more port number out of range")
            sys.exit()
            
    if os.path.isfile(sys.argv[4]):
        print("file already exists")
        sys.exit()
        
    return int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]

def packChecker(pack):
    """Verifies the packets integrity and authenticty"""
    if pack.magic_no != MAGIC_NO or pack.packet_type != DATA_PACKET:
        return False
    if not pack.verify():
        print("bit error")
        return False
    return True

def main():
    """main"""
    expected = 0
    rin_port, rout_port, crin_port, file = checkCommandArgs()
    
    #rin socket
    rin = Server(IP, rin_port, BUFFER_SIZE)
    rin.accept()
    
    #rout socket
    rout = Client(IP, rout_port)
    rout.connect(IP, crin_port)
    
    #opens and creates file
    open_file = File(file)
    
    while True:
        buf = rin.receive()
        print("recieved")
        pack = pickle.loads(buf)
        print(pack)
        
        if not packChecker(pack):
            continue
        response = Packet(ACKNOWLEDGMENT_PACKET, pack.seq_no, 0)
        rout.send(pickle.dumps(response))
        print("sent")
        
        if pack.seq_no == expected:
            expected += 1
        else:
            continue
        
        if pack.data_len > 0:
            open_file.write(pack.data)
        else:
            break
    
    open_file.close()
    rout.shutdown()
    rin.close()
    rout.close()
    
main()