from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		unittitle = component.xpath('./did/unittitle')[0]
		title = etree.tostring(unittitle).strip()
		physdescs = component.xpath('./did/physdesc')
		if len(physdescs) > 1:
			extent = False
			and_not = False
			for physdesc in physdescs:
				if physdesc.xpath('./extent'):
					extent = True
				if not physdesc.xpath('./extent'):
					and_not = True
			if extent and and_not:
				print filename, tree.getpath(component)