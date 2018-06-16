import socket
import select
import pickle

ACKNOWLEDGMENT_PACKET = 1
DATA_PACKET = 0
MAGIC_NO = 0x497E

class Server:
    """Wrapper class for socket server"""
    def __init__(self, ip, port, buf_size):
        self.data = None
        self.connection = None
        self.buf_size = buf_size        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(1)
        
        
    def accept(self):
        self.connection, address = self.sock.accept()
        
    
    def receive(self):
        while self.data is None:
            self.data = self.connection.recv(self.buf_size)

        d = self.data
        self.data = None
        return d
    
    def receiveSecond(self, next_no):
        try:
            self.connection.settimeout(1.0)
            self.data = self.connection.recv(self.buf_size)
        except:
            return False
        self.connection.settimeout(None)
        rcvd = pickle.loads(self.data)
        self.data = None
        if not rcvd.verify():
            return False
        if rcvd.magic_no != MAGIC_NO or rcvd.packet_type != ACKNOWLEDGMENT_PACKET:
            return False
        if rcvd.data_len != 0 or next_no != rcvd.seq_no:
            return False
        return True        
            
    def close(self):
        self.sock.close()
