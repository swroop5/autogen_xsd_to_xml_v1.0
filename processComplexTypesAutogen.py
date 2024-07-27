from lxml import etree
import autogen_xml_block as axb
from collections import namedtuple
import json

# Define a named tuple structure
XML_OBJ = namedtuple("XML_OBJ", ["name", "typ", "indent", "muss"])

def xtractXmlObjLstFromFile(filename):
    lines = []
    with open(filename, 'r+') as f:
        lines = f.readlines()

    xml_obj_lst = []
    for line in lines:
        indent = line.count('\t')
        xml_elem = ''
        typ = ''
        muss = ''
        values = line.split(',')
        if values is None:
            continue
        if len(values) == 1:
            xml_elem, typ = values[0], ''
        elif len(values) == 2:
            xml_elem, typ = values[0], values[1]
        elif len(values) == 3:
            xml_elem, typ, muss = values[0], values[1], values[2]
        elif len(values) == 4:
            xml_elem, typ, muss = values[0], values[1], f'{values[2]},{values[3]}'
        elif len(values) == 5:
            xml_elem, typ, muss = values[0], values[1], f'{values[2]},{values[3]},{values[4]}'
        if xml_elem is None or xml_elem == '':
            continue
        xml_elem = xml_elem.strip('\t')
        typ = typ.strip('\n')
        xml_obj = XML_OBJ(
            name=xml_elem, typ=typ, indent=indent, muss=muss
        )
        xml_obj_lst.append(xml_obj)
    return xml_obj_lst

def processTyps(xml_obj:XML_OBJ, muss):
    res = ''
    if 'Code.' in xml_obj.typ:
        ver = '3.5'
        if '.Typ3' in xml_obj.typ:
            codelistenTypName = xml_obj.typ[14:-5]
            key = codelistenTypName.lower()
            if key in codeListenTyp1_Typ3VersDict.keys():
                ver = codeListenTyp1_Typ3VersDict[key]
            else:
                print("Typ 3 Code listen Version missing: " + key)
            res = axb.createCodeLisTyp(xml_obj.name, ver, xml_obj.name.capitalize(), muss)
        else:
            codelistenTypName = xml_obj.typ[9:]
            key = codelistenTypName
            if key in codeListenTyp1_Typ3VersDict.keys():
                ver = codeListenTyp1_Typ3VersDict[key]
            else:
                print("Typ 1 Code listen Version missing: " + key)
                print("Code listen Version To be filled manually: " + xml_obj.typ)
            res = axb.createCodeLisTyp(xml_obj.name, ver, xml_obj.name.capitalize(), muss)
        return res
    elif 'DatumsType' in xml_obj.typ:
        res = axb.createFElem(xml_obj.name, ['konvertierungsmethode:konvDatum yyyyMMdd yyyy-MM-dd'], xml_obj.name.capitalize())
        return res
    elif 'datatype' in xml_obj.typ or 'boolean' in xml_obj.typ or 'double' in xml_obj.typ or 'xs:date'  in xml_obj.typ or 'xs:gYear'  in xml_obj.typ or 'stringUUIDType' in xml_obj.typ:
        res = axb.createFElem(xml_obj.name, None, xml_obj.name.capitalize())
        return res
    elif 'type' == xml_obj.typ or '' == xml_obj.typ or 'type ' == xml_obj.typ:
        res = ''
        return res

def processMussVal(xml_obj:XML_OBJ):
    res = ''
    if '1..' in xml_obj.muss:
        res = 'j'
    elif '0..' in xml_obj.muss:
        res = 'n'
    else:
        res = 'j'
    return res

def getChildElems(xml_obj_list, index, indent):
    result = []
    count = index + 1
    while count < len(xml_obj_list) and indent < xml_obj_list[count].indent:
        result.append(xml_obj_list[count])
        count = count + 1
    return result

def getCodeListenTyp1_Typ3Dict(filename):
    # Initialize an empty dictionary to store the merged data
    codelistenTyp1_Typ3Vers_dict = {}
    # Open the file for reading
    with open(filename, "r") as file:
        # Read each line (which represents a dictionary) from the file
        for line in file:
            # Parse the JSON string into a Python dictionary
            if line and line != '\n':
                data_dict = json.loads(line)
                # Merge the dictionary into the merged_dict
                codelistenTyp1_Typ3Vers_dict.update(data_dict)
    return codelistenTyp1_Typ3Vers_dict

def processXMLObjLst(xml_obj_list = [], indent = 0):
    res = []
    klein_lst = []
    index = 0
    index_upd_flg = False
    f_elems_lst = []
    while index < len(xml_obj_list):
        obj = xml_obj_list[index]
        if obj.name == '':
            continue
        muss = processMussVal(obj)
        xml_elem_obj = processTyps(obj, muss)
        indent_obj = int(obj.indent)
        klein_lst = getChildElems(xml_obj_list, index, indent_obj)
        if '' == xml_elem_obj and len(klein_lst) > 0:
            if len(f_elems_lst) > 0:
                res.append(axb.createZeileElem(f_elems_lst, 'n'))
            f_elems_lst = []
            index_upd_flg = False
            block_elems_lst = []
            block_elems_lst.extend(processXMLObjLst(klein_lst, indent_obj))
            index = index + len(klein_lst) + 1
            index_upd_flg = True
            res.append(axb.createBlockElem_withName(block_elems_lst, None, obj.name, 'j', ''))
        else:
            index_upd_flg = False
            if 'DatumsType' in obj.typ or 'datatype' in obj.typ or 'boolean' in obj.typ or 'double' in obj.typ or 'xs:date'  in obj.typ or 'xs:gYear'  in obj.typ or 'stringUUIDType' in obj.typ:
                f_elems_lst.append(xml_elem_obj)
                index = index + 1
                continue
            else:
                if len(f_elems_lst) > 0:
                    res.append(axb.createZeileElem(f_elems_lst, 'n'))
                f_elems_lst = []
            if xml_elem_obj != '':
                res.append(xml_elem_obj)
        if index_upd_flg == False:
            index = index + 1
    if len(f_elems_lst) > 0:
        res.append(axb.createZeileElem(f_elems_lst, 'n'))
    f_elems_lst = []
    return res
            
#block_name = 'output_Type.STRAF.Fachdaten.Strafverfahren'
#block_name = 'output_Type.STRAF.HyDaNe'
#block_name = 'output_nachricht.straf.owi.verfahrensmitteilung.externAnJustiz.0500010'
block_name = 'output_Type.STRAF.Tatvorwurf'
block_name = 'output_Type.GDS.Grunddaten'
codeListenTyp3Filename = "all_codelisten_vers_typ1_typ3.txt"
#block_name = 'output_Type.STRAF.Fachdaten.Strafverfahren'
filename = block_name + '.txt'
xml_obj_lst = xtractXmlObjLstFromFile(filename)
codeListenTyp1_Typ3VersDict = getCodeListenTyp1_Typ3Dict(codeListenTyp3Filename)
xml_elems_list = processXMLObjLst(xml_obj_lst, -1)
xml_elems_root = axb.createBlockElem_withName(xml_elems_list, None, block_name, 'j', 'n')
# Pretty-print the XML
xml_string = etree.tostring(xml_elems_root, pretty_print=True, encoding="unicode")
with open('output_pp.xml', 'w+') as f:
    f.write(xml_string)