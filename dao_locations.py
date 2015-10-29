from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
outpath = 'C:/Users/djpillen/GitHub/test_dir/eads'

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    daos = tree.xpath('//dao')
    rewrite = False
    for dao in daos:
        parent = dao.getparent()
        if parent.tag != 'did':
            rewrite = True

            parent_did = parent.xpath('./did')[0]
            parent_did.append(dao)
            print filename, parent.tag, dao.attrib['href']
    if rewrite:
        with open(join(path,filename),'w') as ead_out:
            ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
