from lxml import etree
import csv
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

miscellaneous_csv = 'C:/Users/Public/Documents/miscellaneous_all.csv'
miscellaneous_series_csv = 'C:/Users/Public/Documents/miscellaneous_series.csv'
completely_miscellaneous_csv = 'C:/Users/Public/Documents/miscellaneous_full_title.csv'

potential_matches = ['miscellaneous','misc.']

for csvfile in [miscellaneous_csv, miscellaneous_series_csv, completely_miscellaneous_csv]:
	if os.path.exists(csvfile):
		os.remove(csvfile)

headers = ['Collection', 'Component Title', 'Level', 'Extent', 'Trail', 'XPath']

with open(miscellaneous_csv,'ab') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(headers)

with open(miscellaneous_series_csv,'ab') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(headers)

with open(completely_miscellaneous_csv,'ab') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerow(headers)

def calculate_physdesc_extents(physdescs):
	physdesc_extents = {}
	for physdesc in physdescs:
		extents = physdesc.xpath('./extent')
		if extents:
			extent = extents[0].text.strip()
			extent_number = extent.split()[0]
			extent_type = ' '.join(extent.split()[1:])
			if extent_type not in physdesc_extents:
				physdesc_extents[extent_type] = 0
			physdesc_extents[extent_type] += float(extent_number)
	return physdesc_extents

def calculate_subcomponent_extents(subcomponents):
	subcomponent_extents = {}
	for subcomponent in subcomponents:
		if not subcomponent.xpath(".//*[starts-with(local-name(), 'c0')]"):
			physdescs = subcomponent.xpath('./did/physdesc')
			physdesc_extents = {}
			if physdescs:
				physdesc_extents = calculate_physdesc_extents(physdescs)
			if physdesc_extents:
				for extent_type in physdesc_extents:
					if extent_type not in subcomponent_extents:
						subcomponent_extents[extent_type] = 0
					subcomponent_extents[extent_type] += physdesc_extents[extent_type]
			else:
				if 'folders' not in subcomponent_extents:
					subcomponent_extents['folders'] = 0
				subcomponent_extents['folders'] += 1
	return subcomponent_extents


miscellaneous_titles = []
miscellaneous_series = []
completely_miscellaneous = []
for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	collection_title = re.sub(r'<(.*?)>','',etree.tostring(tree.xpath('//archdesc/did/unittitle')[0])).strip().encode('utf-8')
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		unittitle = component.xpath('./did/unittitle')[0]
		component_title = re.sub(r'<(.*?)>','',etree.tostring(unittitle)).strip().encode('utf-8')
		if 'misc.' in component_title.lower() or 'miscellaneous' in component_title.lower():
			component_path = tree.getpath(component)
			level = component.attrib['level']
			if level == 'otherlevel':
				level = component.attrib['otherlevel']
			physdescs = component.xpath('./did/physdesc')
			subcomponents = component.xpath(".//*[starts-with(local-name(), 'c0')]")
			component_extents = {}
			if physdescs:
				physdesc_extents = calculate_physdesc_extents(physdescs)
				if physdesc_extents:
					for extent_type in physdesc_extents:
						if extent_type not in component_extents:
							component_extents[extent_type] = 0
						component_extents[extent_type] += physdesc_extents[extent_type]
				elif subcomponents:
					subcomponent_extents = calculate_subcomponent_extents(subcomponents)
					for extent_type in subcomponent_extents:
						if extent_type not in component_extents:
							component_extents[extent_type] = 0
						component_extents[extent_type] += subcomponent_extents[extent_type]
				else:
					if 'folders' not in component_extents:
						component_extents['folders'] = 0
					component_extents['folders'] += 1
			else:
				if subcomponents:
					subcomponent_extents = calculate_subcomponent_extents(subcomponents)
					for extent_type in subcomponent_extents:
						if extent_type not in component_extents:
							component_extents[extent_type] = 0
						component_extents[extent_type] += subcomponent_extents[extent_type]
				else:
					if 'folders' not in component_extents:
						component_extents['folders'] = 0
					component_extents['folders'] += 1
			component_extent_statements = ["{0} {1}".format(component_extents[extent_type],extent_type) for extent_type in component_extents]
			component_extent = '; '.join(component_extent_statements)

			component_parent = component.getparent()
			parent_titles = []
			while component_parent.tag.startswith('c0'):
				component_parent_title = re.sub(r'<(.*?)>','',etree.tostring(component_parent.xpath('./did/unittitle')[0])).strip().encode('utf-8')
				parent_titles.append(component_parent_title)
				component_parent = component_parent.getparent()
			parent_titles.reverse()
			parent_titles.append(component_title)
			trail = ' --> '.join(parent_titles)

			miscellaneous_titles.append([collection_title, component_title, level, component_extent, trail, component_path])

			if 'series' in level:
				miscellaneous_series.append([collection_title, component_title, level, component_extent, trail, component_path])

			if component_title.lower() == 'misc.' or component_title.lower() == 'miscellaneous':
				completely_miscellaneous.append([collection_title, component_title, level, component_extent, trail, component_path])

with open(miscellaneous_csv,'ab') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(miscellaneous_titles)

with open(miscellaneous_series_csv,'ab') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(miscellaneous_series)

with open(completely_miscellaneous_csv,'ab') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(completely_miscellaneous)
		