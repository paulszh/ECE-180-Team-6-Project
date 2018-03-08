#!/usr/bin/env python
# _*_coding:utf-8_*_
import csv

with open('C:\Users\lalal\Desktop\document\ucsd\ece180\Price to Rent Ratio All.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]
    month = rows[0]
    time = month[10:]
    print time
with open('C:\Users\lalal\Desktop\document\ucsd\ece180\Price to Rent Ratio All.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for i, rows in enumerate(reader):
        if i == 11:
            row = rows
            id92122 = row[10:]
    print id92122
with open('C:\Users\lalal\Desktop\document\ucsd\ece180\Price to Rent Ratio All.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for i, rows in enumerate(reader):
        if i == 20:
            row = rows
            id92037 = row[10:]
    print id92037
import numpy as np
import matplotlib.pyplot as plt

year = [2011,2012,2013,2014,2015,2016,2017]
i = 0
ave_92122 = []
ave_92037 = []
id92122 = map(float, id92122)
id92037 = map(float, id92037)
while i < len(time):
    sum92122 = sum(id92122[i:i+12])
    sum92037 = sum(id92037[i:i+12])
    ave92122 = sum92122/12.
    ave92037 = sum92037/12.
    i = i+12
    ave_92122.append(ave92122)
    ave_92037.append(ave92037)
print ave_92122
print ave_92037
plt.xticks(range(len(year)), year)
plt.plot(ave_92122,label="id92122")
plt.plot(ave_92037,label='id92037')
plt.xticks(rotation=45)
plt.show()
