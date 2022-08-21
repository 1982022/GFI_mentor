import csv

repo_GFI_count = {}
GFI_repo = {}
GFI_newcomer_expert = {}
file0 = open('../GFI_selection/GFI_closed.csv', 'r')
csv_reader = csv.reader(file0)
next(csv_reader)
for row in csv_reader:
    GFI_repo[row[0]] = row[1]
    if row[1] not in repo_GFI_count.keys():
        repo_GFI_count[row[1]] = 1
    else:
        repo_GFI_count[row[1]] += 1
file0.close()
repo_GFI_count = sorted(repo_GFI_count.items(), key=lambda item:item[1], reverse=True)
#print(repo_GFI_count)
repos = set([item[0] for item in repo_GFI_count])
network = {}
for k in repos:
    network[k] = {}
file1 = open('../RQ1/issue_commenter/issue_commenter.csv', 'r')
# issue_id,user_id,comment_id,created_at,identity
csv_reader1 = csv.reader(file1)
next(csv_reader1)
for row in csv_reader1:
    if row[4] == 'newcomers':
        if row[0] in GFI_newcomer_expert.keys():
            GFI_newcomer_expert[row[0]][0].append(row[1])
        else:
            GFI_newcomer_expert[row[0]] = [[row[1]],[]]
    if row[4] == 'expert':
        if row[0] in GFI_newcomer_expert.keys():
            GFI_newcomer_expert[row[0]][1].append(row[1])
        else:
            GFI_newcomer_expert[row[0]] = [[],[row[1]]]
file1.close()

file2 = open('../RQ1/issue_pr_commenter/pr_commenter.csv', 'r')
#issue_id,issue_created_at,pr_id,user_id,comment_id,created_at,identity
csv_reader2 = csv.reader(file2)
next(csv_reader2)
for row in csv_reader2:
    if row[6] == 'newcomers':
        if row[0] in GFI_newcomer_expert.keys():
            GFI_newcomer_expert[row[0]][0].append(row[3])
        else:
            GFI_newcomer_expert[row[0]] = [[row[3]],[]]
    if row[6] == 'expert':
        if row[0] in GFI_newcomer_expert.keys():
            GFI_newcomer_expert[row[0]][1].append(row[3])
        else:
            GFI_newcomer_expert[row[0]] = [[],[row[3]]]
file2.close()

file3 = open('../RQ1/commit_commenter/commit_commenter.csv', 'r')
#issue_id,issue_created_at,commit_sha,commit_id,user_id,comment_id,created_at,identity
csv_reader3 = csv.reader(file3)
next(csv_reader3)
for row in csv_reader3:
    if row[7] == 'newcomers':
        if row[0] in GFI_newcomer_expert.keys():
            GFI_newcomer_expert[row[0]][0].append(row[4])
        else:
            GFI_newcomer_expert[row[0]] = [[row[4]],[]]
    if row[7] == 'expert':
        if row[0] in GFI_newcomer_expert.keys():
            GFI_newcomer_expert[row[0]][1].append(row[4])
        else:
            GFI_newcomer_expert[row[0]] = [[],[row[4]]]
file3.close()

for issue_id in GFI_newcomer_expert.keys():
    repo_id = GFI_repo[issue_id]
    newcomers =  list(set(GFI_newcomer_expert[issue_id][0]))
    experts = list(set(GFI_newcomer_expert[issue_id][1]))
    for newcomer in newcomers:
        for expert in experts:
            newcomer_expert = '%s,%s'%(newcomer, expert)
            if newcomer_expert in network[repo_id].keys():
                network[repo_id][newcomer_expert] += 1
            else:
                network[repo_id][newcomer_expert] = 1

file4 = open('network.csv', 'w')
#repo_id, newcomer_id, expert_id, weight
csv_writer = csv.writer(file4)
csv_writer.writerow(['repo_id', 'newcomer_id', 'expert_id', 'weight'])
for repo_id in network.keys():
    items = network[repo_id]
    for newcomer_expert in items.keys():
        l = newcomer_expert.split(',')
        csv_writer.writerow([repo_id, l[0], l[1], items[newcomer_expert]])
file4.close()

