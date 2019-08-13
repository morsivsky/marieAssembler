class Line:
    def __init__(self, address, lineStr, physicalLineNumber):
        self.address = address
        self.tokens = lineStr.split()
        self.hexaOutput = 0
        self.physicalLineNumber = physicalLineNumber  # line number at input txt file
        self.processTokens()

    def processTokens(self):
        self.label = ''
        self.opcode = ''
        self.operand = ''
        self.hexOperand=0
        self.directVal = ''
        if len(self.tokens) == 3:
            self.label = self.tokens[0][:-1]
            self.opcode = self.tokens[1]
            self.operand = self.tokens[2]
        if len(self.tokens) == 2:
            self.opcode = self.tokens[0]
            self.operand = self.tokens[1]
        if len(self.tokens) == 1:
            self.opcode = self.tokens[0]

class symbol:
    def __init__(self,address,refs):
        #self.symbol=symbol
        self.address=address
        self.refs=refs


   

