from InstructionSet import InstructionSet
from line import Line,symbol,output
import filesWriterManager
import sys

def link(prog1,prog2):
    if prog2 is None:
        return prog1

    resolveFirst(prog1,prog2)
    resolveFirst(prog2,prog1)
    for sym in prog2.symbolTable:
        prog1.symbolTable[sym] = prog2.symbolTable[sym] 
    
    for df in prog2.extDefs:
        prog1.extDefs[df]= prog2.extDefs[df]
    
    for rf in prog2.extRefs:
        prog1.extRefs[rf]= prog2.extDefs[rf]

    prog1.lines.extend(prog2.lines)
    return prog1


def resolveFirst(prog1,prog2):
    toDeleteRefs=[]
    for i in prog1.extRefs:
        if i in prog2.extDefs:
            for loc in prog1.extRefs[i]: #modify lines that contain that ref
                lin =None
                for iy in prog1.lines:
                    if iy.address ==loc:
                        lin=iy
                        break
                
                lin.hexOperand = prog2.extDefs[i]
                lin.hexaOutput = "0x{0:0=1X}{1:0=3X}".format(
                    InstructionSet[lin.opcode.lower()],lin.hexOperand)
                prog2.symbolTable[i].refs.append(lin.address)

            toDeleteRefs.append(i)
            
    for delRef in toDeleteRefs:
        prog1.extRefs.pop(delRef)

def main(paths):
    #paths= ['example.txt']
    outs=[]
    for pth in paths:
        start=0
        if len(outs) !=0:
            start =outs[-1].lines[-1].address + 1
        out =output(pth,start)
        out.process() #assembling
        outs.append(out)

    from functools import reduce
    reduce(link,outs)
    filesWriterManager.clean('./result')
    filesWriterManager.createLstFile(outs[0].lines,outs[0].startAddress,'./result')
    filesWriterManager.createSymFile(outs[0].symbolTable,'./result')
    filesWriterManager.createObjFile(outs[0].lines,outs[0].symbolTable,"test",outs[0].startAddress,'./result')


if __name__ == "__main__":
    #main(sys.argv[1:]) #ex: python main.py example2.txt example3.txt example4.txt
    main(['example.txt'])
    #main(['example2.txt','example3.txt','example4.txt',])
    print("done")
