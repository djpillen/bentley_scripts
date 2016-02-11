from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	unittitles = tree.xpath('//did/unittitle')
	for unittitle in unittitles:
		if unittitle.text and unittitle.xpath("unitdate"):
			print filename, etree.tostring(unittitle)