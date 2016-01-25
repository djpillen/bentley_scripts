from lxml import etree
import os
from os.path import join
import csv
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

removable_media_csv = 'C:/Users/Public/Documents/removable_media.csv'

extent_types = ['optical disks','floppy disks','zip disks','USB thumb drives']
extent_physfacet_dict = {'optical disks':['DVD','CD'], 'floppy disks':['3.5"','5.25"']}
extent_container_summary_dict = {'images':['CD'],'digital files':['CD']}
physfacet_types = ['CD','DVD','optical cartridge','computer disk','removable cartridge','compact disc', '5.25" floppy disk','3.5" floppy disk','zip disk','optical disk']

master_list = ['optical','floppy','disc','disk','thumb drive','CD','DVD']

# Files that contain parent-level physdescs that should not be added to the removable_media_dict
skip_files = ['krebsmic.xml']

removable_media_count = {}
removable_media_files = {}

def characterize_removeable_media(component):
	physdescs = component.xpath('./did/physdesc')
	if physdescs:
		for physdesc in physdescs:
			extents = physdesc.xpath('./extent')
			physfacets = physdesc.xpath('./physfacet')
			if physfacets:
				physfacet_string = etree.tostring(physfacets[0])
				physfacet = re.sub(r'<genreform(.*?)>','',physfacet_string)
			else:
				physfacet = False
			if extents:
				extent = extents[0].text
				extent_numbers = re.findall(r'(\d+)', extent)
				if extent_numbers:
					extent_number = extent_numbers[0]
					extent_number = int(extent_number)
					extent_type = re.findall(r'[\d\+]+\s(.+)', extent)[0]
					if extent_type in extent_types:
						if extent_type in extent_physfacet_dict:
							physfacet_found = False
							if physfacet:
								for physfacet_type in extent_physfacet_dict[extent_type]:
									physfacet_lower = physfacet_type.lower()
									if physfacet_lower in physfacet.lower():
										if extent_type == 'floppy disks':
											extent_type = physfacet_type + ' ' + extent_type
										else:
											extent_type = physfacet_type
										physfacet_found = True
							if not physfacet_found:
								extent_type = extent_type + ' (type not specified)'
						if extent_type not in removable_media_count:
							removable_media_count[extent_type] = 0
							removable_media_files[extent_type] = []
						removable_media_count[extent_type] += extent_number
						if filename not in removable_media_files[extent_type]:
							removable_media_files[extent_type].append(filename)
					elif len(extents) == 2 and extent_type in extent_container_summary_dict:
						container_summary = extents[1].text
						for container_summary_type in extent_container_summary_dict[extent_type]:
							if container_summary_type in container_summary:
								extent_type = container_summary_type + 's (quantity not specified)'
								if extent_type not in removable_media_count:
									removable_media_count[extent_type] = 0
									removable_media_files[extent_type] = []
								removable_media_count[extent_type] += 1
								if filename not in removable_media_files[extent_type]:
									removable_media_files[extent_type].append(filename)
			elif physfacet:
				for physfacet_type in physfacet_types:
					physfacet_lower = physfacet_type.lower()
					if physfacet_lower in physfacet.lower():
						singular = True
						if physfacet_lower + 's' in physfacet.lower():
							singular = False
						if singular:
							if physfacet_type not in removable_media_count:
								removable_media_count[physfacet_type] = 0
								removable_media_files[physfacet_type] = []
							removable_media_count[physfacet_type] += 1
							if filename not in removable_media_files[physfacet_type]:
								removable_media_files[physfacet_type].append(filename)
						else:
							physfacet_type = physfacet_type + 's (quantity not specified)'
							if physfacet_type not in removable_media_count:
								removable_media_count[physfacet_type] = 0
								removable_media_files[physfacet_type] = []
							removable_media_count[physfacet_type] += 1
							if filename not in removable_media_files[physfacet_type]:
								removable_media_files[physfacet_type].append(filename)

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		children = component.xpath("./*[starts-with(local-name(), 'c0')]")
		if not children:
			characterize_removeable_media(component)
		else:
			child_extents = False
			for child in children:
				if child.xpath('./did/physdesc'):
					child_extents = True
			if not child_extents:
				characterize_removeable_media(component)
			else:
				# Outlier EAD that has a subseries physfacet of compact discs except where indicated
				if filename == 'rfwms.xml':
					for child in children:
						if child.xpath('./did/container'):
							add_one = True
							child_physdescs = child.xpath('./did/physdesc')
							if child_physdescs:
								child_physdesc_string = etree.tostring(child_physdescs[0])
								# If a child has a physdesc, it either says that there are only cassettes OR that it includes a cassette
								# For things that "include" a cassette, it still includes a compact disc. Otherwise, it is just a cassette and should not be counted as RM
								# Also, some say that the audio recording is in "parts," but it is still assumed to be a CD
								if not 'includes' in child_physdesc_string and not 'parts' in child_physdesc_string:
									add_one = False
							if add_one:
								removable_media_count['CD'] += 1
					if filename not in removable_media_files['CD']:
						removable_media_files['CD'].append(filename)
				# The filenames in skip_files include parent-level extent statements that are also represented in child-level extents
				# For files that are not in skip_files, the RM is only mentioned in the parent-level extent, and should be counted
				elif filename not in skip_files:
					characterize_removeable_media(component)
	print filename

print "Writing CSV"
sorted_removable_media_count = sorted(removable_media_count,key=removable_media_count.get,reverse=True)

with open(removable_media_csv,'ab') as csvfile:
	writer = csv.writer(csvfile)
	for removable_media in sorted_removable_media_count:
		count = removable_media_count[removable_media]
		files = removable_media_files[removable_media]
		if not removable_media.endswith('s') and not removable_media.endswith(')'):
			removable_media = removable_media + 's'
		writer.writerow([count, removable_media, "\n".join(files)])