from lxml import etree
import os
from os.path import join
import uuid

# Enter the path to your starting EAD directory
input_directory = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

type_dict = {}

# Enter the path to the output directory for the modified EADs
# Warning! If you set the output_directory to the same path as the input_directory,
# all of your original EADs will be overwritten
output_directory = 'C:/Users/djpillen/GitHub/test_dir'

# Loop through each file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".xml"):
        print filename
        ead = etree.parse(join(input_directory,filename))
        components = ead.xpath("//*[starts-with(local-name(), 'c0')]")
        # Check each component for multiple containers
        for component in components:
            containers = component.xpath('./did/container')
            # Only add ids and parent attributes if there are two containers
            if len(containers) == 2:
                child_type = containers[1].attrib['type']
                child_label = containers[1].attrib['label']
                if child_type != child_label:
                    if child_type not in type_dict:
                        type_dict[child_type] = []
                    if child_label not in type_dict[child_type]:
                        type_dict[child_type].append(child_label)

for child_type in type_dict:
    print child_type, type_dict[child_type]
