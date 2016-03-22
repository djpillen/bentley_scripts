from lxml import etree
import os
from os.path import join

master_eads = 'C:/Users/Public/Documents/test_in'
dlxs_eads = 'C:/Users/Public/Documents/test_out'

for filename in os.listdir(master_eads):
	print filename
	tree = etree.parse(join(master_eads,filename))
	physdescs = tree.xpath('//physdesc')
	for physdesc in physdescs:
		new_tag = ''
		new_text = ''
		extent_statement = False
		physical_detail = False
		physical_details = []
		extents = physdesc.xpath('./extent')
		physfacets = physdesc.xpath('./physfacet')
		dimensions = physdesc.xpath('./dimensions')
		if extents:
			extent_statement = extents[0].text.strip().encode('utf-8')
		if len(extents) == 2:
			container_summary = extents[1].text.strip().encode('utf-8')
			physical_details.append(container_summary)
		if physfacets:
			physfacet = physfacets[0].text.strip().encode('utf-8')
			physical_details.append(physfacet)
		if dimensions:
			dimension = dimensions[0].text.strip().encode('utf-8')
			physical_details.append(dimension)
		if physical_details:
			physical_detail = "; ".join(physical_details)
		if extent_statement and physical_detail:
			new_tag = 'extent'
			new_text = "{0} ({1})".format(extent_statement, physical_detail)
		elif extent_statement and not physical_detail:
			new_tag = 'extent'
			new_text = extent_statement
		elif physical_detail and not extent_statement:
			new_tag = 'physfacet'
			new_text = physical_detail
		did = physdesc.getparent()
		new_physdesc = etree.Element('physdesc')
		new_extent = etree.SubElement(new_physdesc, new_tag)
		new_extent.text = new_text.decode('utf-8')
		did.append(new_physdesc)
		did.remove(physdesc)
	with open(join(dlxs_eads,filename),'w') as f:
		f.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))



