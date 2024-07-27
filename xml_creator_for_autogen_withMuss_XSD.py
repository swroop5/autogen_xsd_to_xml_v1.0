

def splitIntoDataTypes(lines):
    resultLst = []
    ind = 0
    if ind < len(lines)-1:
        while lines[ind] and ind < len(lines)-1:
            finished = False
            if 'start#' in lines[ind]:
                datatypeLst = []
                while 'finish#' not in lines[ind]:
                    datatypeLst.append(lines[ind])
                    if ind < len(lines)-1:
                        ind = ind +1
                else:
                    if ind < len(lines)-1:
                        ind = ind + 1
                    finished = True
            else:
                if ind < len(lines)-1:
                    ind = ind + 1
            if finished:
                resultLst.append(datatypeLst[1:])
                finished = False
    return resultLst

def printData(datatypes):
    for datatype in datatypes:
        for elem in datatype:
            print(elem)

def printAllDatatypes(datatypes):
    for datatype in datatypes:
        for elem in datatype:
            if 'complexType' in elem:
                print(elem[12:])

def printAllCodeTypes(datatypes):
    for datatype in datatypes:
        for elem in datatype:
            if elem.startswith('Codelisten Code.'):
                print(elem[16:])

def printXMLTags(datatype, datatypes, fw, tabs):
    xmlTagsLst = []
    tabsCopy = tabs + ''
    for elem in datatype:
        if all(char.isspace() for char in elem):
            elem = elem.strip('\t')
            fw.write(',' + elem)
            continue
        if 'complexType' in elem:
            continue
        if '(extension of tns:' in elem:
            elemCopy = elem.strip('\t')
            elemCopy = elemCopy.strip(')\n')
            elemCopy = elemCopy[18:]
            tabsCopy = processTypGDSComplexTypes(elemCopy, elem, datatype, datatypes, tabsCopy, tabs, fw)
        if '0..1' in elem or '1..1' in elem or '.*' in elem or '..' in elem or '(' in elem or ')' in elem:
            fw.write(',' + elem)
            continue
        #if 'type tns:Type.' in elem:
        if 'type ' in elem:
            if 'type tns:Type.' in elem:
                elemCopy = elem.strip('\t')
                if 'type tns:Type.GDS.Akte\n' == elemCopy or 'type tns:Type.GDS.Teilakte\n' == elemCopy or 'type tns:Type.GDS.Dokument\n' == elemCopy:
                    continue
                else:
                    tabsCopy = processTypGDSComplexTypes(elemCopy[9:], elem, datatype, datatypes, tabsCopy, tabs, fw)
                    continue
            else:
                elem = elem.strip('\t')
                fw.write(',' + elem)
                continue
        #print(elem)
        elem = elem.strip('\n')
        fw.write(tabs + elem)

def get_continuous_tabs(input_string):
    continuous_tabs = ""
    
    for char in input_string:
        if char == '\t':
            continuous_tabs += char
        else:
            break  # Stop when a non-tab character is encountered
    
    return continuous_tabs

def processTypGDSComplexTypes(elem, elem_raw, datatype, datatypes, tabsCopy, tabs, fw):
    tabs_carry = get_continuous_tabs(elem_raw)
    elem = elem.strip('\t')
    if elem not in datatype[0]:
        for data in datatypes:
            if 'complexType ' + elem in data[0]:
                if not 'Type.GDS.Xdomea.stringUUIDType' in data[0] and \
                            not 'Type.GDS.Datumsangabe' in data[0] and \
                                not 'Type.GDS.Zeitangabe' in data[0]:
                    fw.write(",type \n")
                    tabsCopy = tabsCopy + '\t' + tabs_carry
                printXMLTags(data, datatypes, fw, tabsCopy)
                if not 'Type.GDS.Xdomea.stringUUIDType' in data[0] and \
                            not 'Type.GDS.Datumsangabe' in data[0] and \
                                not 'Type.GDS.Zeitangabe' in data[0]:
                    tabsCopy = tabs + ''
                break
        else:
            print(elem + '    ' + data[0])
    else:
        fw.write(',' + elem)
    return tabsCopy
        

nachricht_type = 'Type.GDS.Grunddaten'
indNach = 0
with open("output_complex_types_xsd_tabbed.txt", "r+") as f:
    lines = f.readlines()
    datatypes = splitIntoDataTypes(lines)
    for index, type in enumerate(datatypes):
        if nachricht_type in type[0]:
            indNach = index
            break
    with open("output_" + nachricht_type + ".txt", "w+") as fw:
        printXMLTags(datatypes[indNach], datatypes, fw, '')
   
