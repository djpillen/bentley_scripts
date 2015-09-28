from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

subelements = []
whatever = ['extptr','num','list','blockquote']

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    for subelement in tree.xpath('//p/*'):
        if subelement.xpath('.//p'):
            if subelement.tag not in whatever:
                p_tag = subelement.getparent()
                print subelement.tag
                print etree.tostring(p_tag)
            #if subelement.tag not in subelements:
                #subelements.append(subelement.tag)

#print subelements
