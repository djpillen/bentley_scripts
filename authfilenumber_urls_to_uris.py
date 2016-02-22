from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	for subject in tree.xpath('//controlaccess/*'):
		if 'authfilenumber' in subject.attrib:
			if subject.attrib['authfilenumber'].endswith('.html'):
				subject.attrib['authfilenumber'] = subject.attrib['authfilenumber'].replace('.html','')
	with open(join(path,filename),'w') as f:
		f.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))