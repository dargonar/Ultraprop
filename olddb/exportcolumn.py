import csv

csvreader = csv.reader(open('temp.csv', 'rb'), delimiter=',', quotechar='"')
fff = []
for row in csvreader:
     #fff.append(row[20])
     print row[3] + '\n'