from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

parens_around_unitdate = re.compile(r"\(<unitdate.*>.*</unitdate>\)")
for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	unittitles = tree.xpath('//did/unittitle')
	rewrite = False
	for unittitle in unittitles:
		if unittitle.xpath('./unitdate'):
			unittitle_string = etree.tostring(unittitle)
			if parens_around_unitdate.search(unittitle_string):
				rewrite = True
				did = unittitle.getparent()
				unittitle_string_fix = re.sub(r"\((<unitdate.*>.*</unitdate>)\)",r"\1",unittitle_string)
				new_unittitle = etree.fromstring(unittitle_string_fix)
				did.insert(did.index(unittitle)+1, new_unittitle)
				did.remove(unittitle)
	if rewrite:
		with open(join(path,filename),'w') as f:
			f.write(etree.tostring(tree, encoding='utf-8',xml_declaration=True,pretty_print=True))

