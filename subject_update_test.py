subjects = ['Dallas--J.--Pillen.','Harry--Potter.','Cheese--Sand wich.']
to_update = {'J.':'John','Pillen':'Nellip','Sand wich':'Sandwich'}
new_subjects = []


for subject in subjects:
    terms = subject.split('--')
    match_terms = 0
    updated_terms = []
    for term in terms:
        if (terms.index(term) == len(terms) - 1) and term.endswith('.') and term.strip('.') in to_update:
            term = term.strip('.')
            term = to_update[term] + '.'
            match_terms += 1
        elif term in to_update:
            term = to_update[term]
            match_terms += 1
        updated_terms.append(term)
    if match_terms > 0:
        new_subject = '--'.join(updated_terms)
        new_subjects.append(new_subject)

print new_subjects
