#每個文件都有一個內建的變數叫做__name__
#print(__name__) #執行後會先執行進入點並跑出字串__main__，而c語言的進入點叫function main

import requests

def download_weather():
    url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON'
    response = requests.get(url)
    if response.status_code == 200:
        print('下載成功!')
        weather = response.json() #requests內有一個function叫json，可以直接將json轉為python資料結構
        return weather
    else:
        print('下載失敗!')
        return False
        

def main():
    print("main function開始執行!")
    #下載json檔
    weather = download_weather() #download_weather內所使用的weather只能在該函式內使用，故不會與此處的weather衝突

    if weather != False:
        print('下載完畢!')
    else:
        print('應用程式下載失敗')
        return

if __name__ == '__main__':
    main()