import csv
from dateutil.relativedelta import relativedelta
import datetime
                     
general = set()
issues = {}
issue_repo = {}
file4 = open('../../GFI_selection/GFI_closed.csv', 'r')
csv_reader4 = csv.reader(file4)
next(csv_reader4)
for row in csv_reader4:
    issues[row[0]] = set()
    issue_repo[row[0]] = row[1]
file4.close()


file1 = open('../issue_commenter/issue_commenter.csv', 'r')
# issue_id,user_id,comment_id,created_at,identity
csv_reader1 = csv.reader(file1)
next(csv_reader1)
for row in csv_reader1:
    if row[2] != '':
        if row[4] != '':
            issues[row[0]].add(row[4])
        else:
            issues[row[0]].add('general')
file1.close()

file2 = open('../issue_pr_commenter/pr_commenter.csv', 'r')
#issue_id,issue_created_at,pr_id,user_id,comment_id,created_at,identity
csv_reader2 = csv.reader(file2)
next(csv_reader2)
for row in csv_reader2:
    if row[4] != '':
        if row[6] != '':
            issues[row[0]].add(row[6])
        else:
            issues[row[0]].add('general')
file2.close()

file3 = open('../commit_commenter/commit_commenter.csv', 'r')
#issue_id,issue_created_at,commit_sha,commit_id,user_id,comment_id,created_at,identity
csv_reader3 = csv.reader(file3)
next(csv_reader3)
for row in csv_reader3:
    if row[5] != '':
        if row[7] != '':
            issues[row[0]].add(row[7])
        else:
            issues[row[0]].add('general')
file3.close()

res = {}
file4 = open('newcomer_expert_GFIs.csv', 'w')
csv_writer = csv.writer(file4)
csv_writer.writerow(['issue_id'])

for i in issues.keys():
    items = issues[i]
    label = '+'.join(sorted(list(items)))
    if label == 'expert+newcomers' or label == 'expert+general+newcomers':
        csv_writer.writerow([i])
    if label not in res.keys():
        res[label] = 1
    else:
        res[label] += 1
print(res)
print(len(general))

file4.close()