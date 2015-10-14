"""
Check for EADs that start container numbering again in new series, subgrps, etc.
So like each subgroup has a "Box 1" but those containers are really different things
Might be tricky
"""

from lxml import etree
import os
from os.path import join
import re



path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
count = 1
for filename in os.listdir(path):
    max_box = 0
    tree = etree.parse(join(path,filename))
    physdescs = tree.xpath('//physdesc')
    extents = physdescs[0].xpath('./extent')
    if len(extents) > 1:
        con_sum = extents[1].text
        if 'box' in con_sum:
            box_nums = re.findall(r'([\d\.]+)',con_sum)
            box_nums = box_nums[0]
    else:
        if 'linear feet' in extents[0].text or 'box' in extents[0].text or 'linear foot' in extents[0].text:
            box_nums = re.findall(r'([\d\.]+)',extents[0].text)
            box_nums = box_nums[0]
    components = tree.xpath("//dsc//*[starts-with(local-name(), 'c0')]")
    for component in components:
        containers = component.xpath('./did/container')
        if containers:
            container = containers[0]
            if container.attrib['type'] == 'box':
                try:
                    box_num = int(container.text)
                    if box_num > max_box:
                        max_box = box_num
                except:
                    continue

    if box_nums and max_box > 0:
        if '.' in box_nums:
            box_nums = float(box_nums)
            box_nums = int(round(box_nums + 0.5))
        else:
            box_nums = int(box_nums)
        difference = abs(max_box - box_nums)

        if difference > 1:
            print count, filename, box_nums, max_box, difference
            count += 1
    box_nums = None

'''
path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'
subgrps = []
for filename in os.listdir(path):
    tree = etree.parse(join(path,filename))
    top_levels = tree.xpath("//c01")
    for top_level in top_levels:
        if top_level.attrib['level'] == 'subgrp':
            if filename not in subgrps:
                subgrps.append(filename)

print subgrps
'''
