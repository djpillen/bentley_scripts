from lxml import etree
import os
from os.path import join
import uuid
import re

path = 'C:/Users/Public/Documents/aspace_migration/test_eads'

special_cases = ['kelseymu.xml']

for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path,filename))
    if filename not in special_cases:
        container_ids = {}
        components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
        for component in components:
            c_containers = component.xpath('./did/container')
            if c_containers:
                container = c_containers[0]
                if 'type' in container.attrib:
                    container_type_label_num = container.attrib['type'] + container.attrib['label'] + container.text
                    if container_type_label_num not in container_ids:
                        container_ids[container_type_label_num] = str(uuid.uuid4())

        for container_type_label_num in container_ids:
            container_ids[container_type_label_num] = re.sub(r'[A-Za-z\-]','',container_ids[container_type_label_num])

        containers = tree.xpath('//did/container')
        for container in containers:
            if 'type' in container.attrib:
                container_type_label_num = container.attrib['type'] + container.attrib['label'] + container.text
                if container_type_label_num in container_ids:
                    container.attrib['label'] = container.attrib['label'] + ' ['+str(container_ids[container_type_label_num])+']'
    else:
        subgrps = tree.xpath('//c01')
        for subgrp in subgrps:
            container_ids = {}
            sub_components = subgrp.xpath(".//*[starts-with(local-name(), 'c0')]")
            for sub_component in sub_components:
                c_containers = sub_component.xpath('./did/container')
                if c_containers:
                    container = c_containers[0]
                    if 'type' in container.attrib:
                        container_type_label_num = container.attrib['type'] + container.attrib['label'] + container.text
                        if container_type_label_num not in container_ids:
                            container_ids[container_type_label_num] = str(uuid.uuid4())

            for container_type_label_num in container_ids:
                container_ids[container_type_label_num] = re.sub(r'[A-Za-z\-]','',container_ids[container_type_label_num])

            containers = subgrp.xpath('.//did/container')
            for container in containers:
                if 'type' in container.attrib:
                    container_type_label_num = container.attrib['type'] + container.attrib['label'] + container.text
                    if container_type_label_num in container_ids:
                        container.attrib['label'] = container.attrib['label'] + ' ['+str(container_ids[container_type_label_num])+']'

    with open(join(path,filename),'w') as eadout:
        eadout.write(etree.tostring(tree,xml_declaration=True,encoding="utf-8"))
