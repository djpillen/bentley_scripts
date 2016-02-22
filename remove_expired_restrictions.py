import csv
from lxml import etree
import os
from os.path import join
from datetime import datetime

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
expired_csv = 'C:/Users/Public/Documents/accessrestrict_expired.csv'

now = datetime.now().strftime("%Y-%m-%d")
for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    accessrestricts = tree.xpath('//accessrestrict')
    for accessrestrict in accessrestricts:
        dates = accessrestrict.xpath('./p/date')
        if dates:
            date = dates[0]
            if 'normal' in date.attrib:
                normalized = date.attrib['normal']
                if normalized < now:
                    accessrestrict.getparent().remove(accessrestrict)
                    print "Removed {0} from {1}".format(normalized, filename)
    with open(join(path,filename),'w') as f:
        f.write(etree.tostring(tree,encoding='utf-8',pretty_print=True,xml_declaration=True))