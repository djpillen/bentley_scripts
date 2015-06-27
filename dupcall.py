from lxml import etree
import os
from os.path import join


path = 'Real_Masters_all'

callnumbers = []
filecount = 0

print 'counting files...'

for filename in os.listdir(path):
    filecount += 1

print filecount

eachfile = 0
for filename in os.listdir(path):
    eachfile += 1
    tree = etree.parse(join(path, filename))
    callnumber = tree.xpath('//archdesc/did/unitid')
    for r in callnumber:
        print 'checking call numbers in ' + str(eachfile) + ' of ' + str(filecount)
        callno = r.text.encode('utf-8')
        callnumbers.append(callno)

dupes = set([x for x in callnumbers if callnumbers.count(x) > 1])

for r in dupes:
    for filename in os.listdir(path):
        tree = etree.parse(join(path, filename))
        callnumber = tree.xpath('//archdesc/did/unitid')
        for cn in callnumber:
            if cn.text == r:
                print filename + ' ' + cn.text

print dupes
