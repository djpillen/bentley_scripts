from lxml import etree
import os
from os.path import join
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
inconsistency_csv = 'C:/Users/Public/Documents/component_level_inconsistency.csv'

data = []
for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	level_ones = tree.xpath('//dsc//c01')
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	level_one_levels = {}
	for level_one in level_ones:
		level_one_level = level_one.attrib["level"]
		level_one_levels[level_one_level] = level_one_levels.get(level_one_level, 0) + 1
	if len(level_one_levels) > 1:
		data.append([filename, "<c01>", level_one_levels])
		print filename, "<c01>", level_one_levels
	for component in components:
		subcomponents = component.xpath("./*[starts-with(local-name(), 'c0')]")
		subcomponent_levels = {}
		for subcomponent in subcomponents:
			subcomponent_level = subcomponent.attrib["level"]
			subcomponent_levels[subcomponent_level] = subcomponent_levels.get(subcomponent_level, 0) + 1
		if len(subcomponent_levels) > 1 and any("series" in level for level in subcomponent_levels):
			data.append([filename, tree.getpath(component),subcomponent_levels])
			print filename, tree.getpath(component), subcomponent_levels

with open(inconsistency_csv,'wb') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(data)