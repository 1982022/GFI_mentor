#!/usr/bin/python3
import csv
import pymysql
import numpy as np
import pandas as pd
from scipy import stats
import requests
import json

db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')

file1 = open('types.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)

repo_type = dict()
for row in csv_reader:
    repo_type[row[0]] = row[1]
file1.close()

repo_attri = dict()
numm = 0
for repo in repo_type.keys():
    print(repo, numm)
    numm += 1
    repo_attri[repo] = []
    try:
        cursor = db.cursor() 
        sql = "SELECT count(distinct author_id) from commits where project_id = %s"%(repo)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        repo_attri[repo].append(int(results[0][0]))
    except:
        repo_attri[repo].append(-1)
    
    try:
        cursor = db.cursor() 
        sql = "SELECT count(distinct id) from commits where project_id = %s"%(repo)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        repo_attri[repo].append(int(results[0][0])) 
    except:
        repo_attri[repo].append(-1)
    
    try:
        cursor = db.cursor() 
        sql = "SELECT count(distinct id) from issues where repo_id = %s"%(repo)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        repo_attri[repo].append(int(results[0][0]))  
    except:
        repo_attri[repo].append(-1)
    
    try:
        cursor = db.cursor() 
        sql = "SELECT timestampdiff(month, created_at, updated_at) from projects where id = %s"%(repo)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        repo_attri[repo].append(int(results[0][0]))  
    except:
        repo_attri[repo].append(-1)

    try:
        cursor = db.cursor() 
        sql = "SELECT url from projects where id = %s"%(repo)
        # print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        request_url = results[0][0]
        token = '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'
        headers = {'Authorization': 'token ' + token}
        response = requests.get(request_url, headers=headers).text
        info = json.loads(response)
        repo_attri[repo].append(int(info["stargazers_count"]))
    except:
        repo_attri[repo].append(-1)
db.close()

type_attri = dict()
for repo in repo_attri:
    if repo_type[repo] not in type_attri.keys():
        type_attri[repo_type[repo]] = [[repo]+repo_attri[repo]]
    else:
        type_attri[repo_type[repo]].append([repo]+repo_attri[repo])

frame_centralized = pd.DataFrame(type_attri['centralized mentoring'], columns = ['repo_id', '#authors', '#commits', '#issues', '#month', '#stars'])
frame_centralized.insert(frame_centralized.shape[1], 'type', 'centralized mentoring')

frame_decentralized = pd.DataFrame(type_attri['decentralized mentoring'], columns = ['repo_id','#authors', '#commits', '#issues', '#month', '#stars'])
frame_decentralized.insert(frame_decentralized.shape[1], 'type', 'decentralized mentoring')

frame_collaborative = pd.DataFrame(type_attri['collaborative mentoring'], columns = ['repo_id','#authors', '#commits', '#issues', '#month', '#stars'])
frame_collaborative.insert(frame_collaborative.shape[1], 'type', 'collaborative mentoring')

frame_distributed = pd.DataFrame(type_attri['distributed mentoring'], columns = ['repo_id','#authors', '#commits', '#issues', '#month', '#stars'])
frame_distributed.insert(frame_distributed.shape[1], 'type', 'distributed mentoring')

frame = pd.concat([frame_centralized, frame_decentralized, frame_collaborative, frame_distributed], ignore_index = True)

frame.to_csv('sample_repo_attri.csv')