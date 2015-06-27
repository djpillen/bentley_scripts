from lxml import etree
import os
from os.path import join

path = 'path'

for filename in os.listdir(path):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(join(path,filename), parser)
    root = tree.getroot()
    for elem in root.iter('*'):
        if elem.text is not None:
            elem.text = elem.text.strip()
            elem.text = elem.text.rstrip(",")
    outFilePath = 'path2'
    outFile = open((join(outFilePath,filename)),'w')
    doc = etree.tostring(root, encoding="utf-8", xml_declaration=True, doctype='<!DOCTYPE ead PUBLIC "+//ISBN 1-931666-00-8//DTD ead.dtd (Encoded Archival Description (EAD) Version 2002)//EN" "ead.dtd">', pretty_print=True)
    outFile.write(doc)
    outFile.close()
