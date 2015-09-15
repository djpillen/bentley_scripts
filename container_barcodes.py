from lxml import etree
import os
from os.path import join
import uuid
import re

path = 'C:/Users/djpillen/GitHub/test_dir'

for filename in os.listdir(path):
    print filename
    container_ids = {}
    tree = etree.parse(join(path,filename))
    components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
    for r in components:
        containers = r.xpath('./did/container')
        for c in containers:
            if 'type' in c.attrib:
                container_type_num = c.attrib['type'] + c.text
                if container_type_num not in container_ids:
                    container_ids[container_type_num] = str(uuid.uuid4())

    for container_type_num in container_ids:
        container_ids[container_type_num] = re.sub(r'[A-Za-z\-]','',container_ids[container_type_num])

    containers = tree.xpath('//did/container')
    for c in containers:
        if 'type' in c.attrib:
            container_type_num = c.attrib['type'] + c.text
            if container_type_num in container_ids:
                c.attrib['label'] = c.attrib['label'] + ' ['+str(container_ids[container_type_num])+']'

    fout = open(join(path,filename), 'w')
    fout.write(etree.tostring(tree))
    fout.close()
