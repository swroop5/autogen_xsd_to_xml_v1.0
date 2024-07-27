import os
from lxml import etree

def extract_complex_type_names(folder_path, namespace):
    # List all files in the folder
    files = [file for file in os.listdir(folder_path) if file.endswith(('.xsd', '.xml'))]

    # Create an empty list to store the extracted names
    complex_type_names = []

    complex_types = []
    complex_type_dict = {}
    # Process each file
    for file in files:
        file_path = os.path.join(folder_path, file)

        # Parse the XML/XSD file
        tree = etree.parse(file_path)
        root = tree.getroot()

        ns = {'real_person': "http://www.w3.org/2001/XMLSchema",
            'role': "http://www.xjustiz.de"}

        for actor in root.findall('real_person:complexType', ns):
            complex_types.append(actor)
            name = actor.get('name')
            if name:
                complex_type_names.append(name)
            for seq in actor:
                name = seq.findall('real_person:element', ns)
                if name is not None:
                    for child in name:
                        if child is not None:
                            print(child.get('name'), child.get('type'))
                            complex_type_dict[name] = [child.get('name'), child.get('type')]
    
    for ctype in complex_types:
        name = ctype.get('name')
        if name:
            complex_type_names.append(name)
            for seq in actor:
                name = seq.findall('real_person:element', ns)
                if name is not None:
                    for child in name:
                        if child is not None:
                            print(child.get('name'), child.get('type'))
                            complex_type_dict[name] = [child.get('name'), child.get('type')]
            
    return complex_type_dict

def extract_nachrichten_type(folder_path):
    # List all files in the folder
    files = [file for file in os.listdir(folder_path) if file.endswith(('.xsd', '.xml'))]

    # Create an empty list to store the extracted names
    nachrichten_type_names = []

    nachrichten_types = []
    # Process each file
    for file in files:
        file_path = os.path.join(folder_path, file)

        # Parse the XML/XSD file
        tree = etree.parse(file_path)
        root = tree.getroot()

        ns = {'real_person': "http://www.w3.org/2001/XMLSchema",
            'role': "http://www.xjustiz.de"}

        for actor in root.findall('real_person:element', ns):
            
            if actor is not None and 'nachricht.' in actor.get('name'):
                nachrichten_types.append(actor)
            # name = actor.get('name')
            # if name:
            #     complex_type_names.append(name)
            # for seq in actor:
            #     name = seq.findall('real_person:element', ns)
            #     if name is not None:
            #         for child in name:
            #             if child is not None:
            #                 print(child.get('name'), child.get('type'))
    
    for ctype in nachrichten_types:
        name = ctype.get('name')
        if name:
            nachrichten_type_names.append(name)
    return nachrichten_type_names

# Example usage:
folder_path = 'C:\\XjustizVersionen\\V3.4.1\\XJustiz_3_4_1_XSD\\XJustiz 3.4.1 XSD\\'

target_namespace = 'http://www.example.com/namespace'  # Replace with your predefined namespace
result = extract_complex_type_names(folder_path, target_namespace)
#print(result)

with open('output_complex_types_xsd.txt', 'w+') as f:
    for typ in result:
        f.write(typ + '  =  ' + result[typ])

# result = extract_nachrichten_type(folder_path)
# print(result)
