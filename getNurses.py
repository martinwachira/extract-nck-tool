from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import requests
import re

br = webdriver.Firefox()
url = "https://osp.nckenya.com/LicenseStatus"
br.get(url)
content = br.page_source
soup = BeautifulSoup(content, 'lxml')
sleep(2)
sName = br.find_element_by_xpath("/html/body/div[1]/div[2]/section/div[2]/div/div/div/div/div/div/div[2]/form/div[1]/div/div/input")
sleep(3)
sName.send_keys("martin")
br.find_element_by_xpath("//*[@id='provider']/div[1]/div/div/div/button").click()
sleep(3)

table = soup.find('table')

body = thead.find_all('tr')
#
# get column heads
head = body[0]
body_rows = body[1:]
headings = []

for item in head.find_all('th'):
    item = (item.text).rstrip("\n")
    headings.append(item)

print(headings)
#declare an empty list for holding all records
all_rows = []

# loop through all table rows to get all table datas

for nurses in table.find_all('tbody'):
    rows = nurses.find_all('tr')
    for row in rows:
        nurseRecords = row.find('td').text
        sleep(2)
        print(nurseRecords)

# for row_num in range(len(body_rows)):
#     row = []
#     for row_item in body_rows[row_num].find_all('td'):
#         stripA = re.sub("(\xa0)|(\n)|,","",row_item.text)
#         row.append(stripA)
#
# all_rows.append(row)

# match each record to its field name
# cols = ['name', 'license', 'xxx', 'xxxx']
df = pd.DataFrame(data=nurseRecords, columns=headings)

# print data
df.head()

# save nurses list to csv
df.to_csv('nurses.csv')
