import re
import os
from os.path import join
from lxml import etree

text = re.compile(r'\w')

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    titles = tree.xpath('//unittitle')
    for title in titles:
            dates = title.xpath('./unitdate')
            if dates:
                    for date in dates:
                            if date.tail and text.search(date.tail):
                                print etree.tostring(title)
