from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

test_dir = 'C:/Users/djpillen/GitHub/test_dir'

subject_tags = ['subject','geogname','genreform','title']
agent_tags = ['persname','corpname','famname']

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in agent_tags and sub.text is not None:
            if not 'ref' in sub.attrib:
                print filename, sub.text.encode('utf-8')
    """
    for dao in tree.xpath('.//did/dao'):
    	if not 'ref' in dao.attrib:
    		print filename, dao.attrib['href']
	"""
