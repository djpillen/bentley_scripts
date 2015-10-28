from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

only_processinfo = []
only_dao = []

for filename in os.listdir(path):
    print filename
    has_processinfo = False
    has_dao = False
    tree = etree.parse(join(path,filename))
    processinfo = tree.xpath('//processinfo')
    dao = tree.xpath('//dao')
    for process in processinfo:
        if process.xpath('.//extptr'):
            href = process.xpath('.//extptr')[0].attrib['href']
            if href == 'digitalproc':
                has_processinfo = True
    if dao:
        has_dao = True
    if has_processinfo and not has_dao:
        only_processinfo.append(filename)
    if has_dao and not has_processinfo:
        only_dao.append(filename)

print 'Only processinfo:',only_processinfo
print 'Only dao:',only_dao
