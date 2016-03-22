from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

agent_tags = ['corpname','persname','famname']
subject_tags = ['subject','geogname','genreform']

agents_and_subjects_dict = {}
for filename in os.listdir(path):
	print "Building agents and subjects dict from {}".format(filename)
	tree = etree.parse(join(path,filename))
	agents = []
	for agent_tag in agent_tags:
		agents.extend(tree.xpath("//controlaccess/{}".format(agent_tag)))
	subjects = []
	for subject_tag in subject_tags:
		subjects.extend(tree.xpath("//controlaccess/{}".format(subject_tag)))
	for agent in agents:
		agent_text = agent.text.strip().rstrip(".").encode('utf-8').split('--')[0]
		if agent_text not in agents_and_subjects_dict:
			agents_and_subjects_dict[agent_text] = {"agents":{},"subjects":{}}
		agents_and_subjects_dict[agent_text]["agents"][agent.tag] = agents_and_subjects_dict[agent_text]["agents"].get(agent.tag,0)+1
	for subject in subjects:
		subject_text = subject.text.strip().rstrip(".").encode('utf-8').split('--')[0]
		if subject_text not in agents_and_subjects_dict:
			agents_and_subjects_dict[subject_text] = {"agents":{},"subjects":{}}
		agents_and_subjects_dict[subject_text]["subjects"][subject.tag] = agents_and_subjects_dict[subject_text]["subjects"].get(subject.tag,0)+1

print "Looking for agents or subjects with conflicting tag types"
for agent_or_subject in agents_and_subjects_dict:
	for key, value in agents_and_subjects_dict[agent_or_subject].items():
		if not agents_and_subjects_dict[agent_or_subject][key]:
			del agents_and_subjects_dict[agent_or_subject][key]
for agent_or_subject in agents_and_subjects_dict:
	keys = agents_and_subjects_dict[agent_or_subject]
	if len(keys) > 1:
		print "{0}: {1}".format(agent_or_subject, agents_and_subjects_dict[agent_or_subject])
		print "\n"
