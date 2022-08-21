#!/usr/bin/python3
import csv
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats


db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')

file1 = open("pr_commenter.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)

file2 = open("pr_commenter_exp_distribution.csv", "w")
csv_writer = csv.writer(file2)
csv_writer.writerow(['issue_id', 'created_at', '#comment', '#commenter', '#newcomer', '#expert', '#newcomer_comment', '#expert_comment'])

# res: issue_id, created_at, #comment, #commenter, #newcomer, #expert, #newcomer_comment, #expert_comment
res = []
num_comment, num_newcomer_comment, num_expert_comment = 0, 0, 0
commenters, newcomers, experts = [], [], []
issue_id = -1
num = 0
for row in csv_reader:
    print(num)
    num += 1
    if row[0] != issue_id:
        try:
            cursor = db.cursor() 
            sql = "SELECT created_at from issues where id = %s"%(issue_id)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            created_at = results[0][0]
        except:
            created_at = -1
        res.append([issue_id, created_at, num_comment, len(set(commenters)), len(set(newcomers)), len(set(experts)), num_newcomer_comment, num_expert_comment])    
        issue_id = row[0] 
        #print(res[-1])

        num_comment, num_newcomer_comment, num_expert_comment = 0, 0, 0
        commenters, newcomers, experts = [], [], []
        if row[4] != '':
            num_comment = 1
            commenters = [row[3]]
        if row[6] == 'newcomers':
            newcomers = [row[3]]
            num_newcomer_comment = 1
        if row[6] == 'expert':            
            experts = [row[3]]
            num_expert_comment = 1
        
    else:
        if row[4] != '':
            num_comment += 1
            commenters.append(row[3])
        if row[6] == 'newcomers':
            newcomers.append(row[3])
            num_newcomer_comment += 1
        if row[6] == 'expert':            
            experts.append(row[3])
            num_expert_comment += 1
res.append([issue_id, created_at, num_comment, len(set(commenters)), len(set(newcomers)), len(set(experts)), num_newcomer_comment, num_expert_comment]) 
res = res[1:]
#print(res)

for item in res:
    csv_writer.writerow(item)
file1.close()
file2.close()
db.close()