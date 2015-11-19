from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		did = component.xpath('./did')[0]
		unittitle = component.xpath('./did/unittitle')
		unitdates = component.xpath('./did/unitdate')
		if not unittitle:
			wrapper = etree.Element('unittitle')
			wrapper.append(unitdates[0])
			did.append(wrapper)
			print filename, tree.getpath(component), len(unitdates)
	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))