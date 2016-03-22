from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'


begins_with_words = re.compile(r"^[A-Za-z]")
begins_with_spaces = re.compile(r"^\s")
"""
first_words = []
for filename in os.listdir(path):
	print filename
	tree = etree.parse(join(path,filename))
	unitdates = tree.xpath('//unittitle/unitdate')
	for unitdate in unitdates:
		if unitdate.attrib['type'] == 'bulk':
			unitdate_text = unitdate.text.strip().encode("utf-8")
			if begins_with_words.match(unitdate_text):
				first_word = re.findall(r"^[A-Za-z]+", unitdate_text)[0]
				if first_word not in first_words:
					first_words.append(first_word)

print first_words
"""

bulk_words = ["primarily","mainly","mostly","bulk"]
for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	unitdates = tree.xpath('//unittitle/unitdate')
	rewrite = False
	for unitdate in unitdates:
		unitdate_text = unitdate.text.strip().encode('utf-8').lower()
		if any(word in unitdate_text for word in bulk_words):
			print filename, unitdate_text
		#if begins_with_words.match(unitdate_text):
			#first_word = re.findall(r"[A-Za-z]+",unitdate_text)[0]
			#if first_word in bulk_words:
				#print filename, unitdate_text
					#rewrite = True
					#unitdate_text_fix = re.sub(r"^[A-Za-z]+\s+","",unitdate_text)
					#unitdate.text = unitdate_text_fix
			#if begins_with_spaces.match(unitdate_text):
				#rewrite = True
				#unitdate_text_fix = re.sub(r"^\s+","",unitdate_text)
				#unitdate.text = unitdate_text_fix
	if rewrite:
		with open(join(path,filename),'w') as f:
			f.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))

