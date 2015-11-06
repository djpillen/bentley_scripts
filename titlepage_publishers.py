from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

publishers = {}

for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	publisher = tree.xpath('//titlepage/publisher')[0]
	statement = etree.tostring(publisher)
	if statement not in publishers:
		publishers[statement] = 0
	publishers[statement] += 1

for publisher in publishers:
	print publisher, publishers[publisher]