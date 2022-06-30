import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filename = ["nowind.csv", "wind.csv"]
nowind = pd.read_csv(filename[0], index_col=0, header=0)
wind = pd.read_csv(filename[1], index_col=0, header=0)

df = pd.DataFrame(nowind)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(20, 15), dpi=180)

df.plot.bar(alpha=0.7)

plt.title('无干扰下不同策略不同时间片的总功耗对比',fontsize=10)
plt.xlabel('不同的策略',fontsize=10)
plt.ylabel('恒湿机总功耗（KW.h）',fontsize=10)
plt.xticks(fontproperties='Times New Roman', size=10, rotation=0)
plt.yticks(fontproperties='Times New Roman', size=10)
plt.savefig('无干扰下不同策略不同时间片的总功耗对比.png')

plt.show()


plt.clf()
df = pd.DataFrame(wind)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(20, 15), dpi=180)
df.plot.bar(alpha=0.7)
plt.title('有干扰下不同策略不同时间片的总功耗对比',fontsize=10)
plt.xlabel('不同的策略',fontsize=10)
plt.ylabel('恒湿机总功耗（KW.h）',fontsize=10)
plt.xticks(fontproperties='Times New Roman', size=10, rotation=0)
plt.yticks(fontproperties='Times New Roman', size=10)
plt.savefig('有干扰下不同策略不同时间片的总功耗对比.png')
plt.show()




