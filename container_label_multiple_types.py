from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

suspect = {'Folder':'box','Box':'reel','Oversize Folder':'box','Oversize Volume':'box'}

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    containers = tree.xpath('//did/container')
    for container in containers:
        if 'label' in container.attrib and 'type' in container.attrib:
            label = container.attrib['label']
            container_type = container.attrib['type']
            if label in suspect:
                if suspect[label] == container_type:
                    print filename, tree.getpath(container)
