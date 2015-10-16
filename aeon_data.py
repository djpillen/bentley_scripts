from lxml import etree
import re
import os
from os.path import join
import json
import re
import csv
import math

'''
# Build and save a list of EAD call numbers
ead_path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
eads = []

for filename in os.listdir(ead_path):
    print filename
    tree = etree.parse(join(ead_path,filename))
    call_number = tree.xpath('//archdesc/did/unitid')[0].text.encode('utf-8').strip()
    eads.append(call_number)

with open('C:/Users/Public/Documents/aeon/eads.txt','a') as ead_list:
    ead_list.write('\n'.join(eads))
'''

ead_path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
tags = ['subject','geogname']

minimum_requests = 25

aeon_data = 'C:/Users/Public/Documents/aeon/circulation_20151016.xml'
ead_file = open('C:/Users/Public/Documents/aeon/eads.txt','r').read()
ead_list = []
for ead in ead_file.splitlines():
    ead_list.append(ead)


# Parse Aeon Transactions
eads = {}
titles = {}

ns = {'aeon':'Transaction_x0020_Report_x0020_-_x0020_Frequency_x0020_of_x0020_Circulation_x0020__x0028_no_x0020_staff_x0029_'}
tree = etree.parse(aeon_data)
transactions = tree.xpath('//aeon:TransactionsGroup',namespaces=ns)

for transaction in transactions:
    title_number = transaction.attrib['CallNumber'].encode('utf-8').split('\n')
    frequency = transaction.attrib['Transactions_TransactionNumber']
    if len(title_number) > 1:
        call_number = title_number[1]
        if call_number in ead_list:
            if int(frequency) > minimum_requests:
                eads[call_number] = {}
                eads[call_number]['frequency'] = int(frequency)
                eads[call_number]['subjects'] = []


for filename in os.listdir(ead_path):
    tree = etree.parse(join(ead_path,filename))
    call_number = tree.xpath('//archdesc/did/unitid')[0].text.encode('utf-8').strip()
    coll_title = tree.xpath('//unittitle')[0]
    coll_title = re.sub(r'<(.*?)>','',etree.tostring(coll_title))
    if call_number in eads:
        titles[call_number] = coll_title.encode('utf-8').strip()
        controlaccesses = tree.xpath('//controlaccess')
        for controlaccess in controlaccesses:
            for subject in controlaccess.xpath('./*'):
                if subject.tag in tags:
                    subject_text = subject.text.encode('utf-8')
                    if subject_text not in eads[call_number]['subjects']:
                        eads[call_number]['subjects'].append(subject_text)

subjects = {}
for ead in eads:
    for subject in eads[ead]['subjects']:
        if subject not in subjects:
            subjects[subject] = {}
            subjects[subject]['count'] = eads[ead]['frequency']
            subjects[subject]['eads'] = [ead]
            subjects[subject]['titles'] = [titles[ead]]
        else:
            subjects[subject]['count'] += eads[ead]['frequency']
            subjects[subject]['eads'].append(ead)
            subjects[subject]['titles'].append(titles[ead])

for subject in subjects:
    weighted = subjects[subject]['count'] * len(subjects[subject]['eads'])
    subjects[subject]['weight'] = math.sqrt(weighted)


data = {'nodes':[],'links':[]}
appended = []
checked = []
for subject in subjects:
    if subject not in appended:
        data['nodes'].append({'name':subject,'group':int(subjects[subject]['weight']),'eads':'--'.join(subjects[subject]['titles'])})
        appended.append(subject)

for subject in appended:
    for ead in subjects[subject]['eads']:
        for other_subject in eads[ead]['subjects']:
            if other_subject != subject and other_subject not in checked:
                data['links'].append({'source':appended.index(subject),'target':appended.index(other_subject),'value':1})
    checked.append(subject)

with open('C:/Users/djpillen/GitHub/test_dir/aeon_data/relationships.json','w') as outfile:
    outfile.write(json.dumps(data))


'''
with open('C:/Users/Public/Documents/aeon/aeon_most_popular_subjects.csv','ab') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Subject','Total Requested Collections','Total Requests','Score','Requested Collections'])
for subject in subjects:

    with open('C:/Users/Public/Documents/aeon/aeon_most_popular_subjects.csv','ab') as csvfile:
        writer = csv.writer(csvfile)
        row = []
        row.append(subject)
        row.append(len(subjects[subject]['eads']))
        row.append(subjects[subject]['count'])
        row.append(subjects[subject]['weight'])
        subject_eads = {}
        for ead in subjects[subject]['eads']:
            subject_eads[titles[ead]] = eads[ead]['frequency']
        sorted_eads = sorted(subject_eads,key=subject_eads.get,reverse=True)
        for ead in sorted_eads:
            row.append(ead)
            row.append(subject_eads[ead])
        writer.writerow(row)
            #writer.writerow([subject, len(subjects[subject]['eads']), subjects[subject]['count'],subjects[subject]['weight']])
'''
