#!/usr/bin/python3
import csv
from cmath import sin
import re
import pymysql
from regex import E, F

def judge_newcomer(user_id, repo_id, time):
    try:
        cursor = db.cursor()
        sql = "SELECT count(*) as num from (select distinct id from commits where project_id = %s and author_id = %s and created_at < '%s') as tmp"%(repo_id, user_id, time)
        #print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        if int(results[0][0]) < 3:
            return True
        else:
            return False
    except:
        print("Error: unable to fetch expert id")
        return False

file1 = open("GFI_mentor/RQ4/commit_info_merge1.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)

file3 = open("GFI_mentor/RQ4/all_sha.csv", "r")
csv_reader2 = csv.reader(file3)
next(csv_reader2)

file2 = open("GFI_mentor/RQ4/commit_info_cbn.csv", "w")
csv_writer = csv.writer(file2)
csv_writer.writerow(['issue_id', 'closed_by_newcomer', 'files', 'lines', 'sha', 'author_id'])

db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')

t = 0
issue_repos = {}
for row in csv_reader2:
    issue_repos[row[0]] = row[2]
for row in csv_reader:
    try:
        cursor = db.cursor()
        sql = "SELECT author_id, created_at, project_id from commits where sha = '%s'"%(row[3])
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        if judge_newcomer(results[0][0], issue_repos[row[0]], results[0][1]):
            csv_writer.writerow([row[0],1,row[1],row[2],row[3],results[0][0]])
            t += 1
            print(t)
        else:
            csv_writer.writerow([row[0],0,row[1],row[2],row[3],results[0][0]])
    except:
        print("Error: unable to fetch commit")