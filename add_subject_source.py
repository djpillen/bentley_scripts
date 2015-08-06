from lxml import etree
import os
from os.path import join
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

sources = {'subject':{},'geogname':{},'genreform':{}}
to_update = {'subject':[],'geogname':[],'genreform':[]}
tags = ['subject','geogname','genreform']

updateable = {'subject':{},'geogname':{},'genreform':{'Photographs.':'aat'}}

'''
for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            if 'source' in sub.attrib:
                if '--' in sub.text:
                    terms = sub.text.split('--')
                    first_term = terms[0]
                    if first_term not in sources[sub.tag]:
                        sources[sub.tag][first_term] = []
                        sources[sub.tag][first_term].append(sub.attrib['source'])
                    elif first_term in sources:
                        if sub.attrib['source'] not in sources[sub.tag][first_term]:
                            sources[sub.tag][first_term].append(sub.attrib['source'])
                else:
                    if sub.text.strip('.') not in sources[sub.tag]:
                        sources[sub.tag][sub.text.strip('.')] = []
                        sources[sub.tag][sub.text.strip('.')].append(sub.attrib['source'])
                    elif sub.text.strip('.') in sources[sub.tag]:
                        if sub.attrib['source'] not in sources[sub.tag][sub.text.strip('.')]:
                            sources[sub.tag][sub.text.strip('.')].append(sub.attrib['source'])

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            if not 'source' in sub.attrib:
                if '--' in sub.text:
                    terms = sub.text.split('--')
                    first_term = terms[0]
                    if first_term not in to_update[sub.tag]:
                        to_update[sub.tag].append(first_term)
                else:
                    if sub.text.strip('.') not in to_update[sub.tag]:
                        to_update[sub.tag].append(sub.text.strip('.'))
single = 0
multiple = 0
unknown = 0
for tag in to_update:
    for sub in to_update[tag]:
        if sub in sources[tag]:
            if len(sources[tag][sub]) == 1:
                single += 1
                updateable[tag][sub] = sources[tag][sub]

            elif len(sources[tag][sub]) > 1:
                multiple += 1
        else:
            unknown += 1
print 'Single:',single
print 'Multiple:',multiple
print 'Unknown:',unknown
'''

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None and not 'source' in sub.attrib:
            if sub.text in updateable[sub.tag]:
                sub.attrib['source'] = updateable[sub.tag][sub.text]
                print sub.tag, sub.text, sub.attrib['source']
                '''
            if '--' in sub.text:
                terms = sub.text.split('--')
                first_term = terms[0]
                if first_term in updateable[sub.tag]:
                    sub.attrib['source'] = updateable[sub.tag][first_term][0]
                    print filename
            else:
                if sub.text.strip('.') in updateable[sub.tag]:
                    sub.attrib['source'] = updateable[sub.tag][sub.text.strip('.')][0]
                    print filename
                    '''
    with open(join(path,filename),'w') as ead_out:
        ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True, pretty_print=True))
