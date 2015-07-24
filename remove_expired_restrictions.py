import csv
from lxml import etree
import os
from os.path import join
from prettifydirectory import prettify_xml_in_directory

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

with open('C:/Users/Public/Documents/accessrestrict_expired_fulltext-1.csv','rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            filename = row[0]
            if filename in os.listdir(path):
                date_path = row[1]
                parser = etree.XMLParser(remove_blank_text=True)
                tree = etree.parse(join(path,filename), parser)
                access_date = tree.xpath(date_path)
                access_path = access_date[0].getparent().getparent()
                access_path.getparent().remove(access_path)
                outfile = open((join(path, filename)), 'w')
                outfile.write(etree.tostring(tree, pretty_print=True, encoding='utf-8', xml_declaration=True))
                outfile.close()
