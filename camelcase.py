import os
from os.path import join

path = 'C:/Users/Public/Documents/test_ead-3'
outFilePath = 'C:/Users/Public/Documents/camelcase'
for filename in os.listdir(path):
    start = open(join(path, filename), 'r')
    finish = open(join(outFilePath, filename), 'w')
    for i in start:
        finish.write(i.replace('actuate="onrequest"', 'actuate="onRequest"').replace('actuate="onload"', 'actuate="onLoad"'))
    finish.close()
    print filename
