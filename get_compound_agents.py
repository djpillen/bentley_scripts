from lxml import etree
import csv
import os
from os.path import join

tags = ['persname','corpname','famname']

output = 'C:/Users/djpillen/GitHub/test_run/subjects/compound_agents_20151116.csv'

path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

uniques = []

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None:
            if '---' in sub.text:
                modified = sub.text.replace('---','- --')
                if modified not in uniques:
                    uniques.append(modified)
            elif '--' in sub.text:
                if sub.text not in uniques:
                    uniques.append(sub.text)
    print filename

for unique in uniques:
    print unique
    row = []
    row.append(unique)
    terms = unique.split('--')
    for term in terms:
        row.append(term)
    with open(output, 'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)
