import csv
import os
from os.path import join
from lxml import etree


subject_terms_csv = 'C:/Users/Public/Documents/subject_terms_clustered.csv'
path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
test_path = 'C:/Users/djpillen/GitHub/test_dir'

to_update = {}

print 'Building dictionary...'
with open(subject_terms_csv, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader,None)
    for row in reader:
        original = row[0]
        updated = row[1]
        if original != updated:
            print original, updated
            if original not in to_update:
                to_update[original] = updated

tags = ['subject', 'geogname']

print 'Processing EADs...'
for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    for sub in tree.xpath('//controlaccess/*'):
        if sub.tag in tags and sub.text is not None and '--' in sub.text:
            terms = sub.text.split('--')
            match_terms = 0
            updated_terms = []
            for term in terms:
                if (terms.index(term) == len(terms) - 1) and term.endswith('.') and (term.strip('.') in to_update or term in to_update):
                    if term.strip('.') in to_update and term == to_update[term.strip('.')]:
                        updated_terms.append(term)
                    elif term in to_update and term.strip('.') == to_update[term]:
                        updated_terms.append(term)
                    else:
                        if term.strip('.') in to_update:
                            new_term = to_update[term.strip('.')]
                            if new_term.endswith('.'):
                                updated_terms.append(new_term)
                                match_terms += 1
                            else:
                                updated_terms.append(new_term + '.')
                                match_terms += 1
                        elif term in to_update and to_update[term].endswith('.'):
                            new_term = to_update[term]
                            updated_terms.append(new_term)
                            match_terms += 1
                        else:
                            new_term = to_update[term] + '.'
                            updated_terms.append(new_term)
                            match_terms += 1
                elif term in to_update:
                    new_term = to_update[term]
                    updated_terms.append(new_term)
                    match_terms += 1
                else:
                    updated_terms.append(term)
            if match_terms > 0:
                new_subject = '--'.join(updated_terms)
                print sub.text + ':' + new_subject
                sub.text = new_subject
    with open(join(path,filename),'w') as ead_out:
        ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True, pretty_print=True))
