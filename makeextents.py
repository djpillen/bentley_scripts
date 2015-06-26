import csv

with open('makeextents.csv', 'rb') as file:
    reader = csv.reader(file)
    next(reader, None)
    for row in reader:
        
        n1 = 3
        n2 = 6
        extents = row[n1..n6]
        
        number = row[3]
        filename = row[0]
        xpath = row[1]
        #expression = row[2]
        normalized = row[3]
        print filename + ' ' + normalized
        try:
            file = open(join(path, filename))
            tree = etree.parse(file)
            date = tree.xpath(xpath)
            #date[0].text = expression
            date[0].attrib['normal'] = normalized
            outfile = open(join(path, filename), 'w')
            outfile.write(etree.tostring(tree, encoding="utf-8", xml_declaration=True))
            outfile.close()
            print 'success!'
        except:
            outfile = open('accessrestrictdateerrors.txt','a')
            outfile.write(filename + ' ' + normalized)
            outfile.close()
            print 'oops!'
            
        
print "accessrestrictdate-normal-2 Complete"



l = [1,2,3,4....16]
zip(l,l[3:])[::4]

r = range(3,100)
four = zip(r,r[3:])[::4]
for group in four:
    rows = range(group[0],group[1]+1)
    number = r[0]
    type = r[1]
    portion = r[2]
    summary = r[3]
    