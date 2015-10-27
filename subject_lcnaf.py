from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

tags = ['genreform']

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    controlaccesses = tree.xpath('//controlaccess')
    for controlaccess in controlaccesses:
        for subject in controlaccess.xpath('./*'):
            if subject.tag in tags:
                if subject.attrib['source'] == 'lcnaf':
                    print filename, subject.tag, subject.text.encode('utf-8')
