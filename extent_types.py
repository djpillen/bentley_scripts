from lxml import etree
import os
from os.path import join
import re
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

extent_types = {}

for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	physdescs = tree.xpath('//physdesc')
	for physdesc in physdescs:
		extents = physdesc.xpath('./extent')
		if extents:
			extent = extents[0]
			extent_type = re.findall(r'[\d\+]+\s(.+)', extent.text)[0]
			if extent_type not in extent_types:
				extent_types[extent_type] = 0
			extent_types[extent_type] += 1

sorted_types = sorted(extent_types, key=extent_types.get,reverse=True)

with open('C:/Users/Public/Documents/extent_types.csv','ab') as csv_file:
	writer = csv.writer(csv_file)
	for extent_type in sorted_types:
		writer.writerow([extent_type,extent_types[extent_type]])
