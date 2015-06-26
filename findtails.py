from lxml import etree
import os
from os.path import join
import re

path = 'Real_Masters_all'
outFilePath = 'test-spaces'
tails = []
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    elems = tree.xpath('//*')
    spaces = re.compile('\s')
    dont_replace = re.compile('[\'\.\,\?\!\"\-\:\)\}\]\;\s]')
    for r in elems:
        if r.tail and not 'lb' in r.tag and not spaces.match(r.tail):
            print r.tag + ' ' + r.tail[0].encode('utf-8')
            if r.tail[0] not in tails:
                tails.append(r.tail[0])
            else:
                continue
            '''
            print filename + ' ' + tree.getpath(r) + ' ' + r.tag + ' ' + r.tail[0].encode('utf-8')
            if r.tail[0] not in tails:
                tails.append(r.tail[0])
            else:
                continue

        if not 'lb' in r.tag and r.tail and word_or_paren.match(r.tail) and not punctuation.match(r.tail):
            print filename + ' ' + tree.getpath(r)
            print filename + ' ' + r.tag + ' ' + r.tail.encode('utf-8')
            r.tail = ' ' + r.tail
            tails += 1
       '''
print tails