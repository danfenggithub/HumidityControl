import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from HumidityControl.solutions.gymRoom import *

pre = "csv/"

filename = ["ifelse.csv", "power1.csv", "power2.csv", "power3.csv", "rainbow1.csv"]

from scipy.interpolate import make_interp_spline


def smoothline(filen, num=1):
    filen = list(map(float, filen))
    filenx = []
    fileny = []
    for i in range(0, len(filen), num):
        filenx.append(i)
        fileny.append(np.mean(filen[i:i + num]))

    x_smooth = np.linspace(min(filenx), max(filenx), 300)
    y_smooth = make_interp_spline(filenx, fileny)(x_smooth)
    return x_smooth, y_smooth


def numtofanpower(pandasList):
    return pandasList.iloc[:, 6:9].apply(lambda x: sum([FanPowerFunction(i) for i in x]), axis=1)


def numtoRHReward(pandasList):
    return pandasList.iloc[:, 12:].apply(lambda x: sum([abs(i - 40) for i in x]), axis=1)


IfElse = pd.read_csv(pre + filename[0])
Power1 = pd.read_csv(pre + filename[1])
Power2 = pd.read_csv(pre + filename[2])
Power3 = pd.read_csv(pre + filename[3])
Rainbow = pd.read_csv(pre + filename[4])
# Rainbow1 = pd.read_csv(pre + filename[5])

IfElsePowerList = numtofanpower(IfElse)
Power1PowerList = numtofanpower(Power1)
Power2PowerList = numtofanpower(Power2)
Power3PowerList = numtofanpower(Power3)
RainbowPowerList = numtofanpower(Rainbow)
# RainbowPowerList1 = numtofanpower(Rainbow1)

PowerList = [IfElsePowerList, Power1PowerList, Power2PowerList,
             Power3PowerList, RainbowPowerList]

IfElseRHRewardList = numtoRHReward(IfElse)
Power1RHRewardList = numtoRHReward(Power1)
Power2RHRewardList = numtoRHReward(Power2)
Power3RHRewardList = numtoRHReward(Power3)
RainbowRHRewardList = numtoRHReward(Rainbow)
# RainbowRHRewardList1 = numtoRHReward(Rainbow1)

RHRewardList = [IfElseRHRewardList, Power1RHRewardList, Power2RHRewardList,
                Power3RHRewardList, RainbowRHRewardList]

plt.figure(0)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(10, 8), dpi=180)
ax1 = plt.subplot(111)

for m in range(len(filename)):
    Color = ["b", 'gold', 'orange', 'lightgreen', "r", "gold", "b"]
    Linesty1e = ['-', '-', '-', '-', '-', '-.', ':']
    x1_smooth, y1_smooth = smoothline(RHRewardList[m])
    ax1.plot(x1_smooth, y1_smooth, label=filename[m].split(".")[0], color=Color[m], ls=Linesty1e[m])

ax1.set_title('不同策略的湿度差下降曲线', fontsize=20)
ax1.set_xlabel('step数（一个step相当于30秒）', fontsize=20)
ax1.set_ylabel('21个点湿度差绝对值之和', fontsize=20)
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.legend(loc="upper right", fontsize=20)
plt.tight_layout()
plt.show()

plt.figure(1)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(10, 8), dpi=180)
ax2 = plt.subplot(111)

for m in range(len(filename)):
    Color = ["b", 'gold', 'orange', 'lightgreen', "r", "gold", "b"]
    Linesty1e = ['-', '-', '-', '-', '-', '-.', ':']
    x1_smooth, y1_smooth = smoothline(PowerList[m])
    ax2.plot(x1_smooth, y1_smooth, label=filename[m].split(".")[0], color=Color[m], ls=Linesty1e[m])
    plt.fill_between(x1_smooth, 0, y1_smooth, facecolor=Color[m], alpha=0.5)

ax2.set_title('不同策略的功耗变化曲线', fontsize=20)
ax2.set_xlabel('step数（一个step相当于30秒）', fontsize=20)
ax2.set_ylabel('恒湿机功率（kw/h）', fontsize=20)
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.legend(loc="upper right", fontsize=20)
plt.tight_layout()
plt.show()

plt.figure(3)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(10, 8), dpi=180)
ax3 = plt.subplot(111)

sumPowerList = [sum(powsum) for powsum in PowerList]

Color1 = ["gold", 'b', 'orange', 'r', "lightgreen", "gold"]
plt.bar(range(len(sumPowerList)), sumPowerList, color=Color1, tick_label=[mm.split(".")[0] for mm in filename])
# ax3.plot(x1_smooth, y1_smooth, label=filename[m].split(".")[0], color=Color[m], ls=Linesty1e[m])
# plt.fill_between(x1_smooth, 0, y1_smooth, facecolor=Color[m], alpha=0.5)

ax3.set_title('不同策略的总功耗对比', fontsize=20)
ax3.set_xlabel('不同策略', fontsize=20)
ax3.set_ylabel('恒湿机总功耗（kW）', fontsize=20)
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.tight_layout()
plt.show()
