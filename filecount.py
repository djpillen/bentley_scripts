import lxml
from lxml import etree
import os
from os.path import join
import nltk
from collections import defaultdict


path = 'Real_Masters_all'

callnumbers = {}
filecount = 0

for filename in os.listdir(path):
    filecount += 1

eachfile = 0
for filename in os.listdir(path):
    eachfile += 1
    tree = etree.parse(join(path, filename))
    callnumber = tree.xpath('//archdesc/did/unitid')
    for r in callnumber:
        print '\rChecking call numbers in file number ' + str(eachfile) + ' of ' + str(filecount) + ': ' + filename,
        callno = r.text.encode('utf-8')
        callnumbers.setdefault(callno, []).append(filename)
        
print '\nChecking for duplicate call numbers...'


for callno in callnumbers:
    if len(callnumbers[callno]) > 1:
        print callno + ': ' + str(callnumbers[callno])

        
'''
dupes = set([x for x in callnumbers if callnumbers.count(x) > 1])

print '\nYou have ' + str(len(dupes)) + ' duplicate call numbers'

for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    callnumber = tree.xpath('//archdesc/did/unitid')
    for cn in callnumber:
        if cn.text in dupes:
            print filename + ' has duplicate call number ' + cn.text
'''