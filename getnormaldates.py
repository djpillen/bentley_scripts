import lxml
from lxml import etree
import os
from os.path import join
import re
import csv

path = 'C:\Users\BHL Admin\Desktop\EADs\Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    d = tree.xpath('//unitdate')
    for i in d:
        yyyy = re.compile('^[\d]{4}s?$')
        yyyy_yyyy = re.compile('^[\d]{4}s?[-][\d]{4}s?$')
        undated = re.compile('^[Uu]ndated$')
        if yyyy.match(i.text) or yyyy_yyyy.match(i.text) or undated.match(i.text):
            with open('C:/Users/BHL Admin/Desktop/EADs/normaldates.csv', 'ab') as csvfile:
                writer = csv.writer(csvfile, dialect='excel')
                writer.writerow([filename, i.text])
    print filename
           