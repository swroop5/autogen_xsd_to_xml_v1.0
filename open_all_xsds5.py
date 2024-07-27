import os
from lxml import etree

def extract_complex_types(root, ns):
    complex_type_dict = {}

    actor_count = 0
    for actor in root.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}complexType'):
        actor_count = actor_count + 1
    for actor in root.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}complexType'):
        name = actor.get('name')
        
        if name:
            pass
        elif actor_count == 1:
            name = root.get('name')

        if 'Code.' in name:
            continue
        complex_type_dict[name] = []

        for attr in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}attribute'):
            element_name = attr.get('name')
            element_type = attr.get('type')
            complex_type_dict[name].append((element_name, element_type))
        for seq in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
            for choice in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}choice'):
                for child in choice.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                    element_name = child.get('name')
                    element_type = child.get('type')
                    if element_type is None:
                        element_type = extract_nachrichten_type(child, ns)
                    complex_type_dict[name].append((element_name, element_type))
            for child in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                element_name = child.get('name')
                element_type = child.get('type')
                if element_type is None:
                    element_type = extract_complex_types(child, ns)
                complex_type_dict[name].append((element_name, element_type))
        for seq in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
            for sub_seq in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
                for child in sub_seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                    element_name = child.get('name')
                    element_type = child.get('type')
                    if element_type is None:
                        element_type = extract_nachrichten_type(child, ns)
                    complex_type_dict[name].append((element_name, element_type))
        for choice in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}choice'):
            for child in choice.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                element_name = child.get('name')
                element_type = child.get('type')
                if element_type is None:
                    element_type = extract_complex_types(child, ns)
                complex_type_dict[name].append((element_name, element_type))

        for choice in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}choice'):
            for seq in choice.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
                for child in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                    element_name = child.get('name')
                    element_type = child.get('type')
                    if element_type is None:
                        element_type = extract_nachrichten_type(child, ns)
                    complex_type_dict[name].append((element_name, element_type))
        for complexContent in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}complexContent'):
            for child in complexContent.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}extension'):
                complex_type_dict[name].append(('extension of', child.get('base')))
                for seq in child.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
                    for elem in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                        element_name = elem.get('name')
                        element_type = elem.get('type')
                        if element_type is None:
                            element_type = extract_nachrichten_type(elem, ns)
                        complex_type_dict[name].append((element_name, element_type))
                for choice in child.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}choice'):
                    for child2 in choice.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                        element_name = child2.get('name')
                        element_type = child2.get('type')
                        if element_type is None:
                            element_type = extract_nachrichten_type(child, ns)
                        complex_type_dict[name].append((element_name, element_type))

        for complexContent in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}complexContent'):
            for child in complexContent.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}restriction'):
                complex_type_dict[name].append(('restriction of', child.get('base')))
                for seq in child.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
                    for elem in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                        element_name = elem.get('name')
                        element_type = elem.get('type')
                        if element_type is None:
                            element_type = extract_nachrichten_type(elem, ns)
                        complex_type_dict[name].append((element_name, element_type))
                
    return complex_type_dict

def extract_complex_type_names(folder_path, namespace):
    files = [file for file in os.listdir(folder_path) if file.endswith(('.xsd', '.xml'))]

    complex_type_dict = {}

    ns = {'real_person': "http://www.w3.org/2001/XMLSchema", 'role': "http://www.xjustiz.de"}

    for file in files:
        file_path = os.path.join(folder_path, file)
        tree = etree.parse(file_path)
        root = tree.getroot()
        complex_type_dict.update(extract_complex_types(root, ns))
        
    return complex_type_dict


