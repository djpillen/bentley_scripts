from lxml import etree
import os
from os.path import join
import re

ead_path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
marc_path = 'C:/Users/Public/Documents/marc_xml-has_ead-split'

ead_ids = {}
marc_ids = {}
master_dict = {}

def get_ead_ids():
    for filename in os.listdir(ead_path):
        tree = etree.parse(join(ead_path,filename))
        ead_id = tree.xpath('//eadid')[0]
        ead_id = ead_id.text.split('-')[-1]
        #if ead_id not in ead_ids:
            #ead_ids[ead_id] = []
        if ead_id not in master_dict:
            master_dict[ead_id] = {}
        if 'EAD' not in master_dict[ead_id]:
            master_dict[ead_id]['EAD'] = []
        #ead_ids[ead_id].append(filename)
        master_dict[ead_id]['EAD'].append(filename)
        #print ead_id

def get_marc_ids():
    #total_files = 0
    #has_856 = 0
    #no_856 = []
    #ead_ids = {}
    #has_ead = 0
    #only_numbers = re.compile('^\d+$')
    for filename in os.listdir(marc_path):
        #total_files += 1
        tree = etree.parse(join(marc_path, filename))
        ead_path = tree.xpath('//marc:datafield[@tag="856"]/marc:subfield[@code="u"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
        if ead_path:
            ead_id = ead_path[0].text.split('-')[-1]
            #if ead_id not in marc_ids:
                #marc_ids[ead_id] = []
            if ead_id not in master_dict:
                master_dict[ead_id] = {}
            if 'MARC' not in master_dict[ead_id]:
                master_dict[ead_id]['MARC'] = []
            #marc_ids[ead_id].append(filename)
            master_dict[ead_id]['MARC'].append(filename)
            #if not ead_path[0].text.startswith('http://quod.lib.umich.edu/cgi/f/findaid'):
                #print filename, ead_path[0].text
                #os.remove(join(marc_path,filename))
            #else:
                #has_ead += 1
            #has_856 += 1
        #else:
            #no_856.append(filename)
    #print 'Total files:',total_files
    #print 'Has 856:',has_856
    #if no_856:
        #print 'No 856:',no_856
    #print 'EADs:',has_ead

get_marc_ids()
get_ead_ids()

'''
counts = {}

for ead_id in marc_ids:
    if len(marc_ids[ead_id]) not in counts:
        counts[len(marc_ids[ead_id])] = 1
    else:
        counts[len(marc_ids[ead_id])] += 1
    if len(marc_ids[ead_id]) > 5:
        print ead_id, marc_ids[ead_id]

print counts

for ead_id in ead_ids:
    if len(ead_ids[ead_id]) > 1:
        print ead_id, eads_ids[ead_id]
'''

only_eads = 0
only_marc = 0
for ead_id in master_dict:
    if 'EAD' and not 'MARC' in master_dict[ead_id]:
        only_eads += 1
        print ead_id, master_dict[ead_id]
    if 'MARC' and not 'EAD' in master_dict[ead_id]:
        only_marc += 1
        print ead_id, master_dict[ead_id]
print 'Only EADs:',only_eads
print 'Only MARC:',only_marc
