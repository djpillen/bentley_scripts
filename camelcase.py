import os
from os.path import join

path = 'C:/Users/Public/Documents/aspace_migration/retry_eads'
outFilePath = 'C:/Users/Public/Documents/aspace_migration/retry_eads'
for filename in os.listdir(path):
    start = open(join(path, filename), 'r')
    finish = open(join(outFilePath, filename), 'w')
    for i in start:
        finish.write(i.replace('actuate="onrequest"', 'actuate="onRequest"').replace('actuate="onload"', 'actuate="onLoad"'))
    start.close()
    finish.close()
    print filename
