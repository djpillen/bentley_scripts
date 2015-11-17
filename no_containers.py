from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	containers = tree.xpath("//container")
	if not containers:
		print filename