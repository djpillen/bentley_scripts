from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

the_files = {}
show_me = ['bhl.xml']
ignore = ['nispodcast.xml','bamdocs.xml','actonh.xml','stewartmary.xml','mullinsr.xml','pollackp.xml','saxj.xml','caen.xml','schoening.xml','shurtleffm.xml','ticecarol.xml','nsfnet.xml','ootbmpm.xml','gonzalesjess.xml']
for filename in os.listdir(path):
    if filename in show_me:
        tree = etree.parse(join(path,filename))
        daos = tree.xpath('//dao')
        for dao in daos:
            if dao.attrib['href'].startswith('http://hdl.handle.net/2027.42'):
                did = dao.getparent()
                component = did.getparent()
                if did.xpath('./odd') or component.xpath('./odd'):
                    if filename not in the_files:
                        the_files[filename] = []
                    the_files[filename].append(tree.getpath(dao))

for filename in the_files:
    if filename in show_me:
        for loc in the_files[filename]:
            print loc
