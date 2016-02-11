from lxml import etree
import os
from os.path import join
import uuid
import re

path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

# EADs for which box numbering restarts with each subgroup
subgrp_filenames = ['kelseymu.xml']

# Alumni Association EADs. Several of the same containers show up in both EADs.
alumni_filenames = ['alumasso.xml','alumphot.xml']
alumni_barcodes = {}

av_boxes = {}
dvd_boxes = {}
cd_boxes = {}

# The same AV boxes and DVD boxes may appear in multiple collections -- they should all have the same barcode
for filename in os.listdir(path):
    print "Checking for AV Boxes in {0}".format(filename)
    tree = etree.parse(join(path,filename))
    containers = tree.xpath('//container')
    for container in containers:
        if 'type' in container.attrib:
            if container.attrib['type'] == 'avbox':
                if container.text not in av_boxes:
                    av_boxes[container.text] = re.sub(r'[A-Za-z\-]','',str(uuid.uuid4()))
            if container.attrib['label'] == 'DVD Box':
                if container.text not in dvd_boxes:
                    dvd_boxes[container.text] = re.sub(r'[A-Za-z\-]','',str(uuid.uuid4()))
            if container.attrib['label'] == 'CD Box':
                if container.text not in cd_boxes:
                    cd_boxes[container.text] = re.sub(r'[A-Za-z\-]','',str(uuid.uuid4()))

for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path,filename))
    if filename not in subgrp_filenames and filename not in alumni_filenames:
        container_ids = {}
        components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
        for component in components:
            c_containers = component.xpath('./did/container')
            if c_containers:
                container = c_containers[0]
                if 'type' in container.attrib and container.text:
                    container_type_label_num = container.attrib['type'] + container.attrib['label'] + container.text
                    if container_type_label_num not in container_ids:
                        if container.attrib['type'] == 'avbox':
                            container_ids[container_type_label_num] = av_boxes[container.text]
                        elif container.attrib['label'] == 'DVD Box':
                            container_ids[container_type_label_num] = dvd_boxes[container.text]
                        elif container.attrib['label'] == 'CD Box':
                            container_ids[container_type_label_num] = cd_boxes[container.text]
                        elif container_type_label_num not in container_ids:
                            container_ids[container_type_label_num] = re.sub(r'[A-Za-z\-]','',str(uuid.uuid4()))


        containers = tree.xpath('//did/container')
        for container in containers:
            if 'type' in container.attrib and container.text:
                container_type_label_num = container.attrib['type'] + container.attrib['label'] + container.text
                if container_type_label_num in container_ids:
                    container.attrib['label'] = container.attrib['label'] + ' ['+str(container_ids[container_type_label_num])+']'
    elif filename in subgrp_filenames:
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
                            container_ids[container_type_label_num] = re.sub(r'[A-Za-z\-]','',str(uuid.uuid4()))

            containers = subgrp.xpath('.//did/container')
            for container in containers:
                if 'type' in container.attrib:
                    container_type_label_num = container.attrib['type'] + container.attrib['label'] + container.text
                    if container_type_label_num in container_ids:
                        container.attrib['label'] = container.attrib['label'] + ' ['+str(container_ids[container_type_label_num])+']'
    elif filename in alumni_filenames:
        container_ids = {}
        components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
        for component in components:
            c_containers = component.xpath('./did/container')
            if c_containers:
                container = c_containers[0]
                if 'type' in container.attrib:
                    container_type_label_num = container.attrib['type'] + container.attrib['label'] + container.text
                    if container_type_label_num not in alumni_barcodes:
                        alumni_barcodes[container_type_label_num] = re.sub(r'[A-Za-z\-]','',str(uuid.uuid4()))
        containers = tree.xpath('//did/container')
        for container in containers:
            if 'type' in container.attrib:
                container_type_label_num = container.attrib['type'] + container.attrib['label'] + container.text
                if container_type_label_num in alumni_barcodes:
                    container.attrib['label'] = container.attrib['label'] + ' ['+str(alumni_barcodes[container_type_label_num])+']'

    with open(join(path,filename),'w') as eadout:
        eadout.write(etree.tostring(tree,xml_declaration=True,encoding="utf-8",pretty_print=True))
