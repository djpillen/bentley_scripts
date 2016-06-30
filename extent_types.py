from lxml import etree
import os
from os.path import join
import re
import csv

from vandura.config import real_masters_all

extent_types = {}

for filename in os.listdir(real_masters_all):
	print filename
	tree = etree.parse(join(real_masters_all,filename))
	physdescs = tree.xpath('//physdesc')
	for physdesc in physdescs:
		extents = physdesc.xpath('./extent')
		if extents:
			extent = extents[0]
			try:
				extent_type = re.findall(r'[\d\+]+\s(.+)', extent.text)[0]
			except:
				print tree.getpath(extent)
				quit()
			extent_types[extent_type] = extent_types.get(extent_type, 0) + 1

sorted_types = sorted(extent_types, key=extent_types.get,reverse=True)

data = [[extent_type, extent_types[extent_type]] for extent_type in sorted_types]
with open('C:/Users/Public/Documents/extent_types.csv','wb') as csv_file:
	writer = csv.writer(csv_file)
	writer.writerows(data)
