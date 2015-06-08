import csv


def parse():
    with open("orderlist.csv") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'T':
                print "type:" + row[0] + " qty:" + row[3] + " price:" + row[4]