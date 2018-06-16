import sys

READ_SIZE = 512

class File:
    """Manages file reading and writing"""
    def __init__(self, file):
        try:
            self.file = open(file, "r")
        except IOError:
            self.file = open(file, "a")
            
    def readBytes(self):
        data =  self.file.read(READ_SIZE)
        return data, len(data.encode("utf-8"))
    
    def write(self, data):
        self.file.write(data)
    
    def close(self):
        self.file.close()
