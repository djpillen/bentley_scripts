from lxml import etree
import os
from os.path import join
import shutil
import re

marc_path = 'C:/Users/djpillen/GitHub/marc_xml-all/marc_xml-all-split'
ead_path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

marc_ead = 'C:/Users/djpillen/GitHub/marc_xml-all/marc_xml-has_ead-split'
marc_no_ead = 'C:/Users/djpillen/GitHub/marc_xml-all/marc_xml-no_ead-split'
marc_unknown = 'C:/Users/djpillen/GitHub/marc_xml-all/marc_xml-no_ead_no_callno'

ead_call_numbers = []
ead_collection_ids = []

for filename in os.listdir(ead_path):
	print filename
	tree = etree.parse(join(ead_path,filename))
	unitid = tree.xpath('//archdesc/did/unitid')[0].text.strip().encode('utf-8')
	eadid = tree.xpath('//eadid')[0].text.strip().encode('utf-8')
	collection_id = eadid.split('-')[-1]
	if unitid not in ead_call_numbers:
		ead_call_numbers.append(unitid)
	if collection_id not in ead_collection_ids:
		ead_collection_ids.append(collection_id)

for filename in os.listdir(marc_path):
	print filename
	ns = {'marc': 'http://www.loc.gov/MARC21/slim'}
	tree = etree.parse(join(marc_path,filename))
	ead_link = tree.xpath('//marc:datafield[@tag="856"]/marc:subfield[@code="u"]', namespaces=ns)
	call_number = tree.xpath('//marc:datafield[@tag="852"]/marc:subfield[@code="h"]', namespaces=ns)
	if ead_link:
		ead_link_text = ead_link[0].text.strip().encode('utf-8')
		if 'findaid' in ead_link_text and filename not in os.listdir(marc_ead):
			shutil.copy(join(marc_path,filename),marc_ead)
			continue
	elif call_number:
		call_number_text = call_number[0].text.strip().encode('utf-8')
		collection_id = False
		collection_ids = re.findall(r"^\d+",call_number_text)
		if collection_ids:
			collection_id = collection_ids[0]
		if call_number_text in ead_call_numbers and filename not in os.listdir(marc_ead):
			shutil.copy(join(marc_path,filename),marc_ead)
			continue
		elif collection_id and collection_id in ead_collection_ids and filename not in os.listdir(marc_ead):
			shutil.copy(join(marc_path,filename),marc_ead)
			continue
		elif filename not in os.listdir(marc_no_ead):
			shutil.copy(join(marc_path,filename),marc_no_ead)
			continue
	else:
		if filename not in os.listdir(marc_unknown):
			shutil.copy(join(marc_path,filename),marc_unknown)
			continue



