import csv

with open('C:/Users/Public/Documents/normalattributes-9_split.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader, None)
    for row in reader:
        filename = row[0]
        xpath = row[1]
        begin = row[2]
        end = row[3]
        if len(begin) is not 0 and len(end) is not 0:
            if begin > end:
                with open('C:/Users/Public/Documents/dates_begin_after_end-5.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile, dialect='excel')
                    writer.writerow([filename, xpath, begin, end])
        print filename
