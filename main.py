InstructionSet ={
                'load' : 0x1,
                'store' :0x2,
                'add':0x3,
                'subt':0x4,
                'input':0x5,
                'output':0x6,
                'halt':0x7,
                'skipcond':0x8,
                'jump':0x9,
                'clear':0xA,
                'addi':0xB,
                'jumpi':0xC,
                'loudv':0xD,
                'addv':0xE,
                'subtv':0xF,
                }
class Line:
    def __init__(self,address,lineStr):
        self.address= address
        self.tokens =lineStr.split()
        self.hexaOutput= 0
        self.processTokens()
    
    def processTokens(self):
        self.label =''
        self.opcode =''
        self.operand =''
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
        

    def output(self):
        pass



def assemble():
    f =open('example.txt','r')
    allLines = f.read().split('\n')
    startingAddress = 0X64
    symTable= {}
    result = []
    for i,line in enumerate(allLines):
        newLine=Line( int(hex(i),16) + startingAddress,line)
        result.append(newLine)
        if newLine.label !='':
            symTable[newLine.label] =newLine.address
    
    for line in result:
        if line.operand in symTable.keys():
           line.operand = symTable[line.operand]

        output =0
        if line.opcode.lower() not in ['dec','hex','halt','clear','input','output']:
            output = "0x{0:0=1X}{1:0=3X}".format(InstructionSet[line.opcode.lower()],line.operand)
        elif line.opcode.lower() == 'dec':
            output = "0x{0:0=4X}".format(int(line.operand))
        elif line.opcode.lower() == 'hex':
            output ="0x{0:0=4X}".format(line.operand)
        else:
            output = "0x{0:0=4X}".format(InstructionSet[line.opcode.lower()])

    
        line.hexaOutput = output

    print([i.hexaOutput for i in result],sep='\n')



if __name__ == "__main__":
    assemble()