from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/marc_xml-all/marc_xml-all-split'

agent_fields = ['610','611','600']

subdivided_agents = []
for filename in os.listdir(path):
	print "Checking for subdivided agents in {0}".format(filename)
	tree = etree.parse(join(path,filename))
	for agent_field in agent_fields:
		agents = tree.xpath('//marc:datafield[@tag="'+agent_field+'"]//marc:subfield[@code="a"]', namespaces={'marc': 'http://www.loc.gov/MARC21/slim'})
		for agent in agents:
			agent_text = agent.text.strip().encode('utf-8')
			if '--' in agent_text:
				if agent_text not in subdivided_agents:
					subdivided_agents.append(agent_text)

print subdivided_agents