def extract_nachrichten_type(root, ns):
    nachricht_type_dict = {}

    actor_count = 0
    for actor in root.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}complexType'):
        actor_count = actor_count + 1
    for actor in root.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}complexType'):
        name = actor.get('name')
        
        if name:
            pass
        elif actor_count == 1:
            name = root.get('name')

        if 'Code.' in name:
            continue
        nachricht_type_dict[name] = []

        for attr in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}attribute'):
            element_name = attr.get('name')
            element_type = attr.get('type')
            nachricht_type_dict[name].append((element_name, element_type))
        for seq in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
            for choice in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}choice'):
                for child in choice.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                    element_name = child.get('name')
                    element_type = child.get('type')
                    if element_type is None:
                        element_type = extract_nachrichten_type(child, ns)
                    nachricht_type_dict[name].append((element_name, element_type))
            for child in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                element_name = child.get('name')
                element_type = child.get('type')
                if element_type is None:
                    element_type = extract_nachrichten_type(child, ns)
                nachricht_type_dict[name].append((element_name, element_type))
        for seq in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
            for sub_seq in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
                for child in sub_seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                    element_name = child.get('name')
                    element_type = child.get('type')
                    if element_type is None:
                        element_type = extract_nachrichten_type(child, ns)
                    nachricht_type_dict[name].append((element_name, element_type))
        for choice in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}choice'):
            for child in choice.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                element_name = child.get('name')
                element_type = child.get('type')
                if element_type is None:
                    element_type = extract_nachrichten_type(child, ns)
                nachricht_type_dict[name].append((element_name, element_type))
        for choice in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}choice'):
            for seq in choice.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
                for child in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                    element_name = child.get('name')
                    element_type = child.get('type')
                    if element_type is None:
                        element_type = extract_nachrichten_type(child, ns)
                    nachricht_type_dict[name].append((element_name, element_type))
        for complexContent in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}complexContent'):
            for child in complexContent.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}extension'):
                nachricht_type_dict[name].append(('extension of', child.get('base')))
                for seq in child.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
                    for elem in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                        element_name = elem.get('name')
                        element_type = elem.get('type')
                        if element_type is None:
                            element_type = extract_nachrichten_type(elem, ns)
                        nachricht_type_dict[name].append((element_name, element_type))
                for choice in child.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}choice'):
                    for child2 in choice.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                        element_name = child2.get('name')
                        element_type = child2.get('type')
                        if element_type is None:
                            element_type = extract_nachrichten_type(child, ns)
                        nachricht_type_dict[name].append((element_name, element_type))

        for complexContent in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}complexContent'):
            for child in complexContent.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}restriction'):
                nachricht_type_dict[name].append(('restriction of', child.get('base')))
                for seq in child.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
                    for elem in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                        element_name = elem.get('name')
                        element_type = elem.get('type')
                        if element_type is None:
                            element_type = extract_nachrichten_type(elem, ns)
                        nachricht_type_dict[name].append((element_name, element_type))
                
    return nachricht_type_dict

def extract_nachrichten_types(root, ns):
    nachricht_type_dict = {}

    actor_count = 0
    for actor in root.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
        actor_count = actor_count + 1
    for actor in root.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
        name = actor.get('name')
        
        if name:
            pass
        elif actor_count == 1:
            name = root.get('name')

        if 'nachricht' in name:
            if 'Code.' in name:
                continue
            nachricht_type_dict[name] = extract_nachrichten_type(actor, ns)

    return nachricht_type_dict

def extract_nachrichten_type_names(folder_path, namespace):
    files = [file for file in os.listdir(folder_path) if file.endswith(('.xsd', '.xml'))]

    nachricht_type_dict = {}

    ns = {'real_person': "http://www.w3.org/2001/XMLSchema", 'role': "http://www.xjustiz.de"}

    for file in files:
        file_path = os.path.join(folder_path, file)
        tree = etree.parse(file_path)
        root = tree.getroot()
        nachricht_type_dict.update(extract_nachrichten_types(root, ns))
        
    return nachricht_type_dict



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


def extractXMLTags(datatype):
    xmlTagsDict = {}
    key = ''
    name_type_tuple = tuple()
    for elem in datatype:
        elem = elem.strip('\t\n')
        if len(elem) == 0:
            continue
        if 'complexType' in elem:
            elem = elem.strip('\n')
            key = elem[8:]
            xmlTagsDict[key] = []
            continue
        if 'element nachricht' in elem:
            elem = elem.strip('\n')
            key = elem[8:]
            xmlTagsDict[key] = []
            continue
        if '(extension of tns:' in elem:
            elem = elem.strip(')\n')
            elem = elem[18:]
            xmlTagsDict[key].append(('extension of', elem))
            continue
        if 'anonymous simple type' in elem:
            elem = elem.strip('\n')
            name_type_tuple = name_type_tuple + (elem,)
            if len(name_type_tuple) == 2:
                xmlTagsDict[key].append(name_type_tuple)
                name_type_tuple = ()
                continue
        if '0..1' in elem or '1..1' in elem or '.*' in elem or '..' in elem or '(' in elem or ')' in elem:
            continue
        #if 'type tns:Type.' in elem:
        if elem.startswith('type'):
            elem = elem.strip('\n')
            name_type_tuple = name_type_tuple + (elem,)
            if len(name_type_tuple) == 2:
                xmlTagsDict[key].append(name_type_tuple)
                name_type_tuple = ()
                continue
        name_type_tuple = name_type_tuple + (elem,)
    return xmlTagsDict

