import csv
import urllib2

with open('marcxml_callno_dlxs.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        callno = row[2]
        #print callno
        dlxsurl = 'http://quod.lib.umich.edu/cgi/f/findaid/findaid-idx?c=bhlead;idno=umich-bhl-' + callno
        if urllib2.urlopen(dlxsurl):
            print callno + 'has an EAD'
            fout = open('founddlxs.txt', 'a')
            fout.write(callno + ' has an EAD' + '\n\n')
            fout.close()
        else:
            print callno + ' does not have an EAD'
