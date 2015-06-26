import lxml
from lxml import etree
import csv
import re
import os
from os.path import join

path = 'Real_Masters_all'

with open('accessrestrict_expired_fulltext.csv','rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        filename = row[0]
        date_path = row[1]
        component_path = re.sub('\/accessrestrict\/p\/date','',date_path)
        component_path = component_path
        tree = etree.parse(join(path,filename))
        for r in tree.xpath(component_path):
            container = r.xpath('.//container')
            box_number = container[0].text
            print filename
            print date_path
            print box_number