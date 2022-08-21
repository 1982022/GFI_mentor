
import csv
import urllib3
import requests
from urllib.request import Request
from urllib.request import urlopen
import json


file2 = open('GFI_mentor/RQ4/stars.csv', 'w', newline='',encoding='utf-8')
file1 = open('GFI_mentor/RQ4/repo_url2.csv', 'r')
read = csv.reader(file1)
next(read)
csv_writer = csv.writer(file2)
csv_writer.writerow(['repo_id','stars'])

urllib3.disable_warnings()
head = {
    "user-agent": "agent",
    'Authorization': 'token ',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
session = requests.session()
flag = True
for row in read:
    url = row[1]
    try:
        req = Request(url, headers=head)
        response = urlopen(req).read()
        result = json.loads(response.decode())
        flag = False
        bodies = []
        stars = result['stargazers_count']
        csv_writer.writerow([row[0], stars])
    except Exception as e:
        if str(e) == "HTTP Error 404: Not Found" or str(e) == "HTTP Error 410: Gone":
            flag = False
        else:
            print("掉线啦ovo"+str(e))
    print(row[0])