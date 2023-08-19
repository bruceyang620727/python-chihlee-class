import requests
import csv
from datetime import datetime
import pytz
import os
import pandas as pd
import streamlit as st

def download_data()->dict: #傳出dict
    url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON'

    response = requests.get(url) #response是實體
    if response.status_code == 200:
        print('下載成功')
    return response.json()

def jsonDict_csvList(json)->list[dict]:
    '''
    - 由online json viewer看出locaion下的21個地點資料都是dict
    - 傳入json的資料結構，並取出需要的資料
    - 把json資料結構轉成python list，而內部是dict結構
    '''
    location = json['cwbopendata']['dataset']['location'] #location是一個list資料結構，是我們要的，因此用變數location來接收
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
    return weather_list

def save_csv(data:list[dict],fileName)->bool:
    '''
    - 將list[dict]儲存
    - 參數fileName要儲存的檔案名
    '''
    with open(fileName,mode='w',encoding='utf-8',newline='') as file:  #csv檔案需要多加一個newline=''
        fieldnames = ['城市','起始時間','結束時間','最高溫度','最低溫度','感覺']
        writer = csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader() #header就是'城市','起始時間','結束時間','最高溫度','最低溫度','感覺'
        writer.writerows(data)
        return True

def get_csvName()->str:
    '''
    - 取得台灣目前year-month-day.csv
    '''
    taiwan_timezone = pytz.timezone('Asia/Taipei')
    current_date = datetime.now(taiwan_timezone)
    fileName = f"{current_date.year}-{current_date.month}-{current_date.day}.csv"
    return fileName

def get_fileName_path()->str:
    csv_file_name = get_csvName()
    current_cwd = os.path.abspath(os.getcwd())
    abs_file_path = os.path.join(current_cwd,'data',csv_file_name)
    return abs_file_path

def check_file_exist()->bool:
    abs_file_path = get_fileName_path()
    if os.path.exists(abs_file_path):
        return True
    else:
        return False


if not check_file_exist():
    print('檔案不存在')
    json_data = download_data()
    csv_list = jsonDict_csvList(json_data)
    is_save = save_csv(csv_list,get_fileName_path())
    if is_save:
        print('存檔成功')

file_path = get_fileName_path()
dataFrame = pd.read_csv(file_path)
dataFrame['起始時間'] = pd.to_datetime(dataFrame['起始時間']) #把字串變成datetime時間物件
dataFrame['結束時間'] = pd.to_datetime(dataFrame['結束時間']) #把字串變成datetime時間物件
dataFrame['起始時間'] = dataFrame['起始時間'].dt.strftime('%Y-%m-%d日-%H點') #輸出又變成字串series
dataFrame['結束時間'] = dataFrame['結束時間'].dt.strftime('%Y-%m-%d日-%H點') #輸出又變成字串series
dataFrame['最高溫度'] = dataFrame['最高溫度'].astype(int) #將字串轉為int
dataFrame['最低溫度'] = dataFrame['最低溫度'].astype(int) #將字串轉為int
#更改外觀樣式
style = dataFrame.style.highlight_max(subset='最高溫度',axis=0,props='color:white;background-color:red') #傳出dataframe的style
style = style.highlight_max(subset='最低溫度',axis=0,props='color:white;background-color:blue')
#顯示標題
st.title("台灣各縣市氣候:")
st.subheader("攝氏")
#顯非DataFrame
st.dataframe(style,width=800,height=900) #顯示上面傳出的style

st.line_chart(dataFrame,x='城市',y=['最高溫度','最低溫度'])

st.bar_chart(dataFrame,x='城市',y=['最高溫度','最低溫度'])