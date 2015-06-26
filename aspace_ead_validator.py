import lxml
from lxml import etree
import os
from os.path import join
import csv
import re

path = "Real_Masters_all"

for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    extents = tree.xpath('//ead/archdesc/did//physdesc/extent')
    components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
    dates = tree.xpath('//unitdate')
    daos = tree.xpath('//dao')
    unitids = tree.xpath('//unitid')
    for r in extents:
        if r.text is None:
            print filename + ' is missing an extent'
        if r.text is not None:
            begins_alpha = re.compile('^[A-Za-z]')
            if begins_alpha.match(r.text):
                print filename + ' extent begins with letters: ' + r.text
                
    for r in dates:
        if r.text is None:
            print filename + ' has an empty date'
            
    for r in components:
        t = r.xpath("./did[1]//unittitle/text()")
        subt = r.xpath("./did[1]//unittitle/*/text()")
        d = r.xpath("./did[1]//unitdate/text()")
        titlepath = tree.getpath(r)
        if len(t) == 0 and len(subt) == 0 and len(d) == 0:
            print filename + ' is missing a title at ' + titlepath
            
    # for r in daos:
        # if not 'title' in r.attrib:
            # has_plugin = raw_input('have plugin? (y/n): ')
            # if has_plugin == 'y':
                # continue
            # else:
                # print filename + ' has daos that do not have titles'
