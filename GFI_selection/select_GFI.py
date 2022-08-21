#!/usr/bin/python3
import csv
import pymysql
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
from scipy import stats

"""
file1 = open('repo_GFIlabel.csv', 'w')
csv_writer = csv.writer(file1)
csv_writer.writerow(['label_id', 'repo_id'])
# select non-forked repos with gfi label
db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')
cursor = db.cursor()
sql1 = "SELECT distinct repo_labels.id, repo_labels.repo_id from repo_labels, projects\
    where repo_labels.repo_id = projects.id and projects.forked_from is NULL and repo_labels.name = 'good first issue'"
try:
   cursor.execute(sql1)
   results = cursor.fetchall()
   for row in results:
      label_id = row[0]
      repo_id = row[1]
      csv_writer.writerow([label_id, repo_id])
except:
   print ("Error: unable to fetch data")
db.close()
file1.close()
print('Finished!')

# number of repos with GFI label
file1 = open("repo_GFIlabel.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)
d = []
for row in csv_reader:
   d.append(row[1])
d = set(d)
print(len(d))
file1.close()

# GFI distribution
sql2 = "SELECT distinct issue_labels.issue_id, issue_labels.label_id, repo_labels.repo_id \
   from repo_labels, projects, issue_labels\
      where repo_labels.repo_id = projects.id and \
       issue_labels.label_id = repo_labels.id and \
          projects.forked_from is NULL and \
             repo_labels.name = 'good first issue'"

file1 = open('repo_GFI_distribution.csv', 'w')
csv_writer = csv.writer(file1)
csv_writer.writerow(['issue_id', 'label_id', 'repo_id'])
try:
   cursor.execute(sql2)
   results = cursor.fetchall()
   for row in results:
      issue_id = row[0]
      label_id = row[1]
      repo_id = row[2]
      csv_writer.writerow([issue_id, label_id, repo_id])
except:
   print ("Error: unable to fetch data")
db.close()
file1.close()
print('Finished!')

# GFI distribution
idata = open("issue_labels.csv","r")
odata = open("repo_GFIlabel.csv","r")

leftdata = csv.reader(idata)
rightdata = csv.reader(odata)
next(rightdata)
def gen_chunks(reader, chunksize=1000000):
    chunk = []
    for i, line in enumerate(reader):
        if (i % chunksize == 0 and i > 0):
            yield chunk
            del chunk[:]
        chunk.append(line)
    yield chunk

count = 0

d1 = dict([(rows[0],rows[1]) for rows in rightdata]) # label_id, repo_id

with open("repo_GFI_distribution_new.csv", "w") as csvfile:
   output = csv.writer(csvfile)
   output.writerow(['issue_id', 'label_id', 'repo_id'])
   # chunk: label_id, issue_id
   l = []
   for chunk in gen_chunks(leftdata):
      for k in chunk:
         l.append([k[1], k[0], d1.get(k[0], "NaN")])
      count = count+1
      #print(s)
      print(count)
   s = set(tuple(item) for item in l if item[2] != 'NaN')
   for item in s:
      output.writerow(list(item))
idata.close()
odata.close()
"""
# Number of GFI per repo
file1 = open("repo_GFI_distribution.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)
d = dict()
for row in csv_reader:
   if row[2] not in d.keys():
      d[row[2]] = 1
   else:
      d[row[2]] += 1
file1.close()
df = pd.DataFrame(list(d.values()), columns = ['#GFIs'])
df = df[(np.abs(stats.zscore(df['#GFIs'])) < 3)]
p1 = sns.violinplot(y = df['#GFIs'], color="cyan")
print(df['#GFIs'])
plt.show()
plt.savefig("repo_GFI_distribution.png")
"""
# print(sum(list(d.values())))

d = dict(sorted(d.items(), key = lambda kv: kv[1], reverse=True))
tt = 0
ss = []
for k in d.keys():
   if tt > 100:
      break
   else:
      ss.append([k, d[k]])
      tt += 1
print("top 100 repos with most GFI")
print(ss)

num_GFI = list(d.values())

print("number of repos have GFI: %d" % len(d.keys()))
print("top 1%%: %d" % np.percentile(num_GFI,99))
print("top 5%%: %d" % np.percentile(num_GFI,95))
print("top 10%%: %d" % np.percentile(num_GFI,90))
print("top 50%%: %d" % np.percentile(num_GFI,50))

# obatin top 1% repo_id and GFI_id
t = 0
res = []
n = int(len(d)*0.01) # number of top 1% repos
print("number of top 1%% repos: %d" % n)
for k in d.keys():
   if t > n:
      break
   else:
      res.append(k)
      t += 1

file1 = open("repo_GFI_distribution_new.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)

file2 = open("repo_GFI_top1percent.csv", "w")
csv_writer = csv.writer(file2)
csv_writer.writerow(['issue_id', 'label_id', 'repo_id'])
for row in csv_reader:
   if row[2] in res:
      csv_writer.writerow(row)
   else:
      continue
file1.close()
file2.close()
"""
file2 = open("repo_GFI_top1percent.csv", "r")
csv_reader = csv.reader(file2)
next(csv_reader)
d2 = dict()
for row in csv_reader:
   if row[2] not in d2.keys():
      d2[row[2]] = 1
   else:
      d2[row[2]] += 1
file2.close()
df = pd.DataFrame(list(d2.values()), columns = ['#GFIs'])
df = df[(np.abs(stats.zscore(df['#GFIs'])) < 3)]
plt.cla()
p1 = sns.violinplot(y = df['#GFIs'],color="cyan")
print(df['#GFIs'])
plt.show()
plt.savefig("repo_GFI_top1percent.png")

print(df.median())
"""

# choose closed issue
file1 = open("repo_GFI_top1percent.csv", "r")
csv_reader = csv.reader(file1)
next(csv_reader)

with open("GFI_closed.csv", "w") as csvfile:
   output = csv.writer(csvfile)
   output.writerow(['issue_id'])
   for row in csv_reader:
      db = pymysql.connect(host='localhost',
                     user='root',
                     password='password',
                     database='ghtorrent_restore')
      cursor = db.cursor()
      sql = "SELECT * from issue_events where issue_id = %s and action = 'closed'"%(row[0])
      cursor.execute(sql)
      results = cursor.fetchall()
      if len(results) > 0:
         print(results)
         output.writerow([row[0]])
      else:
         print ("nonclosed")
      db.close()
file1.close()
"""