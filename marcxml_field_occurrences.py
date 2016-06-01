from lxml import etree
import os
from os.path import join
import csv

marc_path = 'C:/Users/djpillen/GitHub/marc_xml-all/marc_xml-no_ead-split'
field_occurrences_csv = 'C:/users/djpillen/GitHub/marc_xml-all/marc_field_occurrences.csv'

marc_fields = {}

for filename in os.listdir(marc_path):
	print filename
	ns = {'marc': 'http://www.loc.gov/MARC21/slim'}
	tree = etree.parse(join(marc_path,filename))
	for datafield in tree.xpath('//marc:datafield', namespaces=ns):
		datafield_tag = datafield.attrib["tag"]
		if datafield_tag not in marc_fields:
			marc_fields[datafield_tag] = {"count":0,"subfields":{},"files":[]}
		marc_fields[datafield_tag]["count"] += 1
		if filename not in marc_fields[datafield_tag]["files"] and len(marc_fields[datafield_tag]["files"]) < 5:
			marc_fields[datafield_tag]["files"].append(filename)
		for subfield in datafield.xpath('./marc:subfield',namespaces=ns):
			subfield_code = subfield.attrib["code"]
			subfield_text = subfield.text.strip().encode('utf-8')
			if subfield_code not in marc_fields[datafield_tag]["subfields"]:
				marc_fields[datafield_tag]["subfields"][subfield_code] = {"count":0,"examples":[]}
			marc_fields[datafield_tag]["subfields"][subfield_code]["count"] += 1
			if len(marc_fields[datafield_tag]["subfields"][subfield_code]["examples"]) < 3 and subfield_text not in marc_fields[datafield_tag]["subfields"][subfield_code]["examples"]:
				marc_fields[datafield_tag]["subfields"][subfield_code]["examples"].append(subfield_text)

marc_fields_sortable = {}
for field in marc_fields:
	try:
		sort_field = int(field)
	except:
		sort_field = field
	marc_fields_sortable[sort_field] = field

data = []
for sortable_datafield in sorted(marc_fields_sortable):
	datafield = marc_fields_sortable[sortable_datafield]
	datafield_data = []
	datafield_data.append(datafield)
	datafield_data.append(marc_fields[datafield]["count"])
	datafield_data.append(marc_fields[datafield]["files"])
	for subfield in marc_fields[datafield]["subfields"]:
		datafield_data.append(subfield)
		datafield_data.append(marc_fields[datafield]["subfields"][subfield]["count"])
		datafield_data.append(marc_fields[datafield]["subfields"][subfield]["examples"])
	data.append(datafield_data)

with open(field_occurrences_csv,'wb') as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(data)