from lxml import etree
import re
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

dupe_count = 0
for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    odds = tree.xpath('//odd')
    for odd in odds:
        note = odd.xpath('./p')
        if note:
            note_text = note[0].text
            component = odd.getparent()
            containers = component.xpath('./did/container')
            for container in containers:
                c_type = container.attrib['type']
                label = container.attrib['label']
                number = container.text
                cont_type = re.compile(c_type)
                cont_number = re.compile('\s' + number + '\)?$')
                cont_label = re.compile(label)
                if label and number:
                    if cont_number.search(note_text) and (cont_label.search(note_text) or cont_type.search(note_text)):
                        print filename, label, number, note_text.encode('utf-8')
                        dupe_count += 1

print dupe_count
