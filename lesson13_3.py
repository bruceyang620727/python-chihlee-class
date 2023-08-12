import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

value = st.slider("三角函數",min_value=0, max_value=10)
t = np.arange(0.,5,0.05)
#print(t)
#st.write(t)
y1 = np.sin(np.random.randn()*value*np.pi*t)
y1 = np.cos(np.random.randn()*value*np.pi*t)
#display(y1) #只能用在.ipynb
#print(y1) #即使改成print，仍舊無法顯示在終端機上
#display(y2)
#print(y2)
#st.write(y1)
#st.write(y2)
figure1 = plt.figure(figsize=(8,4)) #figure是畫圖的圖紙
axes1 = figure1.add_subplot()
axes1.plot(y1)
axes1.plot(y2)
#plt.show()
st.write(figure1) #輸出至瀏覽器
