#改用自動抓取政府開放平台資料網址
import requests
import csv

url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON'
response = requests.get(url)
if response.status_code == 200:
    print('下載成功!')
    weather = response.json() #requests內有一個function叫json，可以直接將json轉為python資料結構

weather['cwbopendata']['sent'] #抓到'2023-07-23T16:42:01+08:00'，但這都不是我們要的
location = weather['cwbopendata']['dataset']['location'] #location是一個list資料結構，是我們要的，因此用變數location來接收
weather_list = [] #希望建立外部為list，而內部是dict的資料結構
for item in location: #既然location是list也就是sequence，因此可以用for in來抓資料
    city_item = {} #希望建立內部是dict的資料結構
    city_item['城市'] = item['locationName']
    city_item['起始時間'] = item['weatherElement'][1]['time'][0]['startTime'] #但由online json viewer看出weatherElement是一個索引編號，是一個list結構
    city_item['結束時間'] = item['weatherElement'][1]['time'][0]['endTime']
    city_item['最高溫度'] = float(item['weatherElement'][1]['time'][0]['parameter']['parameterName'])
    city_item['最低溫度'] = float(item['weatherElement'][2]['time'][0]['parameter']['parameterName'])
    city_item['感覺'] = item['weatherElement'][3]['time'][0]['parameter']['parameterName']
    weather_list.append(city_item)
    #print(item) #由online json viewer看出locaion下的21個地點資料都是dict

#存檔csv
with open('目前天氣.csv',mode='w',encoding='utf-8',newline='') as file:  #csv檔案需要多加一個newline=''
    fieldnames = ['城市','起始時間','結束時間','最高溫度','最低溫度','感覺']
    writer = csv.DictWriter(file,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(weather_list)