from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/test_dir/eads'
outpath = 'C:/Users/djpillen/GitHub/test_dir/eads'

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    daos = tree.xpath('//dao')
    for dao in daos:
        did = dao.getparent()
        unittitle_path = did.xpath('./unittitle')[0]
        unittitle_string = etree.tostring(unittitle_path)
        unittitle_no_tags = re.sub(r'<(.*?)>','',unittitle_string)
        unittitle = re.sub(r'\s+',' ',unittitle_no_tags.strip())
        dao.attrib['title'] = unittitle.encode('utf-8')
    with open(join(outpath,filename),'w') as ead_out:
        ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
    print filename
