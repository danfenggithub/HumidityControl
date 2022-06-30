import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from HumidityControl.solutions.gymRoom import *

pre = "5mins/"
time_slot = 5*60
filename = ["baseline.csv", "baselinepoints.csv", "power1.csv", "power2.csv", "power3.csv", "dqn.csv",
            "pid.csv", "pid_m.csv", "our approach.csv"]

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


def numtovar(pandasList):
    return pandasList.iloc[:, 12:].apply(lambda x: np.var([i for i in x]), axis=1)


baseline = pd.read_csv(pre + filename[0])
baseline_M = pd.read_csv(pre + filename[1])
Power1 = pd.read_csv(pre + filename[2])
Power2 = pd.read_csv(pre + filename[3])
Power3 = pd.read_csv(pre + filename[4])
dqn = pd.read_csv(pre + filename[5])
pid = pd.read_csv(pre + filename[6], encoding='ISO-8859-1')
pid_m = pd.read_csv(pre + filename[7], encoding='ISO-8859-1')
our = pd.read_csv(pre + filename[8])

IfElsePowerList = numtofanpower(baseline)
IfElsePowerList_M = numtofanpower(baseline_M)
Power1PowerList = numtofanpower(Power1)
Power2PowerList = numtofanpower(Power2)
Power3PowerList = numtofanpower(Power3)
dqnPowerList = numtofanpower(dqn)
pidPowerList = numtofanpower(pid)
pidmPowerList = numtofanpower(pid_m)
ourPowerList = numtofanpower(our)

PowerList = [IfElsePowerList, IfElsePowerList_M, Power1PowerList, Power2PowerList,
             Power3PowerList, dqnPowerList, pidPowerList, pidmPowerList, ourPowerList]

IfElseRHRewardList = numtoRHReward(baseline)
IfElseRHRewardList_M = numtoRHReward(baseline_M)
Power1RHRewardList = numtoRHReward(Power1)
Power2RHRewardList = numtoRHReward(Power2)
Power3RHRewardList = numtoRHReward(Power3)
dqnRHRewardList = numtoRHReward(dqn)
pidRHRewardList = numtoRHReward(pid)
pid_mRHRewardList = numtoRHReward(pid_m)
points6RHRewardList = numtoRHReward(our)

RHvar = [numtovar(baseline), numtovar(baseline_M), numtovar(Power1), numtovar(Power2), numtovar(Power3), numtovar(dqn),
         numtovar(pid), numtovar(pid_m), numtovar(our)]

RHRewardList = [IfElseRHRewardList / 15, IfElseRHRewardList_M / 15, Power1RHRewardList / 15, Power2RHRewardList / 15,
                Power3RHRewardList / 15, dqnRHRewardList / 15, pidRHRewardList / 15, pid_mRHRewardList / 15,
                points6RHRewardList / 15]

plt.figure(1)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(15, 5), dpi=180)
ax1 = plt.subplot(111)

# Color = ["r", 'gold', 'orange', 'lightgreen', "b", "gold", "c"]
# Linesty1e = ['-', '-', '-', '-', '-', '-', '-']

Color = ["r", 'gray', 'gold', 'orange', 'lightgreen', "b", "darkblue", "chocolate", "c"]
Linesty1e = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
markers = ['o', '^', 's', 'p', '*', 'h', 'H', '+', 'x', 'X', 'D',
           'd', '|', '_']

for m in range(len(filename)):
    # x1_smooth, y1_smooth = smoothline(RHRewardList[m])
    ax1.plot(RHRewardList[m], label=filename[m].split(".")[0], color=Color[m], ls=Linesty1e[m], alpha=0.4)

ax1.set_title('不同策略的平均绝对湿度差下降曲线', fontsize=20)
ax1.set_xlabel('单位为30秒的时间片', fontsize=20)
ax1.set_ylabel('平均绝对湿度差', fontsize=20)
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.legend(loc="upper right", fontsize=20)
plt.tight_layout()
plt.show()

plt.figure(2)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(15, 5), dpi=180)
ax2 = plt.subplot(111)

PowerList1 = [pow * time_slot * 5 / 3600 for pow in PowerList]
sumPowerList = [sum(powsum) for powsum in PowerList1]
merge_data = pd.DataFrame([])
for i in range(len(RHRewardList)):
    DD = pd.DataFrame(RHRewardList[i])
    p_col = [filename[i].split('.')[0]]
    DD.columns = p_col
    merge_data = merge_data.append(DD.T)

for i in range(len(PowerList1)):
    DD = pd.DataFrame(PowerList1[i])
    p_col = [filename[i].split('.')[0]]
    DD.columns = p_col
    merge_data = merge_data.append(DD.T)

for i in range(len(RHvar)):
    DD = pd.DataFrame(RHvar[i])
    p_col = [filename[i].split('.')[0]]
    DD.columns = p_col
    merge_data = merge_data.append(DD.T)

merge_data['sum'] = merge_data.iloc[:, :].apply(lambda x: x.sum(), axis=1)
merge_data['mean'] = merge_data.iloc[:, :-1].apply(lambda x: x.mean(), axis=1)
merge_data.to_csv("result.csv", sep=',', encoding='utf-8')

for m in range(len(PowerList)):
    # print(PowerList[m].values)
    # print(PowerList[m].index)
    # PowerList[m].pop(0)
    # print(PowerList[m])
    ax2.fill_between(PowerList[m].index, PowerList[m].values, color=Color[m], step="post", alpha=0.2)
    ax2.step(PowerList[m].index, PowerList[m].values, label=filename[m].split(".")[0], color=Color[m], ls=Linesty1e[m],
             alpha=0.4, where='post')

ax2.set_title('不同策略的功率变化曲线', fontsize=20)
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

plt.bar(range(len(sumPowerList)), sumPowerList, color=Color, tick_label=[mm.split(".")[0] for mm in filename],
        alpha=0.4)
# ax3.plot(x1_smooth, y1_smooth, label=filename[m].split(".")[0], color=Color[m], ls=Linesty1e[m])
# plt.fill_between(x1_smooth, 0, y1_smooth, facecolor=Color[m], alpha=0.5)

ax3.set_title('不同策略的总功耗对比', fontsize=20)
ax3.set_xlabel('不同的策略', fontsize=20)
ax3.set_ylabel('恒湿机总功耗（KW.h）', fontsize=20)
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.tight_layout()
plt.show()
