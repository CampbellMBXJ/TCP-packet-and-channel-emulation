import sys
import os.path
from client import Client
from server import Server
from file import File
from packet import Packet, PacketBuffer
import pickle

#py sender.py 8091 8090 8089 test.txt

IP = 'localhost'
ACKNOWLEDGMENT_PACKET = 1
DATA_PACKET = 0
PORT_RANGE_UPPER = 64000
PORT_RANGE_LOWER = 1024
BUFFER_SIZE = 1024

def checkCommandArgs():
    """Checks the validity of the command line arguements"""
    try:
        int(sys.argv[1]) #sin
        int(sys.argv[2]) #sout
        int(sys.argv[3]) #csin
    except (ValueError, IndexError) as e:
        print ("One or more port numbers are not ints or were not entered")
        sys.exit()
        
    for i in range(3):
        if int(sys.argv[i+1]) > PORT_RANGE_UPPER or int(sys.argv[i+1]) < PORT_RANGE_LOWER:
            print("One or more port number out of range")
            sys.exit()
            
    if not os.path.isfile(sys.argv[4]):
        print("file does not exist")
        sys.exit()
        
    return int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    
    

def main():
    """Main"""
    next_no = 0
    exit_flag = False
    sin_port, sout_port, csin_port, file = checkCommandArgs()

    #sin socket
    sin = Server(IP, sin_port, BUFFER_SIZE)
    sin.accept()    
    
    #sout socket
    sout = Client(IP, sout_port)
    sout.connect(IP, csin_port)
    
    open_file = File(file)
    buffer = PacketBuffer()
    
    sent = 0
    
    
    while(not exit_flag):
        data, data_len = open_file.readBytes()
        pack = Packet(DATA_PACKET, next_no, data_len, data)
        if data_len == 0:
            exit_flag = True
        buffer.onqueue(pack)
        while True:
            sout.send(pickle.dumps(buffer.peek()))
            sent+=1
            if not sin.receiveSecond(next_no):
                print("no responce or incorrect responce")
                continue
            print("response and checked")
            next_no += 1
            buffer.dequeue()
            break
    open_file.close()
    sout.shutdown()
    sin.close()
    sout.close()
    print("sent: " + str(sent))
    
main()