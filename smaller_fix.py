from lxml import etree

tree = etree.parse('C:/Users/djpillen/GitHub/vandura/Real_Masters_all/muschba.xml')

physdescs = tree.xpath('//physdesc')
for physdesc in physdescs:
	extents = physdesc.xpath('./extent')
	if extents:
		extent = extents[0]
		if 'sheets : various media; or smaller' in extent.text:
			dimensions = physdesc.xpath('./dimensions')[0]
			dimensions.text = dimensions.text + ' or smaller'
			extent.text = extent.text.replace(' : various media; or smaller','')
			physfacet = etree.Element('physfacet')
			physfacet.text = 'various media'
			physdesc.append(physfacet)

with open('C:/Users/djpillen/GitHub/vandura/Real_Masters_all/muschba.xml','w') as ead_out:
	ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))

