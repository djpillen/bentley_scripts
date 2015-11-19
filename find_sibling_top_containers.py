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
			container_0 = {'type':containers[0].attrib['type'],'label':containers[0].attrib['label'],'text':containers[0].text}
			container_1 = {'type':containers[1].attrib['type'],'label':containers[1].attrib['label'],'text':containers[1].text}
			if (container_0['type'] != container_1['type']) and (container_0['label'] != container_1['label']):
				print filename, container_0['type'],container_0['text'],container_1['text']