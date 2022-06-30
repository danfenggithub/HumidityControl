import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from HumidityControl.solutions.gymRoom import *

pre = "windnoisy/"
# pre = "nowind/"

# language = "cn"
language = "us"
# us 代表英文，cn代表英文

csvpath = pre + "csv/"
savepic = pre + "pic/"
time_slot = 30
filename = ["baseline.csv", "power1.csv", "power2.csv", "power3.csv", "dqn.csv", "our approach.csv"]

if language == "cn":
    strategyName = ["CCS", "低档位", "中档位", "高档位", "DQN", "RH-rainbow"]
else:
    strategyName = ["CCS", "low setting", "medium setting", "high setting", "DQN", "RH-rainbow"]
    strategyName1 = ["CCS", "low \n setting", "medium \n setting", "high \n setting", "DQN", "RH- \n rainbow"]


def numtofanpower(pandasList):
    return pandasList.iloc[:, 6:9].apply(lambda x: sum([FanPowerFunction(i) for i in x]), axis=1)


def numtoRHReward(pandasList):
    return pandasList.iloc[:, 12:].apply(lambda x: sum([abs(i - 40) for i in x]), axis=1)


def numtovar(pandasList):
    return pandasList.iloc[:, 12:].apply(lambda x: np.var([i for i in x]), axis=1)


baseline = pd.read_csv(csvpath + filename[0])
Power1 = pd.read_csv(csvpath + filename[1])
Power2 = pd.read_csv(csvpath + filename[2])
Power3 = pd.read_csv(csvpath + filename[3])
points6 = pd.read_csv(csvpath + filename[4])
points9 = pd.read_csv(csvpath + filename[5])

IfElsePowerList = numtofanpower(baseline)
Power1PowerList = numtofanpower(Power1)
Power2PowerList = numtofanpower(Power2)
Power3PowerList = numtofanpower(Power3)
points6PowerList = numtofanpower(points6)
points9PowerList = numtofanpower(points9)

PowerList = [IfElsePowerList, Power1PowerList, Power2PowerList,
             Power3PowerList, points6PowerList,points9PowerList]

IfElseRHRewardList = numtoRHReward(baseline)
Power1RHRewardList = numtoRHReward(Power1)
Power2RHRewardList = numtoRHReward(Power2)
Power3RHRewardList = numtoRHReward(Power3)
points6RHRewardList = numtoRHReward(points6)
points9RHRewardList = numtoRHReward(points9)

RHvar = [numtovar(baseline), numtovar(Power1), numtovar(Power2), numtovar(Power3), numtovar(points6), numtovar(points9)]

RHRewardList = [IfElseRHRewardList / 21, Power1RHRewardList / 21, Power2RHRewardList / 21,
                Power3RHRewardList / 21, points6RHRewardList / 21, points9RHRewardList / 21]

plt.figure(1, figsize=(12, 5.8), dpi=180)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 设置xtick和ytick的方向：in、out、inout
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
import matplotlib.pyplot as plt



if language == "cn":
    plt.rc('font', size=17)
else:
    plt.rc('font', family='Times New Roman', size=16)
y=-0.25


ax1 = plt.subplot(1,7,(1,4))

Color = ["r", 'gold', 'orange', 'lightgreen', "b", "gold", "c"]
Linesty1e = ['-', '-', '-', '-', '-', '-', '-']
markers = ['o', '^', 's', 'p', '*', 'h', 'H', '+', 'x', 'X', 'D',
           'd', '|', '_']

for m in range(len(filename)):
    # x1_smooth, y1_smooth = smoothline(RHRewardList[m])
    # ax1.plot(RHRewardList[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.4, marker=markers[m])
    ax1.plot(RHRewardList[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.6)
if language == "cn":
    ax1.set_title('不同策略的平均绝对湿度差变化曲线', fontsize=20)
    ax1.set_xlabel('时刻（时间间隔为30秒）', fontsize=20)
    ax1.set_ylabel('平均绝对湿度差（%）', fontsize=20)
else:
    # ax1.set_title('The change curve of the average absolute humidity difference of different strategies')
    ax1.set_title('(a)', y=y)
    ax1.set_xlabel('Step (30 seconds each time interval)')
    ax1.set_ylabel('Mean absolute difference of humidity (%)')

plt.xticks()
plt.yticks()
plt.legend(loc="upper right")
# plt.tight_layout()

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
merge_data.to_csv("result.csv", sep=',', encoding='utf-8', mode='a')


ax2 = plt.subplot(1,7,(5,7))

plt.bar(range(len(sumPowerList)), sumPowerList, color=Color, tick_label=[mm for mm in strategyName1],
        alpha=0.4)

if language == "cn":
    ax2.set_title('不同策略的总功耗对比', fontsize=20)
    ax2.set_xlabel('不同的策略', fontsize=20)
    ax2.set_ylabel('恒湿机总功耗（KW.h）', fontsize=20)
else:
    # ax2.set_title('Total power consumption of different strategies')
    ax2.set_title('(b)', y=y)
    ax2.set_xlabel('Different strategies')
    ax2.set_ylabel('Energy consumption (KW.h)')
plt.xticks()
plt.yticks()

plt.tight_layout()

plt.subplots_adjust(bottom=0.19)
plt.savefig(savepic + "湿度差和总功耗合图.png")
plt.show()
