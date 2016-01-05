from lxml import etree
import os
from os.path import join
import csv

ead_path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

beal_av_boxes = 'C:/Users/djpillen/GitHub/audio_reel_to_reel_project/BEAL_exports/all_reels.csv'

av_boxes_dict = {}

with open(beal_av_boxes,'rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		# Grab the digfilecalc -- should match up with hrefs in daos
		digfilecalc = row[15]
		av_box = row[6]
		av_boxes_dict[digfilecalc] = av_box

for filename in os.listdir(ead_path):
	tree = etree.parse(join(ead_path,filename))
	daos = tree.xpath('//dao')
	for dao in daos:
		href = dao.attrib['href']
		if href in av_boxes_dict:
			av_box = av_boxes_dict[href]
			did = dao.getparent()
			dao_component = did.getparent()
			container_component = dao_component.getparent()
			if not container_component.xpath('./did/container'):
				container = etree.Element('container')
				container.attrib['type'] = 'avbox'
				container.attrib['label'] = 'AV Box'
				container.text = av_box
				container_component.xpath('./did')[0].insert(0, container)
	with open(join(ead_path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
	print filename



