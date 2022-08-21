#!/usr/bin/python3
from calendar import c
import csv
import re
import pymysql
import numpy as np
import pandas as pd
from regex import E
from scipy import stats
import requests
import json

db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')

file1 = open('GFI_mentor/RQ4/repos.csv', 'r')
csv_reader = csv.reader(file1)
next(csv_reader)


file2 = open("GFI_mentor/RQ4/repo_attri.csv", "w")
csv_writer = csv.writer(file2)
csv_writer.writerow(['repo_id', '#authors', '#commits', '#issues', '#month'])

repo = {}
repo_attri = {}

for row in csv_reader:
        r = row[0]
        repo_attri[r] = []
        try:
            
            cursor = db.cursor() 
            sql = "SELECT count(distinct author_id) from commits where project_id = %s"%(r)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            repo_attri[r].append(int(results[0][0]))
        except:
            repo_attri[r].append(-1)
        
        try:
            cursor = db.cursor() 
            sql = "SELECT count(distinct id) from commits where project_id = %s"%(r)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            repo_attri[r].append(int(results[0][0])) 
        except:
            repo_attri[r].append(-1)
        
        try:
            cursor = db.cursor() 
            sql = "SELECT count(distinct id) from issues where repo_id = %s"%(r)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            repo_attri[r].append(int(results[0][0]))  
        except:
            repo_attri[r].append(-1)
        
        try:
            cursor = db.cursor() 
            sql = "SELECT timestampdiff(month, created_at, updated_at) from projects where id = %s"%(r)
            cursor.execute(sql)
            results = cursor.fetchall()
            cursor.close()
            repo_attri[r].append(int(results[0][0]))  
        except:
            repo_attri[r].append(-1)
        csv_writer.writerow([r, repo_attri[r][0], repo_attri[r][1], repo_attri[r][2], repo_attri[r][3]])
db.close()

