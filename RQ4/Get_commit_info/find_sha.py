#!/usr/bin/python3
import csv
from cmath import sin
import re
import pymysql
from regex import E, F

file1 = open("GFI_mentor/GFI_selection/GFI_closed.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)

file2 = open("GFI_mentor/RQ4/all_sha.csv", "w")
csv_writer = csv.writer(file2)
csv_writer.writerow(['issue_id', 'actor_id', 'repo_id', 'created_at', 'sha'])

db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')

for row in csv_reader:
    try:
        cursor = db.cursor()
        sql = "SELECT action_specific, actor_id, created_at from issue_events where issue_id = %s and action = 'closed' and action_specific <> 'NULL'"%(row[0])
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        csv_writer.writerow([row[0],results[0][1],row[1],results[0][2],results[0][0]])
    except:
        print("Error: unable to fetch issue")
