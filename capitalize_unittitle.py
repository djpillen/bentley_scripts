from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	unittitles = tree.xpath('//did/unittitle')
	for unittitle in unittitles:
		if unittitle.text and len(unittitle.text.strip()) >= 1:
			unittitle_text = re.sub(r'^\s+','',unittitle.text)
			if not unittitle_text.startswith('de') and not unittitle_text.startswith('vs.') and not unittitle_text.startswith('von'):
				unittitle_text = unittitle_text[0].upper() + unittitle_text[1:]
			unittitle.text = unittitle_text
			if unittitle_text == '()':
				unittitle.getparent().remove(unittitle)
	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
	print filename
