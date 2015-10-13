import csv
from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

agent_dict = {}
agent_tags = ['corpname','persname']

for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    file_agents = []
    origination = tree.xpath('//origination')
    controlaccess = tree.xpath('//controlaccess')
    eadid = tree.xpath('//eadid')[0].text
    for origin in origination:
        for agent in origin.xpath('.//*'):
            if agent.tag in agent_tags:
                agent_text = agent.text.encode('utf-8')
                if agent_text not in file_agents:
                    if agent_text not in agent_dict:
                        agent_dict[agent_text] = {}
                    if 'originator' not in agent_dict[agent_text]:
                        agent_dict[agent_text]['originator'] = []
                    if 'count' not in agent_dict[agent_text]:
                        agent_dict[agent_text]['count'] = 0
                    agent_dict[agent_text]['count'] += 1
                    agent_dict[agent_text]['originator'].append(eadid)
                    file_agents.append(agent_text)
    for control in controlaccess:
        for agent in control.xpath('.//*'):
            if agent.tag in agent_tags:
                agent_text = agent.text.encode('utf-8')
                if agent_text not in file_agents:
                    if agent_text not in agent_dict:
                        agent_dict[agent_text] = {}
                    if 'subject' not in agent_dict[agent_text]:
                        agent_dict[agent_text]['subject'] = []
                    if 'count' not in agent_dict[agent_text]:
                        agent_dict[agent_text]['count'] = 0
                    agent_dict[agent_text]['count'] += 1
                    agent_dict[agent_text]['subject'].append(eadid)
                    file_agents.append(agent_text)
    print filename

print agent_dict