def flattenResultDict(result):
    tups_lst = []
    res = dict()
    for typ, elements in result.items():
        tups_lst.extend(checkTypes(elements))
        res[typ] = tups_lst
        tups_lst = []
    return res

def checkTypes(element):
    if isinstance(element, dict):
        if len(element) == 1:
            for typ, elements in element.items():
                return element[typ]
    elif isinstance(element, tuple):
        return element
    elif isinstance(element, list):
        return element

def search_string_in_nested(data, search_string):
    if isinstance(data, str):
        return search_string == data or search_string == '@' + data

    if isinstance(data, dict):
        for value in data.values():
            if search_string_in_nested(value, search_string):
                return True

    if isinstance(data, list) or isinstance(data, tuple):
        for item in data:
            if search_string_in_nested(item, search_string):
                return True
    return False

def count_nested_elements(data):
    count = 0
    if isinstance(data, dict):
        for key in data.keys():
            if 'nachricht.' in key or 'Type.' in key:
                pass
            else:
                count = count + 1
        for value in data.values():
            count += count_nested_elements(value)
        return count

    if isinstance(data, list):
        #count = len(data)
        for item in data:
            count += count_nested_elements(item)
        return count
    
    if isinstance(data, tuple):
        if 'Type.GDS.Basisnachricht' in data[1]:
            pass
        elif 'extension of' == data[0]:
            return 0
        count += count_nested_elements(data[1])
        return count
        
    return 1


def parse_nested_elements(data, tabs=''):
    final_types_list = []
    if isinstance(data, dict):
        for key in data.keys():
            if 'nachricht.' in key or 'Type.' in key:
                pass
            else:
                final_types_list.append(key)
        for value in data.values():
            final_types_list.append(parse_nested_elements(value))
        return final_types_list

    if isinstance(data, list):
        #count = len(data)
        for item in data:
            final_types_list.append(parse_nested_elements(item))
        return final_types_list
    
    if isinstance(data, tuple):
        if 'Type.GDS.Basisnachricht' in data[1]:
            pass
        elif 'extension of' == data[0]:
            return 0
        tmp_lst = parse_nested_elements(data[1])
        if 'string' == tmp_lst:
            return data
        else:
            return tmp_lst
        return final_types_list
        
    return 'string'

def processComplexTypesDict(data, f, tabs=''):
    tabsCopy = tabs + ''
    if isinstance(data, list):
        if len(data) == 0:
            return
        if isinstance(data[0], str):
            for item in data:
                if isinstance(item, str):
                    if '\t' in tabsCopy:
                        last_tab_index = tabsCopy.rfind('\t')  # Find the last tab character index
                        modified_string = tabsCopy[:last_tab_index] + tabsCopy[last_tab_index+1:]
                    f.write(f"{modified_string + item}\n")
                    f.write(f"{modified_string}type \n")
                elif isinstance(item, tuple):
                    tmp_lst = processComplexTypesDict(item[1], f, tabsCopy)
                    if 'string' == tmp_lst:
                        f.write(f"{tabsCopy + item[0]}\n")
                        f.write(f"{tabsCopy}type {item[1]}\n")
                    else:
                        return tmp_lst
                else:
                    processComplexTypesDict(item, f, tabsCopy)
        else:    
            for item in data:
                if isinstance(item, str):
                    if '\t' in tabsCopy:
                        last_tab_index = tabsCopy.rfind('\t')  # Find the last tab character index
                        modified_string = tabsCopy[:last_tab_index] + tabsCopy[last_tab_index+1:]
                    f.write(f"{modified_string + item}\n")
                    f.write(f"{modified_string}type \n")
                elif isinstance(item, tuple):
                    tmp_lst = processComplexTypesDict(item[1], f, tabsCopy)
                    if 'string' == tmp_lst:
                        f.write(f"{tabsCopy + item[0]}\n")
                        f.write(f"{tabsCopy}type {item[1]}\n")
                    else:
                        return tmp_lst
                else:
                    processComplexTypesDict(item, f, tabsCopy + '\t')
        return
    if isinstance(data, tuple):
        tmp_lst = processComplexTypesDict(data[1], f, tabsCopy)
        if 'string' == tmp_lst:
            f.write(f"{tabsCopy + data[0]}\n")
            f.write(f"{tabsCopy}type {data[1]}\n")
        else:
            return tmp_lst
    return 'string'

