from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

types = []
first_level_admin = []
first_level_add = []
huh = {'list':[]}

# check to make sure that descgrp/descgrp is always followed by odd or index

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    descgrps = tree.xpath('//descgrp')
    for descgrp in descgrps:
        if 'type' in descgrp.attrib:
            if descgrp.attrib['type'] not in types:
                types.append(descgrp.attrib['type'])
            if descgrp.attrib['type'] == 'admin':
                for elem in descgrp.xpath('./*'):
                    if elem.tag not in first_level_admin:
                        first_level_admin.append(elem.tag)
            if descgrp.attrib['type'] == 'add':
                for elem in descgrp.xpath('./*'):
                    if elem.tag not in first_level_add:
                        first_level_add.append(elem.tag)

                    if elem.tag in huh:
                        if filename not in huh[elem.tag]:
                            huh[elem.tag].append(filename)
                            '''
                        for subelem in elem.xpath('./*'):
                            if subelem.tag not in ['odd','index','relatedmaterial']:
                                print filename, subelem.tag
                                '''
                    if elem.tag == 'otherfindaid':
                        print 'otherfindaid:',filename

print types
print 'ADMIN',first_level_admin
print '\n\n\n'
print 'ADD',first_level_add
print '\n\n\n'

for tag in first_level_admin:
    if tag in first_level_add:
        print 'Shows up in both:',tag
for tag in first_level_add:
    if tag in first_level_admin:
        print 'Shows up in both:',tag
print '\n\n\n'
for tag in huh:
    print tag, huh[tag]
