import csv
from sets import Set
from collections import Counter
import nltk
#import matplotlib

file = open('C:/Users/Public/Documents/subjects.csv')
reader = csv.reader(file)

subjects = []

for row in reader:
    subjects.append(row[2])
    
print 'Total subjects: ' + str(len(subjects))
print 'Unique subjects: ' + str(len(Set(subjects)))

words_to_count = (word for word in subjects if word[:1])
c = Counter(words_to_count)
print 'Top ten subjects: ' + str(c.most_common(10))

fdist = nltk.FreqDist(subjects)
print fdist
print fdist.max()
#fdist.plot(50)


