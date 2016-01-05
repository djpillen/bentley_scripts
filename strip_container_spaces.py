from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	containers = tree.xpath('//container')
	for container in containers:
		container.text = container.text.strip()
	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))