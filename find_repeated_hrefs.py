from lxml import etree
import os
from os.path import join
import csv
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
repeat_csv = 'C:/Users/Public/Documents/repeating_hrefs.csv'

hrefs = {}

for filename in os.listdir(path):
	print "Assembling hrefs for {0}".format(filename)
	tree = etree.parse(join(path,filename))
	daos = tree.xpath('//dao')
	for dao in daos:
		href = dao.attrib['href'].strip()
		if href not in hrefs:
			hrefs[href] = []
		hrefs[href].append(filename)

repeated_hrefs = {}

for href in hrefs:
	print "Assembling dictionary of repeating hrefs"
	if len(hrefs[href]) > 1:
		repeated_hrefs[href] = {}
		for filename in hrefs[href]:
			repeated_hrefs[href][filename] = []

for filename in os.listdir(path):
	print "Checking for repeating hrefs in {0}".format(filename)
	tree = etree.parse(join(path,filename))
	daos = tree.xpath('//dao')
	for dao in daos:
		href = dao.attrib['href'].strip()
		if href in repeated_hrefs:
			component = dao.getparent()
			unittitle_path = component.xpath('./unittitle')[0]
			unittitle_string = etree.tostring(unittitle_path)
			unittitle = re.sub(r'<(.*?)>', '', unittitle_string)
			repeated_hrefs[href][filename].append(unittitle)


with open(repeat_csv,'ab') as csvfile:
	print "Writing CSV"
	writer = csv.writer(csvfile)
	for href in repeated_hrefs:
		row = []
		row.append(href)
		for filename in repeated_hrefs[href]:
			row.append(filename)
			row.extend(repeated_hrefs[href][filename])
		writer.writerow(row)