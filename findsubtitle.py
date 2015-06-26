import lxml
from lxml import etree
import os
from os.path import join


path = 'Real_Masters_all'
subtitles = []

for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    subt = tree.xpath('//dsc//unittitle/*')
    unitdate = tree.xpath('//dsc//unittitle/unitdate')
    if not unitdate:
        for r in subt:
            subtpath = tree.getpath(r)
            unittitle = r.getparent()
            print filename + ' ' + subtpath
            print etree.tostring(unittitle)
            # outfile = open('test/subtitles.xml', 'a')
            # outfile.write(etree.tostring(unittitle) + '\n\n\n')
            # outfile.close()
            subttag = r.tag
            if subttag not in subtitles:
                subtitles.append(subttag)
            else:
                continue
            
print subtitles
