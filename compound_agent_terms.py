import csv
from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/without-reservations/Real_Masters_all'

compound_agent_terms = 'C:/Users/djpillen/GitHub/test_run/subjects/compound_agents_terms.csv'

term_type_dict = {}

tags = ['corpname','persname','famname']

with open (compound_agent_terms,'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        row_index = len(row) - 1
        index = 1
        agent = row[0]
        term_type_dict[agent] = {}
        while index < row_index:
            term = row[index]
            term_type = row[index+1]
            term_type_dict[agent][term] = term_type
            index += 2

for filename in os.listdir(path):
    print filename
    tree = etree.parse(join(path,filename))
    for agent in tree.xpath('//controlaccess/*'):
        if agent.tag in tags:
            agent_text = agent.text
            if '---' in agent_text:
                agent_text = agent_text.replace('---','- --')
            if agent_text in term_type_dict:
                for term in term_type_dict[agent_text]:
                    new_term = etree.Element('term')
                    new_term.text = term
                    new_term.attrib['type'] = term_type_dict[agent_text][term]
                    agent.append(new_term)
    with open(join(path,filename),'w') as ead_out:
        ead_out.write(etree.tostring(tree,xml_declaration=True,encoding='utf-8'))
