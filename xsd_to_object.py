from lxml import etree

xsd_path = 'C:\\XjustizVersionen\\V3.4.1\\XJustiz_3_4_1_XSD\\XJustiz 3.4.1 XSD\\'
# Path to the XSD schema file
xsd_file = xsd_path + "xjustiz_0000_grunddatensatz_3_4.xsd"


# Load the XSD schema file
tree = etree.parse(xsd_file)

root = tree.getroot()

#print(root.tag + ' ' + str(root.attrib))

# for child in root:
#     print(child.tag, child.attrib)

# for country in root.findall('xs:complexType'):
#     rank = country.find('xs:element').text
#     name = country.get('name')
#     print(name, rank)

ns = {'name_space': "http://www.w3.org/2001/XMLSchema",
      'role': "http://www.xjustiz.de"}

for actor in root.findall('name_space:complexType', ns):
    for seq in actor:
        name = seq.findall('name_space:element', ns)
        if name is not None:
            for child in name:
                if child is not None:
                    #print(child.get('name'), child.get('type'))
                    pass

# Define a function to recursively process complexType elements
def process_complex_type(element):
    # Check if the current element is a complexType
    if element.tag.endswith('complexType'):
        # Process the contents of the complexType here
        # For example, you can access its name, attributes, child elements, etc.
        print("Processing complexType:", element.get('name'))
        # Add your code here to handle the complexType content as per your requirement

    # Recursively process child elements
    for child in element:
        process_complex_type(child)

# Start processing from the root element
process_complex_type(root)
