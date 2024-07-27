import os
from lxml import etree

def extract_complex_type_names(folder_path, namespace):
    files = [file for file in os.listdir(folder_path) if file.endswith(('.xsd', '.xml'))]

    complex_type_dict = {}

    ns = {'real_person': "http://www.w3.org/2001/XMLSchema", 'role': "http://www.xjustiz.de"}

    for file in files:
        file_path = os.path.join(folder_path, file)
        tree = etree.parse(file_path)
        root = tree.getroot()

        for actor in root.findall('.//real_person:complexType', ns):
            name = actor.get('name')
            if name:
                complex_type_dict[name] = []

                for seq in actor.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}sequence'):
                    for child in seq.iterchildren(tag='{http://www.w3.org/2001/XMLSchema}element'):
                        element_name = child.get('name')
                        element_type = child.get('type')
                        complex_type_dict[name].append((element_name, element_type))
    
    return complex_type_dict

# Example usage:
folder_path = 'C:\\XjustizVersionen\\V3.4.1\\XJustiz_3_4_1_XSD\\XJustiz 3.4.1 XSD\\'

target_namespace = 'http://www.example.com/namespace'  # Replace with your predefined namespace
result = extract_complex_type_names(folder_path, target_namespace)
#print(result)

with open('output_complex_types_xsd.txt', 'w+') as f:
    for typ, elements in result.items():
        f.write(f"{typ} = {elements}\n")
