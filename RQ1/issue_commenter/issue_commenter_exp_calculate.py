#!/usr/bin/python3
import csv
import pymysql
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from dateutil.relativedelta import relativedelta

# standard for identifying experts: whether he/she was among the top 20% of contributors in the year before the issue was reported.
# standard for identifying newcomers: the number of commits he/she contributed less than three.

def find_expert(repo_id, created_at):
    try:
        #print(repo_id, created_at)
        cursor = db.cursor()
        sql = "SELECT distinct author_id, count(*) as num from (select distinct id, author_id from commits where project_id = %s and created_at between '%s' and '%s') as tmp group by author_id"%(repo_id, created_at - relativedelta(years=1), created_at)
        #print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        d = dict([list(item) for item in results])
        d = dict(sorted(d.items(), key = lambda kv: kv[1], reverse=True))
        l = int(len(d) * 0.2)
        experts = list(d.keys())[:l+1]
        #print(experts)
        return experts
    except:
        print("Error: unable to fetch expert id")
        return []

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


if __name__ == '__main__':


    db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')
    file1 = open("../../GFI_selection/GFI_closed.csv", "r")
    csv_reader = csv.reader(file1)
    next(csv_reader)

    file2 = open("issue_commenter.csv", "w")
    csv_writer = csv.writer(file2)
    csv_writer.writerow(['issue_id', 'user_id', 'comment_id', 'created_at', 'identity'])
    count = 0
    for row in csv_reader: 
        print(count)
        count += 1
        if count % 500 == 0:
            db.close()
        else:
            db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore') 
        try:
            cursor = db.cursor()
            sql = "SELECT distinct repo_id, created_at from issues where id = %s"%(row[0])
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            repo_id, issue_created_at = results[0][0], results[0][1]
            #print(repo_id, issue_created_at)
            try:
                cursor = db.cursor()
                sql = "SELECT distinct * from issue_comments where issue_id = %s"%(row[0])
                cursor.execute(sql)
                results = cursor.fetchall()
                cursor.close()
                if len(results):
                    for item in results:
                        issue_id, user_id, comment_id, created_at = item[0], item[1], item[2], item[3]
                        experts = find_expert(repo_id, created_at)
                        if user_id in experts:
                            csv_writer.writerow([issue_id, user_id, comment_id, created_at, 'expert'])
                        else:
                            tag = judge_newcomer(user_id, repo_id, created_at)
                            if tag:
                                csv_writer.writerow([issue_id, user_id, comment_id, created_at, 'newcomers'])
                            else:
                                csv_writer.writerow([issue_id, user_id, comment_id, created_at, ''])
                else:
                    csv_writer.writerow([row[0], '', '', '', ''])
            except:
                print("Error: unable to fetch issue comments")            
        except:
            print("Error: unable to fetch repo id")

    file1.close()
    file2.close()
    db.close()

