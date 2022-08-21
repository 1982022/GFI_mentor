import csv
import re

file1 = open("commit.txt", "r", encoding='UTF-8')
content = file1.read()

file3 = open("GFI_mentor/RQ4/commit_info_merge.csv", "w+", newline='')
csv_writer = csv.writer(file3)
csv_writer.writerow(['issue_id', 'files', 'lines'])

#\d(?= fil(e|es) changed)
#\d(?= deletio(n|ns)\(-\))
#\d(?= insertio(n|ns)\(\+\))
aparts = content.split('%^&*')
for apart in aparts:
    nums = re.findall(r'\d+', apart)[0]
    f = re.findall(r'\d+(?= files{0,1} changed)', apart)
    a = re.findall(r'\d+(?= insertions{0,1}\(\+\))', apart)
    d = re.findall(r'\d+(?= deletions{0,1}\(-\))', apart)
    if len(f) != 0:
        files = int(f[0])
    else:
        files = 0
    if len(a) != 0:
        add = int(a[0])
    else:
        add = 0
    if len(d) != 0:
        dele = int(d[0])
    else:
        dele = 0
    lines = add + dele
    csv_writer.writerow([nums, files, lines])
    print(nums, files, add, dele)