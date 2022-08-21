import csv
from datetime import datetime
from enum import Flag
from sqlite3 import DataError

def time_in_one():
    file1 = open('../issue_commenter/issue_commenter_exp_distribution.csv', 'r')
    file2 = open('all_time.csv', 'r')
    file4 = open('all_time_with_CommentInfo.csv', 'w+', newline='')
    read1 = csv.reader(file1)
    read2 = csv.reader(file2)
    c_writer = csv.writer(file4)
    all_comment = {}
    c_writer.writerow(['issue_id','response_seconds', 'comment', 'commenter','newcomer', 'expert', 'newcomer_comment', 'expert_comment'])
    for row in read2:
        if row[0]!='issue_id':
            all_comment[row[0]] = [row[0],row[1]]
    for row in read1:
        if row[0] in all_comment:
             all_comment[row[0]] = all_comment[row[0]]+[row[1], row[2], row[3], row[4], row[5], row[6]]
    for key,value in all_comment.items():
        c_writer.writerow([value[0],value[1],value[2],value[3],value[4],value[5],value[6],value[7]])

time_in_one()
