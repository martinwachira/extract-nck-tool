from selenium import webdriver
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd
import requests
import re
from datetime import datetime

br = webdriver.Firefox()
url = "https://osp.nckenya.com/LicenseStatus"
br.get(url)
sleep(2)
sName = br.find_element_by_xpath("/html/body/div[1]/div[2]/section/div[2]/div/div/div/div/div/div/div[2]/form/div[1]/div/div/input")
sleep(3)
sName.send_keys("martin")
br.find_element_by_xpath("//*[@id='provider']/div[1]/div/div/div/button").click()
sleep(15)

content = br.page_source
soup = bs(content, 'lxml')

oTab = soup.find('table')
print('length of tables ', len(oTab))

table_ = oTab
body_ = table_.find_all('tr')
print('length of table records. ', len(body_))
heads = body_[0]
th = heads.find_all('th')

bodyRows_ = body_[1:]

all_rows = []

# loop through all table rows to get all table datas
sleep(3)
for row_num in range(len(bodyRows_)):
    row = []
    for row_item in bodyRows_[row_num].find_all('td'):
        stripA = re.sub("(\xa0)|(\n)|,","",row_item.text)
        row.append(stripA)

    all_rows.append(row)
    # match each record to its field name
    cols = ['Nurse Name', 'Licence No.', 'Status', 'View Details']
    df = pd.DataFrame(data=all_rows, columns=cols)

# print data
df.head()
# print(df.head())

# save nurses list to csv
time_now = datetime.now().strftime("%H:%M:%S")
time_now = time_now.replace(':','-')
time_now = time_now.replace(' ','_')
df.to_csv("nurses "+time_now+".csv", index=False)

br.quit()
