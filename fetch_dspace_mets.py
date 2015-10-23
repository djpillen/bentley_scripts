import urllib2
from lxml import etree
import urlparse
import os
from os.path import join


ead_path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
mets_path = 'C:/Users/djpillen/GitHub/test_dir/dspace_mets'


for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    daos = tree.xpath('//dao')
    for dao in daos:
        href = dao.attrib['href'].strip()
        if href.startswith('http://hdl.handle.net/2027.42'):
            print href
            handlepath = urlparse.urlparse(href).path
            mets = "http://deepblue.lib.umich.edu/metadata/handle" + handlepath + "/mets.xml"
            page = urllib2.urlopen(mets)
            metstree = etree.parse(page)
            with open(join(mets_path, the_id + '.xml'),'w') as mets_out:
                mets_out.write(etree.tostring(metstree))
