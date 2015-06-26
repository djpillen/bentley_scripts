import lxml
from lxml import etree
import os
from os.path import join
import re
import csv

path = 'S:/Curation/Projects/Mellon/ArchivesSpace/ATeam_Migration/EADs/Real_Masters_all'
eads = re.compile('\.xml$')
for filename in os.listdir(path):
    if eads.search(filename):
        tree = etree.parse(join(path, filename))
        accessrestrict = tree.xpath('//archdesc/descgrp/accessrestrict')
        if not accessrestrict:
            print filename

               