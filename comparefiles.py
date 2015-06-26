import csv
import lxml
from lxml import etree
import os
from os.path import join

path = 'C:/Users/Public/Documents/Real_Masters_all_2'
path2 = 'C:/Users/Public/Documents/Master'
for filename in os.listdir(path):
    csvfile = open('C:/Users/Public/Documents/realmasterfiles.csv', 'ab')
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow([filename])
    csvfile.close()
    print filename

for filename in os.listdir(path2):
    csvfile = open('C:/Users/Public/Documents/masterfiles.csv', 'ab')
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow([filename])
    csvfile.close()
    print filename