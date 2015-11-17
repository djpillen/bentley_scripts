from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

tags = ['corpname','persname','famname']

for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	for agent in tree.xpath('//controlaccess/*'):
		if agent.tag in tags:
			if '---' in agent.text:
				new_text = agent.text.replace('---','- --')
				agent.text = new_text
	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
