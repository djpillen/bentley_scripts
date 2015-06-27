from lxml import etree
import os
from os.path import join

path = 'C:/Users/Public/Documents/Real_Masters_all'
for filename in os.listdir(path):
    tree = etree.parse(join(path, filename))
    if tree.xpath("//descgrp/list"):
        print filename
        fout = open('C:/Users/Public/Documents/descgrplist.txt', 'a')
        fout.write(filename + '\n')
        fout.close()
    # for cs in tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]"):
        # t = cs.xpath("./did[1]//unittitle/text()")
        # subt = cs.xpath("./did[1]//unittitle/*/text()")
        # d = cs.xpath("./did[1]//unitdate/text()")
        # titlepath = tree.getpath(cs)
        # if len(t) == 0 and len(subt) == 0 and len(d) == 0:
            # csvfile = open('C:/Users/BHL Admin/Desktop/EADs/emptytitles.csv', 'ab')
            # writer = csv.writer(csvfile, dialect='excel')
            # writer.writerow([filename, titlepath])
            # csvfile.close()
