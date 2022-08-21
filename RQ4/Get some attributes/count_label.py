#!/usr/bin/python3
import csv
from cmath import sin
import re
import pymysql
from regex import E, F


file1 = open("GFI_mentor/RQ4/all_issue_cbn.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)

file2 = open("GFI_mentor/RQ4/issue_labels.csv", "w")
csv_writer = csv.writer(file2)
csv_writer.writerow(['issue_id', 'labels'])

db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')

for row in csv_reader:
    try:
        cursor = db.cursor()
        sql = "select count(*) as labels from issue_labels where issue_id = %s"%(row[0])
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        csv_writer.writerow([row[0], results[0][0]])
    except:
        print("Error: unable to fetch repo")