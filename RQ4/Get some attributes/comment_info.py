import csv
file1 = open("GFI_mentor/RQ1/commit_commenter/commit_commenter.csv", "r")
csv_reader1 = csv.reader(file1)
next(csv_reader1)

file2 = open("GFI_mentor/RQ1/issue_commenter/issue_commenter.csv", "r")
csv_reader2 = csv.reader(file2)
next(csv_reader2)

file3 = open("GFI_mentor/RQ1/issue_pr_commenter/pr_commenter.csv", "r")
csv_reader3 = csv.reader(file3)
next(csv_reader3)



file4 = open("GFI_mentor/RQ4/all_comment.csv", "w+", newline='')
csv_writer = csv.writer(file4)
csv_writer.writerow(['issue_id', 'issue_expert_comment', 'issue_newcomer_comment', 'issue_expert','issue_newcomer', 'commit_expert_comment',
                     'commit_newcomer_comment', 'commit_expert', 'commit_newcomer', 'pr_expert_comment', 'pr_newcomer_comment'
                     , 'expert_comment', 'newcomer_comment'])

commit = {}
pr = {}
issue = {}
for row in csv_reader1:
    if row[0] in commit:
        commit[row[0]].append([row[4], row[7]])
    else:
        commit[row[0]] = [[row[4], row[7]]]
for row in csv_reader2:
    if row[0] in issue:
        issue[row[0]].append([row[1], row[4]])
    else:
        issue[row[0]] = [[row[1], row[4]]]
for row in csv_reader3:
    if row[0] in pr:
        pr[row[0]].append([row[3], row[6]])
    else:
        pr[row[0]] = [[row[3], row[6]]]

for key, value in commit.items():
    user = {}
    expert_comment = 0
    newcomer_comment = 0
    expert = 0
    newcomer = 0
    for v in value:
        if v[1] == 'expert':
            expert_comment += 1
        elif v[1] == 'newcomers':
            newcomer_comment += 1
        if v[0] in user:
            pass
        else:
            user[v[0]] = v[1]
            if v[1] == 'expert':
                expert += 1
            elif v[1] == 'newcomers':
                newcomer += 1
    commit[key] = [expert_comment, newcomer_comment, expert, newcomer]

for key, value in pr.items():
    user = {}
    expert_comment = 0
    newcomer_comment = 0
    expert = 0
    newcomer = 0
    for v in value:
        if v[1] == 'expert':
            expert_comment += 1
        elif v[1] == 'newcomers':
            newcomer_comment += 1
        if v[0] in user:
            pass
        else:
            user[v[0]] = v[1]
            if v[1] == 'expert':
                expert += 1
            elif v[1] == 'newcomers':
                newcomer += 1
    pr[key] = [expert_comment, newcomer_comment, expert, newcomer]

for key, value in issue.items():
    user = {}
    expert_comment = 0
    newcomer_comment = 0
    expert = 0
    newcomer = 0
    for v in value:
        if v[1] == 'expert':
            expert_comment += 1
        elif v[1] == 'newcomers':
            newcomer_comment += 1
        if v[0] in user:
            pass
        else:
            user[v[0]] = v[1]
            if v[1] == 'expert':
                expert += 1
            elif v[1] == 'newcomers':
                newcomer += 1
    issue[key] = [expert_comment, newcomer_comment, expert, newcomer]

for key, value in issue.items():
    pr_info = [0, 0, 0, 0]
    commit_info = [0, 0, 0, 0]
    if key in pr:
        pr_info = pr[key]
    if key in commit:
        commit_info = commit[key]
    csv_writer.writerow([key,value[0], value[1], value[2], value[3], commit_info[0], commit_info[1], commit_info[2], commit_info[3]
                         ,pr_info[0], pr_info[1], pr_info[2], pr_info[3]])