import socket


class Client:
    """Wrapper class for socket client"""
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))

    def send(self, data):
        self.sock.send(data)
    
    def connect(self, ip, port):
        self.sock.connect((ip, port))
        
    def close(self):
        self.sock.close()
        
    def shutdown(self):
        self.sock.shutdown(socket.SHUT_RDWR)