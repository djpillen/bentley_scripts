import csv
from lxml import etree
from os.path import join

access_file = 'accessrestrict_expired.csv'
path = 'Real_Masters_all'

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
        with open('accessrestrict_expired_fulltext.csv', 'ab') as csvout:
            writer = csv.writer(csvout, dialect='excel')
            writer.writerow([filename, date_path, normal, etree.tostring(restriction)])


'''
file = 'accessrestrictdate-7.csv'

expired = 0
with open(file, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        filename = row[0]
        path = row[1]
        normal = row[3]
        to_string = row[4]
        if normal < '2015-07-02':
            print normal
            expired += 1
            with open('accessrestrict_expired.csv','ab') as csvout:
                writer = csv.writer(csvout, dialect='excel')
                writer.writerow([filename, path, normal, to_string])

print expired
'''
