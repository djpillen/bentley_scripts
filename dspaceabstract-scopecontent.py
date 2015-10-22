import urllib2
from lxml import etree
import urlparse
import os
from os.path import join


out_path = 'C:/Users/djpillen/GitHub/test_dir/eads'

skip = ['nispodcast.xml','bamdocs.xml','actonh.xml','stewartmary.xml','mullinsr.xml','pollackp.xml','saxj.xml','caen.xml','shurtleffm.xml','ticecarol.xml','ootbmpm.xml']
add_odd = ['schoening.xml','nsfnet.xml','gonzalesjess.xml']

for filename in os.listdir(path):
    if filename not in skip:
        tree = etree.parse(join(path, filename))
        for dao in tree.xpath('.//dao'):
            href = dao.get('href').strip()
            did = dao.getparent()
            c = did.getparent()
            if href.startswith('http://hdl.handle.net/2027.42'):
                if not did.xpath('./odd') and not c.xpath('./odd') or (filename in add_odd):
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
                        ptag.text = '(' + abstract + ')'
                        c.insert(c.index(did)+1, odd)
        outFile = open((join(out_path, filename)), 'w')
        outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True,pretty_print=True))
        outFile.close()
