from InstructionSet import InstructionSet
from line import Line,symbol,output
import filesWriterManager
def funcname(parameter_list):
    pass

def main():
    out =output('example.txt',0)
    out.process()
    #rdeuce function to do linking   
    filesWriterManager.clean('./result')
    filesWriterManager.createLstFile(out.lines, out.startAddress,'./result')
    filesWriterManager.createSymFile(out.symbolTable,'./result')
    filesWriterManager.createObjFile(out.lines,out.symbolTable,"test",out.startAddress,'./result')

if __name__ == "__main__":
    main()
    print("done")
