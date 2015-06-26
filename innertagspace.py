from lxml import etree
import os
from os.path import join
import re

path = 'news_and_info/new_eads'
outFilePath = 'news_and_info/new_eads_1'
for filename in os.listdir(path):
    start = open(join(path, filename), 'r')
    finish = open(join(outFilePath, filename), 'w')
    for i in start:
        innertag = re.sub('((?<=.)(?<!\s)(?<!\>))\<(?=\w)', ' <', i)
        innerand = re.sub('(?<=\>)and',' and', innertag)
        newdoc = innerand
        finish.write(newdoc)
    print filename
start.close()
finish.close()
