import csv
from lxml import etree
from os.path import join


access_file = 'C:/Users/Public/Documents/accessrestrict_expired-1.csv'
path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

'''
with open(access_file, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        filename = row[0]
        print filename
        date_path = row[1]
        normal = row[2]
        tree = etree.parse(join(path,filename))
        date = tree.xpath(date_path)
        restriction = date[0].getparent()
        with open('C:/Users/Public/Documents/accessrestrict_expired_fulltext-1.csv', 'ab') as csvout:
            writer = csv.writer(csvout, dialect='excel')
            writer.writerow([filename, date_path, normal, etree.tostring(restriction)])


'''
date_file = 'C:/Users/Public/Documents/accessrestrictdate-9.csv'

expired = 0
with open(date_file, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        filename = row[0]
        path = row[1]
        normal = row[3]
        to_string = row[4]
        if normal < '2015-11-11':
            print filename, normal
            expired += 1
            with open('C:/Users/Public/Documents/accessrestrict_expired.csv','ab') as csvout:
                writer = csv.writer(csvout, dialect='excel')
                writer.writerow([filename, path, normal, to_string])

print "Expired:",expired
