from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
outFilePath = 'C:/Users/Public/Documents/aspace_migration/test_eads'
for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	daos = tree.xpath('//dao')
	for dao in daos:
		if dao.attrib['actuate'] == 'onrequest':
			dao.attrib['actuate'] = 'onRequest'
		elif dao.attrib['actuate'] == 'onload':
			dao.attrib['actuate'] = 'onLoad'
	with open(join(outFilePath,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
    print filename
