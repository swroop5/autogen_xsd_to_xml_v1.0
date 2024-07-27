import xmltodict

def xml_file_to_dict(file_path):
    with open(file_path, 'r') as file:
        xml_string = file.read()
        return xmltodict.parse(xml_string)

# Example usage:
file_path = 'input.xml'
xml_dict = xml_file_to_dict(file_path)
print(xml_dict)

def dict_to_xml(xml_dict, root_node='root'):
    xml_string = xmltodict.unparse({root_node: xml_dict}, pretty=True)
    return xml_string

converted_xml_string = dict_to_xml(xml_dict)
print(converted_xml_string)

