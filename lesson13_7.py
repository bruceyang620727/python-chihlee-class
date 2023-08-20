import pandas as pd
import streamlit as st

current_weather = pd.read_csv('目前天氣.csv')
st.write("目前台灣天氣")
#current_weather["啟始時間"] = pd.to_datetime(current_weather["啟始時間"])
#current_weather["啟始時間"] = current_weather["啟始時間"].dt.strftime('%Y-%m-%d-%H:%M:%S')
#current_weather["結束時間"] = pd.to_datetime(current_weather["結束時間"])
#current_weather["結束時間"] = current_weather["結束時間"].dt.strftime('%Y-%m-%d-%H:%M:%S')
st.write(current_weather)