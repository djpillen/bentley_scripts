from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	rewrite = False
	unitdates = tree.xpath('//unittitle/unitdate')
	for unitdate in unitdates:
		if "type" not in unitdate.attrib:
			rewrite = True
			unitdate.attrib["type"] = "inclusive"
	if rewrite:
		with open(join(path,filename),'w') as f:
			f.write(etree.tostring(tree, encoding="utf-8",xml_declaration=True, pretty_print=True))