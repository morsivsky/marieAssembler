from InstructionSet import InstructionSet

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


class output:
    def __init__(self,filePath,startAddress=0):
        self.filePath = filePath
        self.startAddress = startAddress
        self.lines=[]
        self.extDefs= {}
        self.extRefs={}
        self.symbolTable={}
            
    def isPreProcessorLine(self,string):
        return any(['ORG' in string,'EXTDEF' in string,'EXTREF' in string])
        

    def process(self):
        f = open(self.filePath, 'r')
        allLines = f.read().split('\n')
        if 'ORG' in allLines[0]:
            self.startAddress= int(allLines[0].replace('ORG',''),16)            
                
        viritualLineNumber = 0

        for i, line in enumerate(allLines):
            if  line =='' or line.isspace() or 'ORG' in line:
                continue

            if 'EXTDEF' in line:
                defs = line.replace('EXTDEF','')
                for df in defs.split(','):
                    self.extDefs[df.strip()] = None
                continue

            if 'EXTREF' in line:
                refs = line.replace('EXTREF','')
                refs = refs.split(',')
                for rf in refs:
                    self.extRefs[rf.strip()] = [] #places to be modfied when this rf is defined
                continue

            newLine = Line(int(hex(viritualLineNumber), 16) + self.startAddress, line, i)
            self.lines.append(newLine)

            if newLine.label != '':
                self.symbolTable[newLine.label] = symbol(newLine.address,[])
                if newLine.label in self.extDefs:
                    self.extDefs[newLine.label] =  newLine.address

            viritualLineNumber += 1
        
        for line in self.lines:
            lbl = line.operand
            if lbl in self.symbolTable: #else already 0
                line.hexOperand = self.symbolTable[lbl].address
                self.symbolTable[lbl].refs.append(line.address)
            elif lbl in self.extRefs:
                self.extRefs[lbl].append(line.address)
         
            if line.opcode.lower() == 'skipcond':
                line.hexOperand =int(line.operand,16)

            if line.opcode.lower() == 'dec':
                line.hexaOutput = "0x{0:0=4X}".format(int(line.operand))
            elif line.opcode.lower() == 'hex':
                line.hexaOutput = "0x{0:0=4}".format(int(line.operand))
            else:
                line.hexaOutput = "0x{0:0=1X}{1:0=3X}".format(
                    InstructionSet[line.opcode.lower()],line.hexOperand)