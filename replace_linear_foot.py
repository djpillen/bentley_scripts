from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	extents = tree.xpath('//extent')
	for extent in extents:
		if extent.text:
			extent_text = extent.text.strip().encode('utf-8')
			if 'linear foot' in extent_text:
				extent.text = extent_text.replace('linear foot','linear feet')
	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))