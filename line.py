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
    def __init__(self,filePath,startAddress):
        self.filePath = filePath
        self.startAddress = startAddress
        self.lines=[]
        self.extDefs= {}
        self.extRefs={}
        self.symbolTable={}

    def prepare(self):
        f = open(self.filePath, 'r')
        allLines = f.read().split('\n')
        if 'org' not in allLines[0].tolower():
            raise Exception("ORG Not Found")
            
        if 'extdef' in allLines[1].tolower():
            defs = allLines[1].tolower() - 'extdef'
            for df in defs.split(','):
                self.extDefs[df.strip()] =None

        if 'extref' in allLines[2].tolower():
            refs = allLines[1].tolower() - 'extref'
            refs = refs.split(',') 
            for rf in refs:
                self.extRefs[rf.strip()] = None
            

    def process(self):
        f = open('example.txt', 'r')
        allLines = f.read().split('\n')
        symTable = {}
        result = []
        viritualLineNumber = 0
        for i, line in enumerate(allLines):
            if line =='' or line.isspace():
                continue
            newLine = Line( int(hex(viritualLineNumber), 16) + self.startAddress, line, i)
            result.append(newLine)

            if newLine.label != '':
                symTable[newLine.label] = symbol(newLine.address,[])

            viritualLineNumber += 1
        
        for line in result:
            if line.operand in symTable.keys():
                lbl = line.operand
                line.hexOperand = symTable[lbl].address
                symTable[lbl].refs.append(line.address)
            if line.opcode.lower() == 'skipcond':
                line.hexOperand =int(line.operand,16)

            if line.opcode.lower() in ['hex','dec']:
                line.hexaOutput = "0x{0:0=4X}".format(int(line.operand))
            else:
                line.hexaOutput = "0x{0:0=1X}{1:0=3X}".format(
                    InstructionSet[line.opcode.lower()],line.hexOperand)


        self.lines,self.symbolTable = result,symTable
   

