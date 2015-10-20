from lxml import etree
import os
from os.path import join


path = 'C:/Users/djpillen/GitHub/test_dir/eads'


callnumbers = {}


for filename in os.listdir(path):
    print 'checking call numbers in ' + filename
    tree = etree.parse(join(path, filename))
    callnumber = tree.xpath('//archdesc/did/unitid')[0].text.encode('utf-8')
    if callnumber not in callnumbers:
        callnumbers[callnumber] = {}
        callnumbers[callnumber]['count'] = 0
        callnumbers[callnumber]['files'] = []
    callnumbers[callnumber]['count'] += 1
    callnumbers[callnumber]['files'].append(filename)

for callnumber in callnumbers:
    if callnumbers[callnumber]['count'] > 1:
        replaced = 0
        total = callnumbers[callnumber]['count']
        while replaced < total:
            for ead in callnumbers[callnumber]['files']:
                with open(join(path,ead),'r') as ead_in:
                    ead_in = ead_in.read()
                    print "amending duplicate call number in " + ead
                    ead_out = open(join(path,ead),'w')
                    ead_out.write(ead_in.replace(callnumber,callnumber + ' ' + str(replaced)))
                    ead_out.close()
                    replaced += 1
