from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		containers = component.xpath('./did/container')
		if len(containers) > 1:
			subcontainer = containers[1]
			con_type = subcontainer.attrib['type']
			con_label = subcontainer.attrib['label']
			if con_type != 'othertype':
				subcontainer.attrib['type'] = con_type.title()
	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
	print filename