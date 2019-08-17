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

        i =0
        if self.tokens[0][-1] ==',':
            self.label = self.tokens[0][:-1]
            i = 1

        self.opcode = self.tokens[i]
        i +=1

        if i < len(self.tokens):
            self.operand = self.tokens[i]

class symbol:
    def __init__(self,address,refs):
        #self.symbol=symbol
        self.address=address
        self.refs=refs


   

