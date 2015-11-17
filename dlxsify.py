from lxml import etree
import os
from os.path import join

path = 'C:/Users/Public/Documents/aspace_exports/aspace_exports_20151110_modified'

# Add up to c08
# add type="call number" to top unitid

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	unitid = tree.xpath('//unitid')[0]
	unitid.attrib['type'] = 'call number'