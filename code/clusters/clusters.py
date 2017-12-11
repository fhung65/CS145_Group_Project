import csv

d = {}

for x in csv.reader(open('cmu_cluster.txt'), delimiter='\t'):
    key = int(x[0])
    if key in d:
        d[key].append(x[1])
    else:
        d[key] = [x[1]]
