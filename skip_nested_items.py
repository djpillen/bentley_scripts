from lxml import etree
import os
from os.path import join

path = 'C:/Users/Public/vbox_shared'
outpath = 'C:/Users/Public/vbox_shared'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	items = tree.xpath('//item')
	for item in items:
		if 'skip' in item.attrib:
			del item.attrib['skip']
		subitems = item.xpath('.//item')
		for subitem in subitems:
			if 'altrender' not in subitem.attrib:
				subitem.attrib['altrender'] = 'skip'
	with open(join(outpath,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
	print filename