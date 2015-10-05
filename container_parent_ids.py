from lxml import etree
import os
from os.path import join
import uuid
import random

# Enter the path to your starting EAD directory
input_directory = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

# Enter the path to the output directory for the modified EADs
# Warning! If you set the output_directory to the same path as the input_directory,
# all of your original EADs will be overwritten
output_directory = 'C:/Users/djpillen/GitHub/test_dir'

# Loop through each file in the input directory

for filename in os.listdir(input_directory):
    ead = etree.parse(join(input_directory,filename))
    components = ead.xpath("//*[starts-with(local-name(), 'c0')]")
    # Check each component for multiple containers
    for component in components:
        containers = component.xpath('./did/container')
        # Only add ids and parent attributes if there are two containers
        if len(containers) == 2:
            parent = containers[0]
            child = containers[1]
            parent_id = str(uuid.uuid4())
            parent.attrib['id'] = parent_id
            child.attrib['parent'] = parent_id
    with open(join(output_directory, filename), 'w') as new_ead:
        new_ead.write(etree.tostring(ead, encoding="utf-8", xml_declaration=True))
    print filename
