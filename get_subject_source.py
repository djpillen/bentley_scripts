from lxml import etree
import os
from os.path import join
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'



sources = {'subject':{},'geogname':{},'genreform':{}}
tags = ['subject','geogname','genreform']


for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path,filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            if sub.text not in sources[sub.tag]:
                sources[sub.tag][sub.text] = []
            if sub.attrib['source'] not in sources[sub.tag][sub.text]:
                sources[sub.tag][sub.text].append(sub.attrib['source'])


for sub_type in sources:
    for subject in sources[sub_type]:
        if len(sources[sub_type][subject]) > 1:
            print sub_type, subject, sources[sub_type][subject]
