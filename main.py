from InstructionSet import InstructionSet
from line import Line,symbol
import outputManager

def assemble():
    f = open('example.txt', 'r')
    allLines = f.read().split('\n')
    startingAddress = 0x0
    symTable = {}
    result = []
    viritualLineNumber = 0
    for i, line in enumerate(allLines):
        if line =='' or line.isspace():
            continue
        newLine = Line( int(hex(viritualLineNumber), 16) + startingAddress, line, i)
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

    import os
    from shutil import rmtree
    if os.path.exists('./result'):
        rmtree('./result')

    os.mkdir('./result')

    outputManager.createLstFile(result, startingAddress,'./result')
    outputManager.createSymFile(symTable,'./result')
    outputManager.createObjFile(result,symTable,"test",startingAddress,'./result')


if __name__ == "__main__":
    assemble()
    print("done")
