from lxml import etree
from collections import OrderedDict

def create_xml_element(tag_name, attributes=None, text=None, children=None):
    element = etree.Element(tag_name, **(attributes or {}))
    children = list(filter(lambda item: item is not None, children))
        
    if text is not None:
        element.text = text
    
    if children is not None:
        for child in children:
            element.append(child)
    
    return element

def createCodeLisTyp(xml_elem, ver, code_name, muss):
    var_1 = create_xml_element('f', {'name': 'code'}, code_name, [])
    var_2 = create_xml_element('zeile', {'index': 'tns:' + xml_elem, 'xml': 'j', 'muss': muss, 'xmlKonstanteAttribute': 'listVersionID="' + ver + '"'}, '\n            ', [var_1])
    return var_2

def createAttribsDict(attribs, xml_elem):
    tmp_dict = OrderedDict([])
    if attribs is not None:
        for attrib in attribs:
            key,value = attrib.split(':')
            tmp_dict.update({key: value})
    dict1 = OrderedDict([('name', 'tns:' + xml_elem)])
    dict1.update(tmp_dict)
    return dict(dict1)

def createAttribsDict_wExPrms(attribs, xml_name, xml, muss):
    tmp_dict = OrderedDict([])
    if attribs is not None:
        for attrib in attribs:
            key,value = attrib.split(':')
            tmp_dict.update({key: value})
    if muss == '':
        dict1 = OrderedDict([('name', 'tns:' + xml_name), ('xml', xml)])
    else:
        dict1 = OrderedDict([('name', 'tns:' + xml_name), ('xml', xml), ('muss', muss)])
    dict1.update(tmp_dict)
    return dict(dict1)

def createFElem(xml_elem, attribs, name):
    var_14 = create_xml_element('f', createAttribsDict(attribs, xml_elem), name, [])
    return var_14

def createZeileElem_withName(vars_lst, xml_index, xml, muss):
    if muss == '':
        var_14 = create_xml_element('zeile', {'index': 'tns:' + xml_index, 'xml': xml}, '\n            ', vars_lst)
    else:
        var_14 = create_xml_element('zeile', {'index': 'tns:' + xml_index, 'xml': xml, 'muss': muss}, '\n            ', vars_lst)
    return var_14

def createZeileElem(vars_lst, muss):
    if muss == '':
        var_14 = create_xml_element('zeile', None, '\n            ', vars_lst)
    else:
        var_14 = create_xml_element('zeile', {'muss': muss}, '\n            ', vars_lst)
    return var_14

def createBlockElem_withName(vars_lst, attribs, xml_name, xml, muss):
    var_14 = create_xml_element('block', createAttribsDict_wExPrms(attribs, xml_name, xml, muss), '\n        ', vars_lst)
    return var_14

def createBlockElem(vars_lst, xml, muss):
    if muss == '':
        var_14 = create_xml_element('block', {'xml': xml}, '\n        ', vars_lst)
    else:
        var_14 = create_xml_element('block', {'xml': xml, 'muss': muss}, '\n        ', vars_lst)
    return var_14

if __name__ == 'main':
    var_1 = createCodeLisTyp('absender.gericht', '3.5', 'BK$bhkennz', 'n')
    var_2 = createFElem('absender.sonstige', None, 'absender.sonstige')
    var_3 = createZeileElem([var_2], 'n')
    var_4 = createBlockElem_withName([var_1, var_3], None, 'auswahl_absender', 'j', 'n')

    root_element = var_4

    # Pretty-print the XML
    xml_string = etree.tostring(root_element, pretty_print=True, encoding="unicode")
    with open('output_pp.xml', 'w+') as f:
        f.write(xml_string)