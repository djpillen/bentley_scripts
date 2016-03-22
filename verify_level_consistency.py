from lxml import etree
import os
from os.path import join
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
inconsistency_csv = 'C:/Users/Public/Documents/component_level_inconsistency.csv'

data = []
for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		subcomponents = component.xpath("./*[starts-with(local-name(), 'c0')]")
		subcomponent_levels = {}
		subcomponent_tags = {}
		for subcomponent in subcomponents:
			subcomponent_level = subcomponent.attrib["level"]
			subcomponent_tag = subcomponent.tag
			subcomponent_levels[subcomponent_level] = subcomponent_levels.get(subcomponent_level, 0) + 1
			subcomponent_tags[subcomponent_tag] = subcomponent_tags.get(subcomponent_tag, 0) + 1
		if len(subcomponent_levels) > 1:
			data.append([filename, tree.getpath(component),subcomponent_levels])
			print filename, tree.getpath(component), subcomponent_levels
		if len(subcomponent_tags) > 1:
			data.append([filename, tree.getpath(component), subcomponent_tags])
			print filename, tree.getpath(component), subcomponent_tags

with open(inconsistency_csv,'wb') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(data)