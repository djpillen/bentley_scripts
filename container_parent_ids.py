from lxml import etree
import os
from os.path import join
import uuid
import re

path = 'C:/Users/Public/Documents/containers'

for filename in os.listdir(path):
    container_ids = {}
    tree = etree.parse(join(path,filename))
    components = tree.xpath("//*[starts-with(local-name(), 'c0')]")
    for r in components:
        containers = r.xpath('./did/container')
        if len(containers) > 1:
            parent = containers[0]
            child = containers[1]
            parent_type_num = parent.attrib['type'] + parent.text
            if parent_type_num not in container_ids:
                container_ids[parent_type_num] = str(uuid.uuid4())
                parent.attrib['id'] = container_ids[parent_type_num]
            else:
                parent.attrib['id'] = container_ids[parent_type_num]
            child.attrib['parent'] = container_ids[parent_type_num]
        elif len(containers) == 1:
            container_type_num = containers[0].attrib['type'] + containers[0].text
            if container_type_num not in container_ids:
                container_ids[container_type_num] = str(uuid.uuid4())
                containers[0].attrib['id'] = container_ids[container_type_num]
            else:
                containers[0].attrib['id'] = container_ids[container_type_num]
    fout = open('C:/Users/Public/Documents/containers/unique_' + filename, 'w')
    fout.write(etree.tostring(tree))
    fout.close()
