from lxml import etree
import os
from os.path import join
import re

vandura = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
trial = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

for path in [vandura]:
	for filename in os.listdir(path):
		tree = etree.parse(join(path,filename))
		extents = tree.xpath('//extent')
		for extent in extents:
			if extent.text:
				extent_text = extent.text.strip().encode('utf-8')
				if extent_text.startswith('(') and extent_text.endswith(')'):
					extent_text = re.sub(r'^\(|\)$','',extent_text)
					extent.text = extent_text
		with open(join(path,filename),'w') as ead_out:
			ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
		print path, filename