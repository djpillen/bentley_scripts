from lxml import etree
import os
from os.path import join

imported = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
exported = 'C:/Users/Public/Documents/aspace_exports_unpublished'

filenames = {}

print "Gathering original filenames..."
for filename in os.listdir(imported):
    print filename
    tree = etree.parse(join(imported,filename))
    eadid = tree.xpath('//eadid')[0]
    eadid_text = eadid.text.strip()
    filenames[eadid_text] = filename

print "Changing filenames..."

for filename in os.listdir(exported):
    print "Changing {0}".format(filename)
    tree = etree.parse(join(exported,filename))
    ns = {'ead':'urn:isbn:1-931666-22-9'}
    eadid = tree.xpath('//ead:eadid',namespaces=ns)[0]
    eadid_text = eadid.text.strip()
    imported_name = filenames[eadid_text]
    os.rename(join(exported,filename), join(exported,imported_name))
    print "{0} changed to {1}".format(filename,imported_name)
