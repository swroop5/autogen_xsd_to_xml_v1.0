from lxml import etree
import re

child_tail_lxml = ''

def create_xml_element(tag_name, attributes=None, text=None, children=None):
    if isinstance(attributes, str):
        element = etree.Comment(attributes)
    else:
        element = etree.Element(tag_name, **(attributes or {}))
    
    if text is not None:
        element.text = text
    
    com_element = etree.Comment('text')
    if children is not None:
        for child in children:
            if isinstance(child, type(com_element)):
                element.append(child)
            else:
                element.append(child)
    
    return element


# def generate_xml_from_file(file_path):
#     root = None
#     with open(file_path, 'r', encoding='utf-8') as file:
#         root = etree.fromstring(file.read())
#     return root

def generate_xml_from_file(file_path):
    root = None
    parser = etree.XMLParser(encoding='utf-8')
    with open(file_path, 'r') as file:
        root = etree.parse(file, parser=parser).getroot()
    return root

def escape_newlines(text):
    if text == None:
        return
    return text.replace('\n', '\\n')

var_count = 0
def genVar():
    global var_count
    var_count = var_count + 1
    return 'var_' + str(var_count)

def generate_element_code(element):
    attributes = element.attrib
    text = escape_newlines(element.text)
    children_code_vars = []
    child_code_lines_list = []
    code = ''
    mod_text = ''
    comment_element = etree.Comment('text')
        
    for child in element:
        if isinstance(child, type(comment_element)):
            var_name, child_code = generate_element_code(child)
            child_code_lines_list.append(child_code)
            children_code_vars.append(var_name)
            child_tail_lxml = child.tail
        else:
            var_name, child_code = generate_element_code(child)
            child_code_lines_list.append(child_code)
            children_code_vars.append(var_name)
        
    for line in child_code_lines_list:
        code += (line + "\n")
    
    var_name = genVar()
    if isinstance(element, type(comment_element)):
        code += f'{var_name} = create_xml_element("dummy", """{str(element.text)} """, None, [])'
        #code += f'{var_name} = create_xml_element("comment", None, None, [])'
    else:
        if '{http://www.EDV-COMPAS.com/2005/icom}f' == element.tag and 'dummy' in code and len(children_code_vars) == 1:
            mod_text = f'"{escape_newlines(child_tail_lxml)}"'
        elif text is None:
            mod_text = None
        else:
            mod_text = f'"{text}"'
        code += f'{var_name} = create_xml_element("{element.tag}", {attributes}, {mod_text}, [{", ".join(children_code_vars)}])'
    return var_name, code

def getFElementsText(filename):
    
    f_element_comment_inside_list = []
    # Your XML pattern as a regular expression
    pattern = r'<\s*f\s+name="[^"]*">\s*<!--[^>]*-->\s*([^<]*)\s*</f>'

    with open(filename, 'r+') as f:
        lines = f.readlines()

    all_lines = ''
    for line in lines:
        all_lines += line

    # Find all matches in the XML document
    matches = re.findall(pattern, all_lines)

    # Extract and print the captured text content from each match
    for match in matches:
        f_element_comment_inside_list.append(match)
    return f_element_comment_inside_list


input_file_path = 'c:\\Users\\sy\\.icom\\formulare\\EIP_NACHRICHT_341.xml'
output_file_path = 'output.py'

f_elems_text_lst = getFElementsText(input_file_path)
root_element = generate_xml_from_file(input_file_path)
var_name, root_element_code = generate_element_code(root_element)

output_code = f"""
from lxml import etree

def create_xml_element(tag_name, attributes=None, text=None, children=None):
    if isinstance(attributes, str):
        attributes = attributes[:-1]
        element = etree.Comment(attributes)
    else:
        element = etree.Element(tag_name, **(attributes or {{}}))
    
    if text is not None:
        element.text = text
    
    com_element = etree.Comment('text')
    if children is not None:
        for child in children:
            if isinstance(child, type(com_element)):
                element.append(child)
            else:
                element.append(child)
            
    return element


# Create the XML structure
{root_element_code}

root_element = {var_name}

# Pretty-print the XML
xml_string = '<?xml version="1.0" encoding="UTF-8"?>\\n' + etree.tostring(root_element, pretty_print=True, encoding="unicode")
with open('output_pp.xml', 'w+', encoding="utf-8") as f:
    f.write(xml_string)
"""

with open(output_file_path, 'w') as output_file:
    output_file.write(output_code)

print(f"Output code has been written to '{output_file_path}'.")