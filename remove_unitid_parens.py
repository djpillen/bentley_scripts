from lxml import etree
import os
from os.path import join

vandura = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
trial = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

for path in [vandura, trial]:
	for filename in os.listdir(path):
		tree = etree.parse(join(path,filename))
		unitids = tree.xpath('//dsc//unitid')
		for unitid in unitids:
			if unitid.text:
				if ')' in unitid.text or '(' in unitid.text:
					unitid.text = unitid.text.replace('(','').replace(')','').strip()
		with open(join(path,filename),'w') as ead_out:
			ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
		print path, filename