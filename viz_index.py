from lxml import etree
import os
from os.path import join
import re

data_path = 'C:/Users/Dallas/Documents/projects/relationships/pages/data'
page_path = 'C:/Users/Dallas/Documents/projects/relationships/pages'
ead_path = 'C:/Users/Dallas/Documents/GitHub/vandura/Real_Masters_all'

dummy_index = 'C:/Users/Dallas/Documents/projects/relationships/dummy_index.html'
real_index = 'C:/Users/Dallas/Documents/projects/relationships/index.html'

eadids = {}

for filename in os.listdir(data_path):
	eadid = filename.replace('.json','')
	eadids[eadid] = ''
	dummy_text = open(dummy_index,'r').read()
	page = dummy_text.replace('EADID','"' + eadid + '"')
	with open(join(page_path,eadid + '.html'),'w') as outfile:
		outfile.write(page)
	
for filename in os.listdir(ead_path):
	print filename
	tree = etree.parse(join(ead_path,filename))
	eadid = tree.xpath('//eadid')[0].text
	coll_title = tree.xpath('//unittitle')[0]
	coll_title = re.sub(r'<(.*?)>','',etree.tostring(coll_title))
	eadids[eadid] = coll_title.encode('utf-8')
	
with open(real_index,'a') as index:
	for eadid in eadids:
		index.write("<a href='pages/" + eadid + ".html'>" + eadids[eadid] + "</a><br/>")
