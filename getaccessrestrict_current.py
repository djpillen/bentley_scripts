import csv
import lxml
from lxml import etree
import os
from os.path import join


'''
with open(file, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        filename = row[0]
        print filename
        date_path = row[1]
        normal = row[2]
        tree = etree.parse(join(path,filename))
        date = tree.xpath(date_path)
        restriction = date[0].getparent()
        with open('accessrestrict_expired_fulltext.csv', 'ab') as csvout:
            writer = csv.writer(csvout, dialect='excel')
            writer.writerow([filename, date_path, normal, etree.tostring(restriction)])
        

'''

file = 'accessrestrictdate-7.csv'

current_dict = {}
current_count = 0
with open(file, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        filename = row[0]
        normal = row[3]
        if normal > '2015-07-02':
            if filename not in current_dict:
                current_dict[filename] = 1
            else:
                current_dict[filename] += 1
            current_count += 1
            
            
for filename in current_dict:
    print filename
    print current_dict[filename]
