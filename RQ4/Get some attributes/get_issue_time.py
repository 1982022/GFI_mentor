#!/usr/bin/python3
import csv
from cmath import sin
import re
import pymysql
from regex import E, F


file1 = open("GFI_mentor/RQ4/all_issue_cbn.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)

file2 = open("GFI_mentor/RQ4/issue_time.csv", "w")
csv_writer = csv.writer(file2)
csv_writer.writerow(['issue_id', 'issue_time'])

db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')

for row in csv_reader:
    try:
        cursor = db.cursor()
        sql = "select created_at from issue_events where issue_id = '%s' and action = 'closed'"%(row[0])
        cursor.execute(sql)
        results1 = cursor.fetchall()
        sql2 = "select created_at from issues where id = '%s'"%(row[0])
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        cursor.close()
        issue_time = (results1[0][0] - results2[0][0]).total_seconds()/2626560
        csv_writer.writerow([row[0], issue_time])
    except:
        print("Error: unable to fetch repo")