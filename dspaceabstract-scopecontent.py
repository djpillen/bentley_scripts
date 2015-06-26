import urllib2
import lxml
from lxml import etree
import urlparse
import os
from os.path import join
import re


path = 'C:/Users/Public/Documents/daos'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for dao in tree.xpath('.//dao'):
        href = dao.get('href')
        handle = re.compile('^http://hdl.handle.net/')
        if handle.match(href):
            handlepath = urlparse.urlparse(href).path
            mets = "http://deepblue.lib.umich.edu/metadata/handle" + handlepath + "/mets.xml"
            page = urllib2.urlopen(mets)
            metstree = etree.parse(page)
            abstract = metstree.xpath("//dim:field[@element='description'][@qualifier='abstract']", namespaces={'dim': 'http://www.dspace.org/xmlns/dspace/dim'})
            abstract = abstract[0].text
            odd = etree.Element('odd')
            odd.text = abstract
            did = dao.getparent()
            c = did.getparent()
            c.append(odd)
            outFilePath = 'C:/Users/Public/Documents/dspacemets'
            outFile = open((join(outFilePath, filename)), 'w')
            outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
            outFile.close()