from lxml import etree
import os
from os.path import join


'''
path = 'Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    didodd = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]//did/odd")
    for r in didodd:
        with open('didodd.csv','ab') as csvfile:
            writer = csv.writer(csvfile, dialect='excel')
            writer.writerow([filename, tree.getpath(r), etree.tostring(r)])
    print filename
'''


path = 'Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    didodd = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]//did/odd")
    for r in didodd:
        odd = r
        did = r.getparent()
        c = did.getparent()
        c.insert(c.index(did)+1, odd)
    outFilePath = 'moveodd'
    outFile = open((join(outFilePath, filename)), 'w')
    outFile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
    outFile.close()
    print filename
