from sshtunnel import SSHTunnelForwarder
import pymysql
import csv
from datetime import datetime


server = SSHTunnelForwarder(
	ssh_address_or_host=('210.22.22.136',22322), 
	ssh_username='ubuntu',  
	ssh_password='inspur@123',  
	remote_bind_address=('localhost', 3306)  
)

server.start()
con = pymysql.connect(host='127.0.0.1',
                     port=server.local_bind_port,
                     user='root',
                     password='password',
                     database='ghtorrent_restore',
                     charset='utf8')  
file1 = open('all_time.csv', 'r')
file0 = open('../issue_commenter/issue_commenter_exp_distribution.csv', 'r')
file2 = open('ratio.csv', 'w', newline='',encoding='utf-8')
read = csv.reader(file1)
read0 = csv.reader(file0)
csv_writer = csv.writer(file2)
csv_writer.writerow(['issue_id', 'response_seconds','all_time','ratio'])
start_times = {}
for row2 in read0:
    if row2[0] == 'issue_id':
        continue
    start_times[row2[0]]=row2[1]
for row in read:
    if row[0]=='issue_id':
        continue
    cursor = con.cursor()
    sql = "select * from issue_events where issue_id = %s"
    cursor.execute(sql,(row[0]))
    results = cursor.fetchall()
    end_time = ''
    start_time = datetime.strptime(start_times[row[0]], '%Y-%m-%d %H:%M:%S')
    for row1 in results:
        if row1[3] == 'closed':
            end_time =row1[5]
    if start_time != '' and end_time!= '' :
        all_time = (end_time-start_time).total_seconds()
        if float(all_time) == 0:
            print(row[0])
    ratio = float(row[1])/float(all_time)
    csv_writer.writerow([row[0], row[1],all_time,ratio])

cursor.close()
con.close()
server.close()
