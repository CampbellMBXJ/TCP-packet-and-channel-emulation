import socket
import sys
import select
import pickle
from server import Server
from client import Client
from packet import Packet
from random import randint

#py channel.py 8089 8088 8087 8086 8091 8085 0

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
        int(sys.argv[1]) #csin
        int(sys.argv[2]) #csout
        int(sys.argv[3]) #crin
        int(sys.argv[4]) #crout
        int(sys.argv[5]) #sin
        int(sys.argv[6]) #rin
        float(sys.argv[7]) #packetloss rate
    except (ValueError, IndexError) as e:
        print ("One or more port numbers are not ints or were not entered")
        sys.exit()
        
    for i in range(6):
        if int(sys.argv[i+1]) > PORT_RANGE_UPPER or int(sys.argv[i+1]) < PORT_RANGE_LOWER:
            print("One or more port number out of range")
            sys.exit()
    
    if float(sys.argv[7]) >= 1 or float(sys.argv[7]) < 0:
        print("packetloss rate out of bounds")
        sys.exit()
        
    return int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), float(sys.argv[7])

def packCheck(pack, sock1, sock2, loss_rate):
    "Wrror checks packet"
    if pack == b"":
        sock1.close()
        sock2.close()
        return False
    if pack.magic_no != MAGIC_NO:
        return False
    rand = randint(1,99)/100.0
    if rand < loss_rate:
        print("dropped")
        return False
    return True

def bitError(packet):
    pack = pickle.loads(packet)
    rand = randint(1,99)/100.0
    if rand < 0.1:
        rand = randint(1,10)
        pack.data_len += rand
    return pickle.dumps(pack)

def main():
    """main"""
    csin_port, csout_port, crin_port, crout_port, sin_port, rin_port, loss_rate = checkCommandArgs()
    
    #csout socket
    csout = Client(IP, csout_port)
    csout.connect(IP, sin_port)
    
    #csin socket 
    csin = Server(IP, csin_port, BUFFER_SIZE)
    csin.accept()
    
    #crout socket
    crout = Client(IP, crout_port)
    crout.connect(IP, rin_port)
    
    #crin socket
    crin = Server(IP, crin_port, BUFFER_SIZE)
    crin.accept()
     
    left_open = True
    right_open = True
    while left_open or right_open:
        print("selecting")
        ready, _, _ = select.select([csin.connection, crin.connection], [], [])
        for server in ready:
            if server is csin.connection:
                pack = csin.receive()
                if pack == b"":
                    data = pack
                    right_open = False
                else:
                    data = pickle.loads(pack)                
                if not packCheck(data, csin, crout, loss_rate):
                    continue
                pack = bitError(pack)
                crout.send(pack)
            elif server is crin.connection:
                pack = crin.receive()
                if pack == b"":
                    data = pack
                    left_open = False
                else:
                    data = pickle.loads(pack)                
                if not packCheck(data, crin, csout, loss_rate):
                    continue
                pack = bitError(pack)
                csout.send(pack)
            
    
main()
print("done")