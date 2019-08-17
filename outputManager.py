def createLstFile(lines, OrgAddress,targetdir):
    if len(lines) == 0:
        return

    lstFile = open('{0}{1}'.format(targetdir,'/listFile.txt'), 'w')

    strLines = []
    orgStr='ORG' + '  ' + '0x{0:0=4X}'.format(OrgAddress)+'\n'
    
    lstFile.writelines('{: ^35}'.format(' ') + orgStr)
    for l in lines:
        s = '{:<25}'.format("0x{0:0=4X}".format(l.address) + '  ' + str(l.hexaOutput) + ' |')
        s += '{:<10}'.format(l.label + ' ' if l.label != '' else ' ')
        s += '{:<10}'.format(l.opcode)
        s += '{:<20}'.format(str(l.operand) + ' ') + '\n'
        strLines.append(s)

    lstFile.writelines(strLines)
    lstFile.close()

def createSymFile(symbolsTable,targetdir): 
    dashedLine = '-' * 65 
    headers = '{0:^10}'.format('Symbol') + '|' +'{0:^9}'.format('Defined') +'|' +'{0:^12}'.format('References')

    txt = dashedLine + '\n' + headers +'\n' + dashedLine + '\n'
    for i in symbolsTable:
        refs = ' '+ ",".join(["0x{0:0=4X}".format(x) for x in symbolsTable[i].refs])
        txt +='{0:^10}'.format(i) + '|' +'{0:^9}'.format("0x{0:0=4X}".format(symbolsTable[i].address)) +  '|' + '{0}'.format(refs) +'\n'

    f = open('{0}{1}'.format(targetdir,'/sym.txt'), 'w')
    f.write(txt)
    f.close()

def createObjFile(lines,symTable,progName,startingAddress,targetdir):
    H = "H {0} {1:0=5X} {2:0=5X} \n".format(progName, startingAddress,len(lines))
    T = ""
    #tLines = 
    for t in divby(lines,4):
        T +="T {0:0=5X}".format(t[0].address)
        for line in t:
            T += " {0:0=5X}".format(int(line.hexaOutput,16)) 
            #T += " {0}".format(line.hexaOutput) 
        T +="\n"
    
    M = ""
    for sym in symTable:
        if len(symTable[sym].refs) == 0:
            continue
        M += "M {0:0=5X}".format(symTable[sym].address) + "   " + ",".join(["{0:0=5X}".format(x) for x in symTable[sym].refs]) + "\n"


    E = "E {0:0=5X}".format(startingAddress)
    f = open('{0}{1}'.format(targetdir,'/obj.txt'), 'w')
    f.write(H + T + M +E)
    f.close()


def divby(lst,n):
    for i in range(0,len(lst),n):
        yield lst[i:i+n]