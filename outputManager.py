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
    f = open('{0}{1}'.format(targetdir,'/sym.txt'), 'w')
    dashedLine = '-' * 65 
    headers = '{0:^10}'.format('Symbol') + '|' +'{0:^9}'.format('Defined') +'|' +'{0:^12}'.format('References')

    txt = dashedLine + '\n' + headers +'\n' + dashedLine + '\n'
    for i in symbolsTable:
        refs = ' '+ ",".join(["0x{0:0=4X}".format(x) for x in symbolsTable[i].refs])
        txt +='{0:^10}'.format(i) + '|' +'{0:^9}'.format("0x{0:0=4X}".format(symbolsTable[i].address)) +  '|' + '{0}'.format(refs) +'\n'

    f.write(txt)
    f.close()

def createObjFile(lines,targetPath):
    pass