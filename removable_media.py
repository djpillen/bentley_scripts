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
physfacet_types = ['CD','DVD','optical cartridge','computer disk','removable cartridge','compact disc', '5.25" floppy disk','3.25" floppy disk','zip disk','optical disk']

removable_media_count = {}
removable_media_files = {}

def characterize_removeable_media(component):
	pass

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		children = component.xpath("./*[starts-with(local-name(), 'c0')]")
		if not children:
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
						extent_number = re.findall(r'(\d+)', extent)[0]
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
									extent_type = container_summary_type + 's (quantity not	specified)'
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
	print filename


print "Writing CSV"
sorted_removable_media_count = sorted(removable_media_count,key=removable_media_count.get,reverse=True)

with open(removable_media_csv,'ab') as csvfile:
	writer = csv.writer(csvfile)
	for removable_media in sorted_removable_media_count:
		count = removable_media_count[removable_media]
		if len(removable_media_files[removable_media]) < 10:
			files = removable_media_files[removable_media]
		else:
			files = ''
		if not removable_media.endswith('s') and not removable_media.endswith(')'):
			removable_media = removable_media + 's'
		writer.writerow([count, removable_media, files])