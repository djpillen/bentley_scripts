from lxml import etree
import os

tree = etree.parse('C:/Users/djpillen/GitHub/vandura/Real_Masters_all/englerj.xml')
physdescs = tree.xpath('//physdesc')
for physdesc in physdescs:
	extents = physdesc.xpath('./extent')
	if extents:
		extent = extents[0]
		if extent.text == '1 VHS Tape':
			extent.text = '1 videotapes'
			physfacets = physdesc.xpath('./physfacet')
			if physfacets:
				physfacet = physfacets[0].text
				physfacet = physfacet + '; VHS (TM)'
			else:
				physfacet = etree.Element('physfacet')
				physfacet.text = 'VHS (TM)'
				physdesc.append(physfacet)
with open('C:/Users/djpillen/GitHub/vandura/Real_Masters_all/englerj.xml','w') as ead_out:
	ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
