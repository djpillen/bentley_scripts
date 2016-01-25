from lxml import etree
import os
from os.path import join
import csv

path = 'C:/Users/djpillen/GitHub/test_run/ead'
digital_object_csv = 'C:/Users/djpillen/GitHub/test_run/posted_digital_objects.csv'

digital_object_refs = {}

with open(digital_object_csv,'rb') as csvfile:
	print "Building dictionary"
	reader = csv.reader(csvfile)
	for row in reader:
		dao_href = row[0]
		aspace_ref = row[1]
		digital_object_refs[dao_href] = aspace_ref

for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	daos = tree.xpath('//dao')
	for dao in daos:
		dao_href = dao.attrib['href']
		if dao_href in digital_object_refs:
			dao.attrib['ref'] = digital_object_refs[dao_href]

	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))