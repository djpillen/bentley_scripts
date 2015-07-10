import os
from os.path import join

path = 'C:/Users/Public/Documents/spec_coll_ead_problem'
outFilePath = 'C:/Users/Public/Documents/spec_coll_ead_utf8'
for filename in os.listdir(path):
    start = open(join(path, filename), 'r')
    finish = open(join(outFilePath, filename), 'w')
    for i in start:
        finish.write(i.encode('utf-8'))
    finish.close()
    print filename
