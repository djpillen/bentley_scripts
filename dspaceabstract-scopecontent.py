import urllib2
from lxml import etree
import urlparse
import os
from os.path import join
import time

ead_path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'
out_path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

mets_path = 'C:/Users/djpillen/GitHub/dspace_mets'

skip = ['nispodcast.xml','bamdocs.xml','actonh.xml','stewartmary.xml','mullinsr.xml','pollackp.xml','saxj.xml','caen.xml','shurtleffm.xml','ticecarol.xml','ootbmpm.xml']
add_odd = ['schoening.xml','nsfnet.xml','gonzalesjess.xml']

for filename in os.listdir(ead_path):
    if filename not in skip:
        tree = etree.parse(join(ead_path, filename))
        for dao in tree.xpath('.//dao'):
            href = dao.get('href').strip()
            did = dao.getparent()
            c = did.getparent()
            if href.startswith('http://hdl.handle.net/2027.42'):
                if not did.xpath('./odd') and not c.xpath('./odd') or (filename in add_odd):
                    handlepath = urlparse.urlparse(href).path
                    the_id = handlepath.split('/')[-1]
                    if the_id + '.xml' not in os.listdir(mets_path):
                        print "Downloading", href
                        dspace_mets = "http://deepblue.lib.umich.edu/metadata/handle" + handlepath + "/mets.xml"
                        page = urllib2.urlopen(dspace_mets)
                        dspace_metstree = etree.parse(page)
                        with open(join(mets_path, the_id + '.xml'),'w') as mets_out:
                            mets_out.write(etree.tostring(dspace_metstree))
                        time.sleep(15)
                    print "Parsing DSpace METS for", href
                    metstree = etree.parse(join(mets_path,the_id + '.xml'))
                    abstract = metstree.xpath("//dim:field[@element='description'][@qualifier='abstract']", namespaces={'dim': 'http://www.dspace.org/xmlns/dspace/dim'})
                    if abstract and abstract is not None:
                        abstract = abstract[0].text
                        odd = etree.Element('odd')
                        ptag = etree.SubElement(odd,'p')
                        ptag.text = '(' + abstract + ')'
                        c.insert(c.index(did)+1, odd)
        outFile = open((join(out_path, filename)), 'w')
        outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True,pretty_print=True))
        outFile.close()
