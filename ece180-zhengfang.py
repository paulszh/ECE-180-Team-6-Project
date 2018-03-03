#!/usr/bin/env python
#_*_coding:utf-8_*_
import csv
with open('C:\Users\lalal\Desktop\document\ucsd\ece180\Price to Rent Ratio All.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    rows = [row for row in reader]
    month = rows[0]
    months = month[-12:]
    print months
with open('C:\Users\lalal\Desktop\document\ucsd\ece180\Price to Rent Ratio All.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for i, rows in enumerate(reader):
        if i == 11:
            row = rows
            specific_value_2017 = row[-12:]
            specific_value_2016 = row[-24:-12]
    print specific_value_2017
    print specific_value_2016
import numpy as np
import matplotlib.pyplot as plt
plt.xticks(range(len(months)),months)
plt.plot(specific_value_2017)
'''
plt.xlable("time")
plt.ylable("price to rent ratio")
plt.title("2017 La Jolla Price To Rent Ratio")
'''
plt.show()