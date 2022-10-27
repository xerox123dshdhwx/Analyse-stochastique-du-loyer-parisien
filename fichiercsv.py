import csv
d = {}
with open('logement-encadrement-des-loyers (1).csv', mode='r') as f:
    data = csv.reader(f)
    d = {rows[0]:rows[1] for rows in data}
    print(d)