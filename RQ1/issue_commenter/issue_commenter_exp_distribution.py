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

file1 = open("issue_commenter.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)

file2 = open("issue_commenter_exp_distribution.csv", "w")
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
        #created_at = -1
        res.append([issue_id, created_at, num_comment, len(set(commenters)), len(set(newcomers)), len(set(experts)), num_newcomer_comment, num_expert_comment])    
        issue_id = row[0] 

        num_comment, num_newcomer_comment, num_expert_comment = 0, 0, 0
        commenters, newcomers, experts = [], [], []
        if row[2] != '':
            num_comment = 1
            commenters = [row[1]]
        if row[4] == 'newcomers':
            newcomers = [row[1]]
            num_newcomer_comment = 1
        if row[4] == 'expert':            
            experts = [row[1]]
            num_expert_comment = 1
        
    else:
        if row[2] != '':
            num_comment += 1
            commenters.append(row[1])
        if row[4] == 'newcomers':
            newcomers.append(row[1])
            num_newcomer_comment += 1
        if row[4] == 'expert':            
            experts.append(row[1])
            num_expert_comment += 1
res.append([issue_id, created_at, num_comment, len(set(commenters)), len(set(newcomers)), len(set(experts)), num_newcomer_comment, num_expert_comment])
res = res[1:]

for item in res:
    csv_writer.writerow(item)
file1.close()
file2.close()
db.close()

comments_list = list(np.array(res).T[2]) 
newcomer_comments_list = list(np.array(res).T[6])
expert_comments_list = list(np.array(res).T[7])            
d_comment =  [[i, 'all'] for i in comments_list] + [[i, 'newcomer'] for i in newcomer_comments_list] + [[i, 'expert'] for i in expert_comments_list]
df_comment = pd.DataFrame(d_comment, columns = ['num_comments', 'commenter_identity'])
df_comment = df_comment.explode('num_comments')
df_comment['num_comments'] = df_comment['num_comments'].astype('int')
# remove outliers
df_comment = df_comment[(np.abs(stats.zscore(df_comment['num_comments'])) < 3)]
print(df_comment.loc[df_comment['commenter_identity'] == 'all']['num_comments'].quantile([0.25, 0.5, 0.75]))
print(df_comment.loc[df_comment['commenter_identity'] == 'newcomer']['num_comments'].quantile([0.25, 0.5, 0.75]))
print(df_comment.loc[df_comment['commenter_identity'] == 'expert']['num_comments'].quantile([0.25, 0.5, 0.75]))
# draw distribution of number of comments
sns.set(style="whitegrid")
sns.violinplot(x="commenter_identity", y="num_comments", data=df_comment)
plt.show()
plt.savefig("issue_comments_distribution.png")

commenter_list = list(np.array(res).T[3]) 
newcomer_commenter_list = list(np.array(res).T[4])
expert_commenter_list = list(np.array(res).T[5])            
d_commenter =  [[i, 'all'] for i in commenter_list] + [[i, 'newcomer'] for i in newcomer_commenter_list] + [[i, 'expert'] for i in expert_commenter_list]
df_commenter = pd.DataFrame(d_commenter, columns = ['num_commenters', 'commenter_identity'])
df_commenter = df_commenter.explode('num_commenters')
df_commenter['num_commenters'] = df_commenter['num_commenters'].astype('int')
# remove outliers
df_commenter = df_commenter[(np.abs(stats.zscore(df_commenter['num_commenters'])) < 3)]
print(df_commenter.loc[df_commenter['commenter_identity'] == 'all']['num_commenters'].quantile([0.25, 0.5, 0.75]))
print(df_commenter.loc[df_commenter['commenter_identity'] == 'newcomer']['num_commenters'].quantile([0.25, 0.5, 0.75]))
print(df_commenter.loc[df_commenter['commenter_identity'] == 'expert']['num_commenters'].quantile([0.25, 0.5, 0.75]))

# draw distribution of number of commenters
plt.cla()
sns.set(style="whitegrid")
sns.violinplot(x="commenter_identity", y="num_commenters", data=df_commenter)
plt.show()
plt.savefig("issue_commenters_distribution.png")
