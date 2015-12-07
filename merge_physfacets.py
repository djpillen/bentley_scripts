from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	physdescs = tree.xpath('//physdesc')
	for physdesc in physdescs:
		physfacets = physdesc.xpath('./physfacet')
		if len(physfacets) > 1:
			first = physfacets[0]
			second = physfacets[1]
			first.text = first.text + '; ' + second.text
			physdesc.remove(second)
	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
	print filename
