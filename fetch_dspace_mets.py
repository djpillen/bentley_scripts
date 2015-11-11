import urllib2
from lxml import etree
import urlparse
import os
from os.path import join


ead_path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
mets_path = 'C:/Users/djpillen/GitHub/dspace_mets'


for filename in os.listdir(ead_path):
    tree = etree.parse(join(ead_path, filename))
    daos = tree.xpath('//dao')
    for dao in daos:
        href = dao.attrib['href'].strip()
        if href.startswith('http://hdl.handle.net/2027.42'):
            
            handlepath = urlparse.urlparse(href).path
            the_id = handlepath.split('/')[-1]
            if the_id + '.xml' not in os.listdir(mets_path):
                print href
                mets = "http://deepblue.lib.umich.edu/metadata/handle" + handlepath + "/mets.xml"
                page = urllib2.urlopen(mets)
                metstree = etree.parse(page)
                with open(join(mets_path, the_id + '.xml'),'w') as mets_out:
                    mets_out.write(etree.tostring(metstree))
