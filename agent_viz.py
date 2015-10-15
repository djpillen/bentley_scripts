import csv
from lxml import etree
import os
from os.path import join
import json

path = 'C:/Users/Dallas/Documents/GitHub/vandura/Real_Masters_all'

subject_dict = {}
eadid_dict = {}
relationships = {}
tags = ['corpname','persname','famname','subject','geogname']

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    file_subjects = []
    origination = tree.xpath('//origination')
    controlaccess = tree.xpath('//controlaccess')
    eadid = tree.xpath('//eadid')[0].text.strip()
    eadid_dict[eadid] = []
    for origin in origination:
        for agent in origin.xpath('.//*'):
            if agent.tag in tags:
                agent_text = agent.text.encode('utf-8')
                if agent_text not in file_subjects:
                    if agent_text not in subject_dict:
                        subject_dict[agent_text] = []
                    subject_dict[agent_text].append(eadid)
                    eadid_dict[eadid].append(agent_text)
                    file_subjects.append(agent_text)
    for control in controlaccess:
        for subject in control.xpath('.//*'):
            if subject.tag in tags:
                subject_text = subject.text.encode('utf-8')
                if subject_text not in file_subjects:
                    if subject_text not in subject_dict:
                        subject_dict[subject_text] = []
                    subject_dict[subject_text].append(eadid)
                    eadid_dict[eadid].append(subject_text)
                    file_subjects.append(subject_text)
    print filename

for eadid in eadid_dict:
    relationships[eadid] = {}
    for subject in eadid_dict[eadid]:
        for ead in subject_dict[subject]:
            if ead != eadid:
                if ead not in relationships[eadid]:
				    relationships[eadid][ead] = []
                relationships[eadid][ead].append(subject)
                    #relationships[eadid][ead] = 0
                #relationships[eadid][ead] += 1
        #related = [ead for ead in subject_dict[subject]]
        #relationships[eadid].extend([ead for ead in related if ead != eadid and ead not in relationships[eadid]])

'''
testid = 'umich-bhl-2015029'


data['nodes'].append({'name':testid})
count = 1
for ead in relationships[testid]:
    data['nodes'].append({'name':ead})
    data['links'].append({'source':0,'target':count,'weight':relationships[testid][ead]})
    count += 1
'''

'''
data = {'nodes':[],'links':[]}
appended = []
'''

for eadid in relationships:
	data = {'nodes':[],'links':[]}
	appended = []
	if eadid not in appended:
		data['nodes'].append({'name':eadid,'group':10})
		appended.append(eadid)
	for ead in relationships[eadid]:
		if ead not in appended:
			data['nodes'].append({'name':ead,'group':len(relationships[eadid][ead]),'subjects':'; '.join(relationships[eadid][ead])})
			appended.append(ead)
		data['links'].append({'source':appended.index(eadid),'target':appended.index(ead),'value':len(relationships[eadid][ead])})
		#for value in relationships[ead]:
		#	if value not in appended:
		#		data['nodes'].append({'name':value,'group':1})
		#		appended.append(value)
		#	data['links'].append({'source':appended.index(ead),'target':appended.index(value),'value':relationships[ead][value]})
		'''
	checked = []
	checked.append(eadid)
	for value in appended:
		if value != eadid:
			for other in appended:
				if other != value and other not in checked:
					if other in relationships[value]:
						data['links'].append({'source':appended.index(value),'target':appended.index(other),'value':relationships[value][other]})
		checked.append(value)
		'''

	with open('C:/Users/Dallas/Documents/projects/relationships/' + eadid + '.json','w') as outfile:
		outfile.write(json.dumps(data))
'''
for link in data['links']:
    if link['weight'] > 1:
        print link
'''
