from lxml import etree
import os
from os.path import join

path = 'test'




for filename in os.listdir(path):
    to_replace = {}
    tree = etree.parse(join(path, filename))
    not_dates = tree.xpath('/ead/archdesc/dsc/c01[2]/c02[2]/c03[2]/c04[12]/did/unittitle/unitdate')
    for not_date in not_dates:
        not_date_tail = not_date.tail
        not_date_string = etree.tostring(not_date).replace(not_date_tail, '')
        content = not_date.text
        to_replace[not_date_string] = content
        unittitle = not_date.getparent()
        unittitle_string = etree.tostring(unittitle)
        #print unittitle_string
        #print not_date_string
        #print unittitle_string.replace(not_date_string, content)
        for k, v in to_replace.iteritems():
            print "Replace: " + k
            print "With: " + v
