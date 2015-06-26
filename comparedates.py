import csv
import lxml
from lxml import etree
import os
from os.path import join

with open('normalattributes-7_split.csv', 'rb') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        filename = row[0]
        xpath = row[1]
        begin = row[2]
        end = row[3]
        if len(begin) is not 0 and len(end) is not 0:
            if begin > end:
                with open('dates_begin_after_end-4.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, xpath, begin, end])
        print filename