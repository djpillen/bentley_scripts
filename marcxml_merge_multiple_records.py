from lxml import etree
import os
from os.path import join
import shutil
import re

marc_no_ead = 'C:/Users/djpillen/GitHub/marc_xml-all/marc_xml-no_ead-split'
marc_no_ead_joined = 'C:/Users/djpillen/GitHub/marc_xml-all/marc_xml-no_ead-joined'

multiple_records = []

for filename in os.listdir(marc_no_ead):
	print filename
	tree = etree.parse(join(marc_no_ead,filename))
	ns = {'marc': 'http://www.loc.gov/MARC21/slim'}
	record = tree.xpath('/marc:record',namespaces=ns)[0]
	call_number = tree.xpath('//marc:datafield[@tag="852"]/marc:subfield[@code="h"]', namespaces=ns)[0].text.strip().encode('utf-8')
	collection_id = re.findall(r"^\d+", call_number)[0]
	dst_filename = collection_id+".xml"
	if dst_filename not in os.listdir(marc_no_ead_joined):
		collection = etree.Element("collection")
		collection.append(record)
		with open(join(marc_no_ead_joined,dst_filename),'w') as f:
			f.write(etree.tostring(collection))
	else:
		existing_marc = etree.parse(join(marc_no_ead_joined,dst_filename))
		collection = existing_marc.xpath('/collection')[0]
		collection.append(record)
		with open(join(marc_no_ead_joined,dst_filename),'w') as f:
			f.write(etree.tostring(collection))
		if collection_id not in multiple_records:
			multiple_records.append(collection_id)

print multiple_records
print len(multiple_records)