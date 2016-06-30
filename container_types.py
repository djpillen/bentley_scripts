from vandura.config import real_masters_all 

from lxml import etree
import os
from os.path import join
import csv

type_label_csv = 'C:/Users/Public/Documents/container_type_label.csv'
path = real_masters_all

container_types = {}
container_labels = {}
subcontainer_type_label = {}

for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path,filename))
    components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
    for component in components:
        containers = component.xpath('./did/container')
        for container in containers:
            if 'type' in container.attrib:
                container_type = container.attrib['type']
                container_types[container_type] = container_types.get(container_type,0) + 1
            if 'label' in container.attrib:
                container_label = container.attrib['label']
                container_labels[container_label] = container_labels.get(container_label,0) + 1
        if len(containers) > 1:
            if 'type' in containers[1].attrib and 'label' in containers[1].attrib:
                container_type = containers[1].attrib['type']
                container_label = containers[1].attrib['label']
                if container_type not in subcontainer_type_label:
                    subcontainer_type_label[container_type] = []
                if container_label not in subcontainer_type_label[container_type]:
                    subcontainer_type_label[container_type].append(container_label)

print 'Container Types'
sorted_types = sorted(container_types, key=container_types.get, reverse=True)
for c_type in sorted_types:
    print "{0} - {1}".format(c_type, container_types[c_type])
print 'Container Labels'
sorted_labels = sorted(container_labels, key=container_labels.get, reverse=True)
for c_label in sorted_labels:
    print "{0} - {1}".format(c_label, container_labels[c_label])
"""
with open(type_label_csv,'ab') as csvfile:
    writer = csv.writer(csvfile)
    for k in subcontainer_type_label:
        row = []
        row.append(k)
        for v in subcontainer_type_label[k]:
            row.append(v)
        writer.writerow(row)
"""
