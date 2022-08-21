#用来将comment，commit，pr的响应时间信息放到一起
import csv
from datetime import datetime
from enum import Flag
from sqlite3 import DataError
def in_one_file():
    file1 = open('../issue_commenter/issue_commenter.csv', 'r')
    file2 = open('../commit_commenter/commit_commenter.csv', 'r')
    file3 = open('../issue_pr_commenter/pr_commenter.csv', 'r')
    file4 = open('all.csv', 'w+', newline='')
    df1 = csv.reader(file1)
    df2 = csv.reader(file2)
    df3 = csv.reader(file3)
    c_writer = csv.writer(file4)
    c_writer.writerow(['issue_id','comment_id','created_at','identity'])
    j = ''
    all_comment = {}
    for row in df1:
        if row[2] == ''or row[4] == '' or row[0] == 'issue_id':
            continue
        if row[0] in all_comment:
            all_comment[row[0]].append([row[0], row[2], row[3], row[4]])
        else:
            all_comment[row[0]] = [[row[0], row[2], row[3], row[4]]]
    for row in df2:

        if row[5] == ''or row[7] == '' or row[0] == 'issue_id':
            continue
        if row[0] in all_comment:
            all_comment[row[0]].append([row[0], row[5], row[6], row[7]])
    
    for row in df3:

        if row[4] == ''or row[6] == '' or row[0] == 'issue_id':
            continue
        if row[0] in all_comment:
            all_comment[row[0]].append([row[0], row[4], row[5], row[6]])
    
    for keys, values in all_comment.items():

        values.sort(key=lambda time: time[2], reverse=False) 
        print(keys)
        for value in values:
            c_writer.writerow([value[0],value[1],value[2],value[3]]) 
    

def issue():
    file1 = open('all.csv', 'r')
    file2 = open('all_time.csv', 'w+', newline='')
    df = csv.reader(file1)
    csv_writer = csv.writer(file2)
    # issue_id	user_id	comment_id	created_at	identity
    csv_writer.writerow(['issue_id','seconds','time'])
    j = ''
    date1 = []
    date2 = []
    for row in df:
        # i&j判断是否进入下一个issue或pr
        i = row[0]
        if len(row)<4:
            print(row[0]+"无数据")
            continue
        # 如果第一个数据
        if j == '' or j == 'issue_id':
            j = i
        # 进入下一个
        elif i!= j:
            issue_id = j
            # 如果两个date都有数据，说明expert和新来者都评论了
            if date1 != [] and date2 !=[]:
                # 找出最早的新来者和专家的评论
                date1.sort()
                date2.sort()
                time1 = datetime.strptime(date1[0], '%Y-%m-%d %H:%M:%S')
                time2 = datetime.strptime(date2[0], '%Y-%m-%d %H:%M:%S')
                # 如果专家在新来者之后评论就写数据，否则认为无效……？
                if time2>time1:
                    time = time2 - time1
                    seconds = (time2-time1).total_seconds()
                    csv_writer.writerow([issue_id,seconds,time])
            date1 = []
            date2 = []
            j = i
        if row[3] =='newcomers':
                date1.append(row[2])
        elif row[3] == 'expert':
                date2.append(row[2])

# issue()
# # pr()
# # in_one_file()



