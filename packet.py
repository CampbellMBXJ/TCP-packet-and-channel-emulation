import hashlib
MAGIC_NO = 0x497E

class Packet:
    """Packet class to be serilized and sent to represent a packet"""
    def __init__(self, packet_type, seq_no, data_len, data=""):
        self.magic_no = MAGIC_NO
        self.packet_type = packet_type
        self.seq_no = seq_no
        self.data_len = data_len
        self.data = data
        string = str(self.data)+str(self.data_len)+str(self.seq_no)+str(self.packet_type)
        self.check_sum = hashlib.md5(string.encode("utf-8")).digest()
        
    def verify(self):
        """Verifies the Check sum matches the rest of the packet data"""
        string = str(self.data)+str(self.data_len)+str(self.seq_no)+str(self.packet_type)
        if self.check_sum == hashlib.md5(string.encode("utf-8")).digest():
            return True
        return False
        
class PacketBuffer:
    """To buffer packets"""
    def __init__(self):
        self.buffer = []
    
    def onqueue(self, packet):
        self.buffer.append(packet)
        
    def dequeue(self):
        return self.buffer.pop(0)
    
    def peek(self):
        return self.buffer[0]