import csv
from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
expired_csv = 'C:/Users/Public/Documents/accessrestrict_expired.csv'

with open(expired_csv,'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            filename = row[0]
            if filename in os.listdir(path):
                print "Removing an expired date in",filename
                date_path = row[1]
                tree = etree.parse(join(path,filename))
                access_date = tree.xpath(date_path)[0]
                access_path = access_date.getparent().getparent()
                access_path.getparent().remove(access_path)
                with open(join(path,filename),'w') as ead_out:
                    ead_out.write(etree.tostring(tree, pretty_print=True, encoding='utf-8', xml_declaration=True))
