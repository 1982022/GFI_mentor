#!/usr/bin/python3
import csv
import pymysql
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from dateutil.relativedelta import relativedelta
import datetime
from tqdm import tqdm

# calculate the commenters experience who left comments on the related commits of the GFIs.
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
        print("Error: unable to fetch newcomers id")
        return False

def find_pr_id(pr_url, issue_url, issue_id):
    try:
        cursor = db.cursor()
        issue_items = issue_url.split('/')
        pr_items = pr_url.split('/')
        if issue_items[3]+issue_items[4] == pr_items[3]+pr_items[4]:
            sql = "SELECT repo_id from issues where id = %s"%(issue_id)
            #print(sql)
        else:
            sql = "SELECT id from projects where name = '%s' and url = '%s'"%(pr_items[4], "https://api.github.com/repos/"+pr_items[3]+"/"+pr_items[4])
            #print(pr_url, sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        repo_id = results[0][0]
        pullreq_id = pr_url.split('/')[-1]
        
        cursor = db.cursor()
        sql = "SELECT distinct pull_request_id from issues where repo_id = %s and issue_id = %s"%(repo_id, pullreq_id)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        pull_request_id = results[0][0]
        #print(pull_request_id)
    except:
        print("Error: unable to fetch pull request id")
        pull_request_id = -1
    return pull_request_id

if __name__ == '__main__':

    print(datetime.datetime.now())
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')
    file1 = open("/get_issue_pr/issue_pr.csv", "r")
    csv_reader = csv.reader(file1)
    next(csv_reader)

    file2 = open("pr_commenter.csv", "w")
    csv_writer = csv.writer(file2)
    csv_writer.writerow(['issue_id', 'issue_created_at', 'pr_id', 'user_id', 'comment_id', 'created_at', 'identity'])
    count = 0
    for row in csv_reader: 
        print(count)
        count += 1
        if count % 100 == 0:
            print(datetime.datetime.now())
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
                pull_request_id = find_pr_id(row[2], row[1], row[0])
                #print(pull_request_id)
                if pull_request_id != -1:
                    sql = "SELECT distinct comment_id, user_id, created_at from pull_request_comments prc where prc.pull_request_id = %s"%(pull_request_id)
                    cursor.execute(sql)
                    results = cursor.fetchall()
                    cursor.close()
                    #print(results)
                    if len(results):
                        for item in results:
                            comment_id, user_id, created_at = item[0], item[1], item[2]
                            experts = find_expert(repo_id, created_at)
                            #print(experts)
                            if user_id in experts:
                                csv_writer.writerow([row[0], issue_created_at, pull_request_id, user_id, comment_id, created_at, 'expert'])
                            else:
                                tag = judge_newcomer(user_id, repo_id, created_at)
                                if tag:
                                    csv_writer.writerow([row[0], issue_created_at, pull_request_id, user_id, comment_id, created_at, 'newcomers'])
                                else:
                                    csv_writer.writerow([row[0], issue_created_at, pull_request_id, user_id, comment_id, created_at, ''])
                    else:
                        csv_writer.writerow([row[0], issue_created_at, pull_request_id, '', '', '', ''])
            except:
                print("Error: unable to fetch  pr and pr comments")
        except:
            print("Error: unable to fetch repo id")
    file1.close()
    file2.close()
    db.close()

