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
		publishers[statement] = []
	publishers[statement].append(filename)

for publisher in publishers:
	file_count = len(publishers[publisher])
	files = publishers[publisher]
	print publisher, file_count