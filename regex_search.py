import re

f_element_comment_inside_list = []
# Your XML pattern as a regular expression
pattern = r'<\s*f\s+name="[^"]*">\s*<!--[^>]*-->\s*([^<]*)\s*</f>'

with open('EIP_NACHRICHT_341.xml', 'r+') as f:
    lines = f.readlines()

all_lines = ''
for line in lines:
    all_lines += line

# Find all matches in the XML document
matches = re.findall(pattern, all_lines)

# Extract and print the captured text content from each match
for match in matches:
    f_element_comment_inside_list.append(match)
