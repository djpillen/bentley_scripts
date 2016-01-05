from lxml import etree
import os
from os.path import join
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

dashes_file = 'C:/Users/Public/Documents/containers_with_dashes.csv'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		containers = component.xpath('./did/container')
		if containers:
			container = containers[0]
			if '-' in container.text:
				container_text = container.attrib['label'] + ' ' + container.text
				with open(dashes_file,'ab') as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow([filename, container_text])
				print filename, container_text