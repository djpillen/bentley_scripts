from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

list_followers = []

note_types = ['bioghist','arrangement','odd','scopecontent','accessrestrict','relatedmaterial','processinfo','userestrict','altformavail','bibliography']

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	for elem in tree.xpath('//*'):
		if elem.tag in note_types and elem.xpath('.//list'):
			elem_string = etree.tostring(elem)
			elem_string = elem_string.replace(' ','').replace('\n','')
			list_follower = re.findall(r'</list>(?!</item>)(?!<list)(?!</p></%s>)(?!</%s>)(?!</p><p><extptrhref="uarpacc")(.{1,20})' % (elem.tag, elem.tag),elem_string)
			if list_follower:
				print filename, elem.tag, list_follower

