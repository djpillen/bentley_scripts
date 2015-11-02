from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

amp_count = 0

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    unittitles = tree.xpath('//unittitle')
    for unittitle in unittitles:
        unittitle_string = etree.tostring(unittitle)
        if '&amp;' in unittitle_string:
            print unittitle_string
            amp_count += 1

print 'Total:',amp_count
