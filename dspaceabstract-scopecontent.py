import urllib2
from lxml import etree
import urlparse
import os
from os.path import join
import re


path = 'C:/Users/djpillen/GitHub/test_dir'

for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for dao in tree.xpath('.//dao'):
        href = dao.get('href')
        handle = re.compile('^http://hdl.handle.net/')
        if handle.match(href):
            print href
            handlepath = urlparse.urlparse(href).path
            mets = "http://deepblue.lib.umich.edu/metadata/handle" + handlepath + "/mets.xml"
            page = urllib2.urlopen(mets)
            metstree = etree.parse(page)
            abstract = metstree.xpath("//dim:field[@element='description'][@qualifier='abstract']", namespaces={'dim': 'http://www.dspace.org/xmlns/dspace/dim'})
            if abstract:
                abstract = abstract[0].text
                odd = etree.Element('odd')
                ptag = etree.SubElement(odd,'p')
                ptag.text = abstract
                did = dao.getparent()
                c = did.getparent()
                c.append(odd)
                outFile = open((join(path, filename)), 'w')
                outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
                outFile.close()
