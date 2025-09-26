class Packet:
    def __init__(self, opcode):
        self.opcode = opcode

    def getCode(self):
        return self.opcode


class RRQ(Packet):
    def __init__(self, opcode, filename):
        super().__init__(opcode)
        self.filename = filename
        self.size = 

    def getFIlename(self):
        return self.filename

class DAT(Packet):
    def __init__(self, opcode, block, size, data):
        super().__init__(opcode)
        self.block = block
        self.size = size
        self.data = data

    def getBlock(self):
        return self.block
    def getSize(self):
        return self.size
    def getData(self):
        return self.data


class ACK(Packet):
    def __init__(self, opcode, block):
        super().__init__(opcode)
        self.block = block

    def getBlock(self):
        return self.block


class ERR(Packet):
    def __init__(self, opcode, error):
        super().__init__(opcode)
        self.error = error

    def printError(self):
        print(self.error)