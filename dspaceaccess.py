import urllib2
from lxml import etree
import urlparse
import os
from os.path import join
import re
import csv


path = 'C:/Users/Public/Documents/dspace'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    for dao in tree.xpath('.//dao'):
        href = dao.get('href')
        handle = re.compile('^http://hdl.handle.net/2027')
        if handle.match(href):
            handlepath = urlparse.urlparse(href).path
            mets = "http://deepblue.lib.umich.edu/metadata/handle" + handlepath + "/mets.xml"
            page = urllib2.urlopen(mets)
            metstree = etree.parse(page)
            if metstree.xpath("//dim:field[@element='rights'][@qualifier='access']", namespaces={'dim': 'http://www.dspace.org/xmlns/dspace/dim'}):
                access = metstree.xpath("//dim:field[@element='rights'][@qualifier='access']", namespaces={'dim': 'http://www.dspace.org/xmlns/dspace/dim'})
                access = access[0].text
                with open('C:/Users/Public/Documents/dspaceaccess.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, href, access])
    print filename
