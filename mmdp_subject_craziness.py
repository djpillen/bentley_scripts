from lxml import etree
import os
from os.path import join

original_eads = 'C:/Users/Public/Documents/Master_20150504-Original_EADs'
demo_eads = 'C:/Users/djpillen/GitHub/mmdp-workshop/EADs'

subject_list = []

for filename in os.listdir(original_eads):
    tree = etree.parse(join(original_eads,filename))
    subjects = tree.xpath('//controlaccess/subject')
    for subject in subjects:
        if subject.text is not None:
            subject_list.append(subject.text)

    print filename

subject_count = len(subject_list)
demo_ead_count = len(os.listdir(demo_eads)) + 1

dispersion = subject_count / demo_ead_count

for filename in os.listdir(demo_eads):
    print "Adding {0} subjects to {1}".format(dispersion, filename)
    tree = etree.parse(join(demo_eads,filename))
    controlaccess = tree.xpath('//controlaccess')[0]
    new_controlaccess = etree.Element('controlaccess')
    header = etree.SubElement(new_controlaccess,'head')
    header.text = 'Demo Subjects'
    for i in range(dispersion):
        new_subject = etree.Element('subject')
        new_subject.text = subject_list[i]
        new_subject.attrib['source'] = 'local'
        new_controlaccess.append(new_subject)
        subject_list.pop(i)
    controlaccess.append(new_controlaccess)
    with open(join(demo_eads,filename),'w') as ead_out:
        ead_out.write(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))
