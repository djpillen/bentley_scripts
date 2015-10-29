import csv

filename = 'U:/web_archives/cdl-links.csv'

with open(filename,'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader,None)
    for row in reader:
        coll_id = row[0]
        ead_href = row[1]
        link = row[2]
        link_type = row[3]
        href_id = ead_href.split('-')[0]
        if coll_id != href_id:
            print coll_id, href_id
