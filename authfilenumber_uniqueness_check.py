from lxml import etree
import os
from os.path import join

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

authfilenumber_to_text_dict = {}
authfilenumber_to_tags = {}
text_to_authfilenumber_dict = {}

tags = ['subject','corpname','persname','famname','geogname','genreform']

'''
print "Building text to authfilenumber dict"
for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	for subject in tree.xpath('//controlaccess/*'):
		if subject.tag in tags and subject.text:
			subject_text = subject.text.encode('utf-8')
			if 'authfilenumber' in subject.attrib:
				authfilenumber = subject.attrib['authfilenumber']
				if subject_text not in text_to_authfilenumber_dict:
					text_to_authfilenumber_dict[subject_text] = authfilenumber

print "Applying authfilenumbers where appropriate"
for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	for subject in tree.xpath('//controlaccess/*'):
		if subject.tag in tags and subject.text:
			subject_text = subject.text.encode('utf-8')
			if subject_text in text_to_authfilenumber_dict and 'authfilenumber' not in subject.attrib:
				subject.attrib['authfilenumber'] = text_to_authfilenumber_dict[subject_text]

	with open(join(path,filename),'w') as ead_out:
		ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
'''

special_cases = ['University of Michigan--Dearborn','University of Michigan--Flint','University of Michigan--Dearborn. Department of History','University of Wisconsin--Milwaukee','Lutheran Church--Missouri Synod']

for filename in os.listdir(path):
	tree = etree.parse(join(path,filename))
	for subject in tree.xpath('//controlaccess/*'):
		if subject.tag in tags and subject.text:
			subject_text = subject.text.strip().rstrip(".").encode('utf-8')
			if subject.tag in ['corpname','persname','famname'] and '--' in subject_text:
				subject_texts = subject_text.split('--')
				joined = '--'.join(subject_texts[0:2]).rstrip(".")
				if joined in special_cases:
					subject_text = joined
				else:
					subject_text = subject_texts[0]
			if 'authfilenumber' in subject.attrib:
				authfilenumber = subject.attrib['authfilenumber']
				if authfilenumber not in authfilenumber_to_text_dict:
					authfilenumber_to_text_dict[authfilenumber] = []
				if subject_text not in authfilenumber_to_text_dict[authfilenumber]:
					authfilenumber_to_text_dict[authfilenumber].append(subject_text)
				if subject_text not in text_to_authfilenumber_dict:
					text_to_authfilenumber_dict[subject_text] = []
				if authfilenumber not in text_to_authfilenumber_dict[subject_text]:
					text_to_authfilenumber_dict[subject_text].append(authfilenumber)
				if authfilenumber not in authfilenumber_to_tags:
					authfilenumber_to_tags[authfilenumber] = []
				if subject.tag not in authfilenumber_to_tags[authfilenumber]:
					authfilenumber_to_tags[authfilenumber].append(subject.tag)
			else:
				authfilenumber = ''
				if subject_text not in text_to_authfilenumber_dict:
					text_to_authfilenumber_dict[subject_text] = []
				if authfilenumber not in text_to_authfilenumber_dict[subject_text]:
					text_to_authfilenumber_dict[subject_text].append(authfilenumber)

print "*** AUTHFILENUMBER TO TEXT ***"
for authfilenumber in authfilenumber_to_text_dict:
	if len(authfilenumber_to_text_dict[authfilenumber]) > 1:
		print "{0}: {1}".format(authfilenumber,authfilenumber_to_text_dict[authfilenumber])

print "\n\n"

authfilenumbers_to_add = {}
print "*** TEXT TO AUTHFILENUMBER ***"
for subject_text in text_to_authfilenumber_dict:
	if len(text_to_authfilenumber_dict[subject_text]) > 1:
		print "{0}: {1}".format(subject_text, text_to_authfilenumber_dict[subject_text])

		if len(text_to_authfilenumber_dict[subject_text]) == 2:
			if '' in text_to_authfilenumber_dict[subject_text]:
				authfilenumber = [authfilenumber for authfilenumber in text_to_authfilenumber_dict[subject_text] if len(authfilenumber) > 1][0]
				authfilenumbers_to_add[subject_text] = authfilenumber

print "\n\n"

print "*** AUTHFILENUMBER TO TAGS ***"
for authfilenumber in authfilenumber_to_tags:
	if len(authfilenumber_to_tags[authfilenumber]) > 1:
		print "{0} - {1}: {2}".format(authfilenumber,authfilenumber_to_text_dict[authfilenumber][0],authfilenumber_to_tags[authfilenumber])

add_authfilenumbers = raw_input("Add authfilenumbers based on the results of TEXT TO AUTHFILENUMBERS?: ")

if authfilenumbers_to_add:
	if add_authfilenumbers.lower() == 'y':
		for filename in os.listdir(path):
			print filename
			tree = etree.parse(join(path,filename))
			for subject in tree.xpath('//controlaccess/*'):
				if subject.text:
					subject_text = subject.text.encode('utf-8')
					if subject_text in authfilenumbers_to_add and not 'authfilenumber' in subject.attrib:
						subject.attrib['authfilenumber'] = authfilenumbers_to_add[subject_text]
			with open(join(path,filename),'w') as f:
				f.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
