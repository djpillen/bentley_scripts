from lxml import etree

tree = etree.parse('C:/Users/djpillen/GitHub/vandura/Real_Masters_all/infolib.xml')

physdescs = tree.xpath('//physdesc')

for physdesc in physdescs:
	extents = physdesc.xpath('./extent')
	if extents:
		extent = extents[0]
		extent_text = extent.text
		if 'minute cassette' in extent_text:
			extent.text = '1 audiocassettes'
			dimensions = etree.Element('dimensions')
			dimensions.text = extent_text.replace(' cassette','s')
			physdesc.append(dimensions)

with open('C:/Users/djpillen/GitHub/vandura/Real_Masters_all/infolib.xml','w') as ead_out:
	ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))