from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

sources = []
suspect = ['local','lcnaf']

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	controlaccesses = tree.xpath('//controlaccess')
	for controlaccess in controlaccesses:
		if controlaccess.xpath('./title'):
			for title in controlaccess.xpath('./title'):
				if title.attrib['source'] in suspect:
					print filename, title.attrib['source'],title.text


'''
					title.attrib['source'] = 'aacr2'
	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
	print filename
'''