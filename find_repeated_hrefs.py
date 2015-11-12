from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

hrefs = {}

for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	daos = tree.xpath('//dao')
	for dao in daos:
		href = dao.attrib['href'].strip()
		if href not in hrefs:
			hrefs[href] = []
		hrefs[href].append(filename)

for href in hrefs:
	if len(hrefs[href]) > 1:
		print href, hrefs[href]