#!/usr/bin/python3
import csv
from cmath import sin
import imp
import re
import pymysql
from regex import E, F
import os

file1 = open("GFI_mentor/RQ4/repo_urls.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)

i = 0
count = 0
for row in csv_reader:
    print(i)
    cmd = 'git clone ' + row[1]
    os.system(cmd)
    i+=1
