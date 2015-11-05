from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

tags = ['persname','corpname','famname']
encodinganalogs = {'persname':[],'corpname':[],'famname':[]}
suspect = ['710','700']
fixes = {'610':'710','611':'711','600':'700'}

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	controlaccesses = tree.xpath('//controlaccess')
	for controlaccess in controlaccesses:
		if controlaccess.xpath('./head'):
			if not 'Contributor' in controlaccess.xpath('./head')[0].text:
				for elem in controlaccess.xpath('./*'):
					if elem.tag in tags and 'encodinganalog' in elem.attrib:
						tag = elem.tag
						encodinganalog = elem.attrib['encodinganalog']
						if encodinganalog not in encodinganalogs[tag]:
							encodinganalogs[tag].append(encodinganalog)
						#if encodinganalog in suspect and encodinganalog not in encodinganalogs[tag]:
							#encodinganalogs[tag][encodinganalog] = []
						#if encodinganalog in suspect and filename not in encodinganalogs[tag][encodinganalog]:
							#encodinganalogs[tag][encodinganalog].append(filename)




	print filename


for tag in encodinganalogs:
	print tag, encodinganalogs[tag]
		#print tag, encodinganalog, encodinganalogs[tag][encodinganalog]