# Example usage:
folder_path = 'C:\\XjustizVersionen\\V3.4.1\\XJustiz_3_4_1_XSD\\XJustiz 3.4.1 XSD\\'

target_namespace = 'http://www.example.com/namespace'  # Replace with your predefined namespace
result = extract_complex_type_names(folder_path, target_namespace)
#print(result)

complexTypesDict = {}
for typ, elements in result.items():
    complexTypesDict.update({typ: parse_nested_elements(elements, '')})

with open('output_complex_types_xsd_tabbed.txt', 'w+') as f:
    for typ, elements in complexTypesDict.items():
        f.write(f"start#\n")
        f.write(f"complexType {typ}\n")
        processComplexTypesDict(elements, f)
        f.write(f"finish#\n")
        
datatypes = []
xmlComplexTypesDict = dict()
with open("all_xjustiz_types.txt", "r+") as f:
    lines = f.readlines()
    datatypes = splitIntoDataTypes(lines)
    for complex_type, elements in result.items():
        for index, type in enumerate(datatypes):
            if complex_type in type[0]:
                indNach = index
                break
        xmlComplexTypesDict.update(extractXMLTags(datatypes[indNach]))

# with open('output_nachrichten_types_pdf.txt', 'w+') as f:
#     for typ, elements in xmlNachrichtTypesDict.items():
#         f.write(f"{typ} = {elements}\n")

# for typ, elements in xmlComplexTypesDict.items():
#     for typp, elems in result.items():
#         if typp in typ:
#             count = count_nested_elements(elems)
#             # if len(elements) == count:
#             #     print("Numbers match: " + str(len(elements)) + " vs " + str(count))
#             # else:
#             #     print(typ + " :  " + "Error in number of elems " + str(len(elements)) + " vs " + str(count))
#             for xml_elem_typs in elements:
#                 present = search_string_in_nested(elems, xml_elem_typs[0])
#                 if present:
#                     pass
#                 else:
#                     print('xsd type: ' + typp + '||pdf type: ' + typ + " :  " + xml_elem_typs[0]  + "  not found ")


# with open('output_complex_types_xsd.txt', 'w+') as f:
#     for typ, elements in result.items():
#         f.write(f"{typ} = {elements}\n")

result = extract_nachrichten_type_names(folder_path, target_namespace)
#print(result)

#result = flattenResultDict(result)

# with open('output_nachrichten_types_xsd_flat.txt', 'w+') as f:
#     for typ, elements in result.items():
#         f.write(f"{typ} = {elements}\n")

datatypes = []
xmlNachrichtTypesDict = dict()
with open("all_xjustiz_types.txt", "r+") as f:
    lines = f.readlines()
    datatypes = splitIntoDataTypes(lines)
    for nachricht_type, elements in result.items():
        for index, type in enumerate(datatypes):
            if nachricht_type in type[0]:
                indNach = index
                break
        xmlNachrichtTypesDict.update(extractXMLTags(datatypes[indNach]))

# with open('output_nachrichten_types_pdf.txt', 'w+') as f:
#     for typ, elements in xmlNachrichtTypesDict.items():
#         f.write(f"{typ} = {elements}\n")

for typ, elements in xmlNachrichtTypesDict.items():
    for typp, elems in result.items():
        if typp in typ:
            count = count_nested_elements(elems)
            #if len(elements) == count:
                #print("Numbers match: " + str(len(elements)) + " vs " + str(count))
            #else:
                #print(typ + " :  " + "Error in number of elems " + str(len(elements)) + " vs " + str(count))
            for xml_elem_typs in elements:
                present = search_string_in_nested(elems, xml_elem_typs[0])
                if present:
                    pass
                else:
                    print(typ + " :  " + xml_elem_typs[0]  + "  not found ")
