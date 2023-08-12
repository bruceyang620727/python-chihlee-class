import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0,1.0,0.05)
print(t)
y1 = np.sin(2*np.pi*t)
y2 = np.cos(2*np.pi*t)
#display(y1) #只能用在.ipynb
print(y1)
#display(y2)
print(y2)
figure1 = plt.figure(figsize=(8,4)) #figure是畫圖的圖紙
axes1 = figure1.add_subplot()
axes1.plot(y1)
axes1.plot(y2)
plt.show()