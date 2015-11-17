from lxml import etree
import os
from os.path import join

# Add an id attribute to titlepage/publisher for the appropriate classification (mhc or uarp)

path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'
classification_base = '/repositories/2/classifications/'
mhc_classification = classification_base + '1'
uarp_classification = classification_base + '2'

for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	publisher = tree.xpath('//titlepage/publisher')[0]
	if 'Michigan Historical Collections' in etree.tostring(publisher):
		publisher.attrib['id'] = mhc_classification
	elif 'University Archives' in etree.tostring(publisher):
		publisher.attrib['id'] = uarp_classification
	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))