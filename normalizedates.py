from lxml import etree
import os
from os.path import join
import re

path = 'new4'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    d = tree.xpath('//unitdate')
    for i in d:
        yyyy = re.compile(r'^\d{4}$')
        yyyys = re.compile(r'^\d{4}s$')
        yyyy_yyyy = re.compile(r'^\d{4}\-\d{4}$')
        yyyys_yyyy = re.compile(r'^\d{4}s\-\d{4}$')
        yyyy_yyyys = re.compile(r'^\d{4}\-\d{4}s$')
        yyyys_yyyys = re.compile(r'^\d{4}s\-\d{4}s$')
        if yyyy.match(i.text) and len(i.text) == 4:
            i.attrib['normal'] = i.text
        elif yyyys.match(i.text) and len(i.text) == 5:
            i.attrib['normal'] = i.text.replace('s', '') + '/' + i.text[:3] + '9'
            i.attrib['certainty'] = "approximate"
        elif yyyy_yyyy.match(i.text) and len(i.text) == 9:
            i.attrib['normal'] = i.text.replace('-', '/')
        elif yyyys_yyyy.match(i.text) and len(i.text) == 10:
            i.attrib['normal'] = i.text.replace('-', '/').replace('s', '')
            i.attrib['certainty'] = "approximate"
        elif yyyy_yyyys.match(i.text) and len(i.text) == 10:
            normalized = i.text.replace('-', '/')
            normalized = normalized.replace(normalized[-2:], '9')
            i.attrib['normal'] = normalized
            i.attrib['certainty'] = "approximate"
        elif yyyys_yyyys.match(i.text) and len(i.text) == 11:
            normalized = i.text.replace('-', '/').replace('s', '', 1)
            normalized = normalized.replace(normalized[-2:], '9')
            i.attrib['normal'] = normalized
            i.attrib['certainty'] = "approximate"
        else:
            continue
    outfilepath = 'new5'
    outfile = open((join(outfilepath, filename)), 'w')
    outfile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
    outfile.close()
    print filename
