from lxml import etree
import os
from os.path import join
import csv

type_label_csv = 'C:/Users/Public/Documents/container_type_label.csv'
path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

container_types = []
container_labels = []
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
                if container_type not in container_types:
                    container_types.append(container_type)
            if 'label' in container.attrib:
                container_label = container.attrib['label']
                if container_label not in container_labels:
                    container_labels.append(container_label)
        if len(containers) > 1:
            if 'type' in containers[1].attrib and 'label' in containers[1].attrib:
                container_type = containers[1].attrib['type']
                container_label = containers[1].attrib['label']
                if container_type not in subcontainer_type_label:
                    subcontainer_type_label[container_type] = []
                if container_label not in subcontainer_type_label[container_type]:
                    subcontainer_type_label[container_type].append(container_label)

print 'Container Types'
print container_types
print 'Container Labels'
print container_labels
print "Type label dictionary"
with open(type_label_csv,'ab') as csvfile:
    writer = csv.writer(csvfile)
    for k in subcontainer_type_label:
        row = []
        row.append(k)
        for v in subcontainer_type_label[k]:
            row.append(v)
        writer.writerow(row)
