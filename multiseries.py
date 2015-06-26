import lxml
from lxml import etree
import os
from os.path import join


path = 'Real_Masters_all'
multiseries_count = 0

for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    series = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')][@level='series']")
    for r in series:
        multiseries = r.xpath(".//*[starts-with(local-name(), 'c0')][@level='series']")
        for m in multiseries:
            multiseries_count += 1
            multiseries_path = tree.getpath(m)
            parent_series = tree.getpath(r)
            siblings = r.xpath(multiseries_path)
            number = multiseries_path[-2]
            print filename + ' found a series nested in a series at ' + multiseries_path
            print number
            
print 'There are ' + str(multiseries_count) + ' series nested within series :('