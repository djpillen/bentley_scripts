import os
from os.path import join

start_path = 'C:/Users/djpillen/GitHub/vandura/Real_Masters_all/'
end_path = 'C:/Users/Public/Documents/camelcase/'

filenames = []

with open('C:/Users/Public/Documents/eadtojsonerrors.txt','r') as errors:
    for filename in errors:
        filename = filename.replace('\n','')
        filename = filename
        filenames.append(filename)
        
print filenames

for filename in filenames:
        start_file = open(start_path + filename)
        start_file = start_file.read()
        end_file = open(end_path + filename,'w')
        end_file.write(start_file)
        end_file.close()
        print filename