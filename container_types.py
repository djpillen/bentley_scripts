from lxml import etree
import os
from os.path import join


path = 'Real_Masters_all'

container_types = []
container_labels = []

for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path,filename))
    container = tree.xpath('//container')
    for r in container:
        if 'type' in r.attrib:
            container_type = r.attrib['type']
            if container_type not in container_types:
                container_types.append(container_type)
        if 'label' in r.attrib:
            container_label = r.attrib['label']
            if container_label not in container_labels:
                container_labels.append(container_label)

print 'Container Types'
print container_types
print 'Container Labels'
print container_labels
