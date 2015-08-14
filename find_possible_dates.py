from lxml import etree
import os
from os.path import join
import re
import csv

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

four_digits = re.compile(r'\d{4}')

for filename in os.listdir(path):
    possible_dates = {}
    tree = etree.parse(join(path,filename))
    unittitles = tree.xpath('//unittitle')
    for unittitle in unittitles:
        if unittitle.text is not None:
            unittitle_text = unittitle.text.encode('utf-8')
            unittitle_path = tree.getpath(unittitle)
            if four_digits.search(unittitle_text):
                years = four_digits.findall(unittitle_text)
                for year in years:
                    if int(year) in range(1850,2015):
                        if unittitle_path not in possible_dates:
                            possible_dates[unittitle_path] = unittitle_text
    if len(possible_dates) > 0:
        for unittitle_path in possible_dates:
            with open('C:/Users/Public/Documents/possible_dates.csv','ab') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([filename, unittitle_path, possible_dates[unittitle_path]])
