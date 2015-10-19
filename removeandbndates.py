import os
from os.path import join
import re

path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all'

for filename in os.listdir(path):
    print filename
    start = open(join(path, filename), 'r').read()
    finish = open(join(path, filename), 'w')
    replaced = re.sub(r'</unitdate>\s?and\s?<unitdate',r'</unitdate>, <unitdate',start)
    finish.write(replaced)
    finish.close()
