import csv
import lxml
from lxml import etree
import os
from os.path import join

path = 'Real_Masters_all_2'
date_dict = {}

'''
with open('not_dates-future.csv', 'rb') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        filename = row[0]
        print filename
        xpath = row[1]        
        file = open(join(path, filename))
        tree = etree.parse(file)
        date = tree.xpath(xpath)
        date_content = date[0].text
        date_string = etree.tostring(date[0])
        with open('not_dates-future_to_replace.csv', 'ab') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow([filename, xpath, date_string, date_content])
'''
            
with open('not_dates-future_to_replace-tail_removed.csv', 'rb') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        filename = row[0]
        print filename
        if filename not in date_dict:
            date_dict[filename] = {}
        date_string = row[3]
        date_content = row[4]
        if date_string not in date_dict[filename]:
            date_dict[filename][date_string] = date_content


for k, v in date_dict.iteritems():
    print k
    print date_dict[k]
    for v in date_dict[k]:
        EAD = open(join(path, k))
        EADread = EAD.read()
        NewEAD = open(join(path, k), 'w')
        NewEAD.write(EADread.replace(v, date_dict[k][v]))
        NewEAD.close()
        print v
        print date_dict[k][v]
    print '\n\n\n'
