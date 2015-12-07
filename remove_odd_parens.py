from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
	for component in components:
		odds = component.xpath('./odd')
		for odd in odds:
			p_tag = odd.xpath('./p')[0]
			odd_text = etree.tostring(p_tag).replace('\n','').replace('<p>','').replace('</p>','').strip()
			if odd_text.startswith('(') and odd_text.endswith(')'):
				new_text = re.sub(r'^\((.*?)\)$',r'\1', odd_text)
				p_tag_loc = odd.index(p_tag)
				odd.remove(p_tag)
				new_p = etree.Element('p')
				new_p.text = new_text
				odd.insert(p_tag_loc,new_p)
		with open(join(path,filename),'w') as ead_out:
			ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
	print filename
