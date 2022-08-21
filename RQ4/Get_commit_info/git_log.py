#!/usr/bin/python3
import csv
from itertools import count
import os

from regex import E, F

file1 = open("GFI_mentor/RQ4/filenames.txt", "r")
names = file1.readlines()

file2 = open("GFI_mentor/RQ4/repo_urls.csv", "r")
csv_reader = csv.reader(file2)
next(csv_reader)

file3 = open("GFI_mentor/RQ4/all_sha.csv", "r")
csv_reader2 = csv.reader(file3)
next(csv_reader2)


repo_names = {}
repo_shas = {}
merge_issue = {}
for row in csv_reader:
    repo_names[row[2]] = row[0]

for row in csv_reader2:
    if row[2] in repo_shas:
        repo_shas[row[2]].append([row[0], row[4]])
    else:
        repo_shas[row[2]] = [[row[0], row[4]]]

for n in names:
    name = n.strip()
    repo_id = repo_names[name]
    shas = repo_shas[repo_id]
    print(shas)
    for s in shas:
        issue_id = s[0]
        sha = s[1]
        cmd = 'cd .. && cd clone_files && cd ' + name + ' && '+ 'echo "'+ issue_id + '" >>../../commit.txt' + ' && ' +'git log --shortstat '+sha+' -1 >> ../../commit.txt ' + ' && echo "%^&*" >>../../commit.txt'
        #print(cmd)
        os.system(cmd)