from lxml import etree
import os
from os.path import join
import re

path = 'C:/Users/Public/Documents/changed'
outFilePath = 'C:/Users/Public/Documents/changed1'
for filename in os.listdir(path):
    start = open(join(path, filename), 'r')
    finish = open(join(outFilePath, filename), 'w')
    for i in start:
        finish.write(i.replace('</unitdate>and<unitdate', '</unitdate><unitdate'))
start.close()
finish.close()
    # outFilePath = 'C:/Users/Public/Documents/testandbndatesresult'
    # outFile = open((join(outFilePath, filename)), 'w')
    # # doc = etree.tostring(root, encoding="utf-8", xml_declaration=True, doctype='<!DOCTYPE ead PUBLIC "+//ISBN 1-931666-00-8//DTD ead.dtd (Encoded Archival Description (EAD) Version 2002)//EN" "ead.dtd">', pretty_print=True)
    # outFile.write(str(file))
    # outFile.close()