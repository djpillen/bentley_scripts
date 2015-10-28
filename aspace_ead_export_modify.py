from lxml import etree
import os
from os.path import join
import re
import pickle

ns = {'ead':'urn:isbn:1-931666-22-9'}

originals = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
new = 'C:/Users/Public/Documents/aspace_migration/dlxs_eads/new'

container_types_file = 'C:/Users/Public/Documents/aspace_migration/container_types.p'


if not os.path.exists(container_types_file):
    label_type = {}
    print 'Building dictionary'
    for filename in os.listdir(originals):
        tree = etree.parse(join(originals,filename))
        containers = tree.xpath('//did/container')
        for container in containers:
            if 'label' in container.attrib and 'type' in container.attrib:
                c_label = container.attrib['label'].lower()
                c_type = container.attrib['type']
                if c_label not in label_type:
                    label_type[c_label] = c_type

    file_out = open(container_types_file,'wb')
    pickle.dump(label_type,file_out)
    file_out.close()
else:
    label_type = pickle.load(open(container_types_file,'rb'))

for filename in os.listdir(new):
    print 'Replacing types in {0}'.format(filename)
    tree = etree.parse(join(new,filename))
    containers = tree.xpath('//did/container')
    for container in containers:
        if 'label' in container.attrib:
            label = container.attrib['label'].lower()
            label = re.sub(r'\[\d+\]','',label)
            label = label.strip()
            container.attrib['label'] = label
            container.attrib['type'] = label_type[label]
    with open(join(new,filename),'w') as ead_out:
        ead_out.write(etree.tostring(tree,encoding="utf-8", xml_declaration=True, pretty_print=True))
