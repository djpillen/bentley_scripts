from lxml import etree
import os
from os.path import join

# Find boxes that have both restricted and unrestricted content



path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
	boxes = {}
	tree = etree.parse(join(path,filename))
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		containers = component.xpath('./did/container')
		if containers:
			container = containers[0]
			c_type = container.attrib['type']
			c_label = container.attrib['label']
			indicator = container.text
			box = c_type + c_label + indicator
			if box not in boxes:
				boxes[box] = []
			if component.xpath('./did/accessrestrict') and 'restricted' not in boxes[box]:
				boxes[box].append('restricted')
			elif 'open' not in boxes[box]:
				boxes[box].append('open')

	for box in boxes:
		if len(boxes[box]) == 1:
			print filename, box
