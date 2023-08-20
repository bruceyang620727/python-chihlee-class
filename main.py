import csv
import pandas as pd
import streamlit as st
import ffn
import matplotlib.pyplot as plt
import plotly.express as px
import os

st.write("""
# 股票交易價格
""")
@st.cache_data
def getStockNames()->pd.Series: #回傳pd.Series
    '''
    - 取得股票名稱
    - 透過台灣codeSearch.csv檔
    '''
    #csv_path = os.path.abspath('/lesson16/codeSearch.csv')
    local_path = "codeSearch.csv"    
    with open(local_path,encoding='utf-8',newline='') as file: #file是個物件
        next(file) #忽略第一列的標題
        csv_reader = csv.reader(file)
        stock_codes = {}
        for item in csv_reader:
            key = item[2]
            stock_codes[key] = item[3] #股票名稱
    #code_series:pd.Series是變數設定型別，可以不設定
    code_series:pd.Series = pd.Series(stock_codes) #把dictionary轉成pandas series
    return code_series

@st.cache_data #能讓function效能更好
def get_dataFrame(menu:list,start_year)->pd.DataFrame:
    stock_data = ffn.get(menu,start=start_year) #stock_data是dataframe
    return stock_data

@st.cache_data
def rename_columns_name(dataFrame:pd.DataFrame,mapping:pd.Series) -> pd.DataFrame:
    '''
    網頁欄位名稱改為中文名稱來顯示
    '''
    #print(dataFrame.columns.str[:4])
    ser1:pd.Series = mapping[dataFrame.columns.str[:4]] #抓2330前四個股票代碼
    dataFrame.columns = ser1.values 
    return dataFrame

#多重選取 / stockNames.values是股票名稱
stockNames:pd.Series = getStockNames()
stock_name_id = stockNames.index.to_numpy() + "_" + stockNames.values #ndArray陣列相加
#options是一個list，是回傳使用者多重選擇後的各股票名稱
#st.sidebar.multiselect可以在網頁上顯示sidebar以及提供各股票的下拉選擇表單
options = st.sidebar.multiselect('請選擇',
                   stock_name_id, #把index & values都放進來
                   placeholder="股票:"  
                       )
#option內的資料是1101_台泥，但是我們要給ffn的是1101.TW
names:list[str] = [] #建立符合ffn需要的股票名稱2330.TW /建立一個空的list，裡面放的是string
#因為options是個list，因此可以用for loop來一個個抓值
for name in options: 
    name_string = name.split('_')[0] #[0]代表股票代碼
    names.append(name_string+".TW")

def display_Data(dataFrame:pd.DataFrame,start_year) -> None: #沒有傳出
    '''
    顯示資料
    '''   
    st.subheader(f'{start_year}~目前的歷史資料')  #顯示標題
    st.dataframe(dataFrame) #顯示dataframe
    st.subheader(f'{start_year}~目前的線圖')
    st.line_chart(dataFrame)
    rebase:pd.DataFrame = dataFrame.rebase()
    st.subheader(f'{start_year}~目前,投資100美金的回報金額')
    st.line_chart(rebase)
    st.subheader(f'{start_year}~目前,報酬分布圖')
    #使用plotly express
    returns = dataFrame.to_returns().dropna() #to_returns是指賺了多少錢
    for name in returns.columns: #每支股票畫一張圖        
        figure = px.histogram(returns,x=name)
        st.plotly_chart(figure)
    
    #若使用matplotlib figure，顯示出來的是圖片 
    #figure = plt.figure(figsize=(10,5))
    #ax = figure.add_subplot(1,1,1)
    #returns.hist(ax=ax)
    #st.pyplot(figure) 

    
    perf = dataFrame.calc_stats()
    stats = perf.stats
    print(stats)
    stats = stats.loc[['start','end','rf','total_return','cagr','max_drawdown','mtd','three_month','six_month','one_year','three_year','five_year','ten_year']]
    #st.dataframe(stats)
    #把英文轉為中文，內容參考ffn()
    stats.index = ["起始日期","結束日期","無風險比例","總報酬率","CAGR","最大虧損","持有1個月","持有3個月","持有6個月","持有1年","持有3年","持有5年","持有10年"]
    styler = stats[2:].style.format(precision=3)
    styler.format(lambda v: f'{v*100:.3f}%')
    st.dataframe(styler,height=425)

if len(names) != 0:
    start_year = st.sidebar.selectbox("起始年份",range(2000,2023)) #起始年份選擇
    dataFrame:pd.DataFrame= get_dataFrame(names,f"{start_year}-01-01")
    dataFrame1 = rename_columns_name(dataFrame,stockNames) #要顯示在網頁前先改名字來顯示股票中文名稱
    st.sidebar.write("you selected:",start_year)
    display_Data(dataFrame1,start_year)


