class Packet:
    def __init__(self, opcode):
        self.opcode = opcode

    def getCode(self):
        return self.opcode


class RRQ(Packet):
    def __init__(self, filename):
        super().__init__(1)
        self.filename = filename

    def getFIlename(self):
        return self.filename

class DAT(Packet):
    def __init__(self,  block, size, data):
        super().__init__(3)
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
    def __init__(self, block):
        super().__init__(4)
        self.block = block

    def getBlock(self):
        return self.block


class ERR(Packet):
    def __init__(self, error):
        super().__init__(5)
        self.error = error

    def printError(self):
        print(self.error)