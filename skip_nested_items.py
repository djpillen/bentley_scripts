from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/test_run/ead'
outpath = 'C:/Users/djpillen/GitHub/test_run/ead'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	items = tree.xpath('//item')
	lists = tree.xpath('//list')
	for top_list in lists:
		if len(re.findall('list', tree.getpath(top_list))) == 1:
			sublists = top_list.xpath('.//list')
			for sublist in sublists:
				sublist.tag = 'sublist'
	for item in items:
		subitems = item.xpath('.//item')
		for subitem in subitems:
			subitem.tag = 'subitem'
			if 'altrender' in subitem.attrib:
				del subitem.attrib['altrender']
	with open(join(outpath,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
	print filename