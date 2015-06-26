import csv
import lxml
from lxml import etree
import os
from os.path import join
import urllib2
from bs4 import SoupStrainer, BeautifulSoup

with open('marcxml_callno_dlxs.csv', 'rb') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        callno = row[2]
        #print callno
        dlxsurl = 'http://quod.lib.umich.edu/cgi/f/findaid/findaid-idx?c=bhlead;idno=umich-bhl-' + callno
        try:
            dlxs = urllib2.urlopen(dlxsurl)
            print callno + 'has an EAD'
            fout = open('founddlxs.txt', 'a')
            fout.write(callno + ' has an EAD' + '\n\n')
            fout.close()
        except:
            print callno + ' does not have an EAD'
        
        