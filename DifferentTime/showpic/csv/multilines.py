import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from HumidityControl.solutions.gymRoom import *

flag = 0

if flag == 0:
    pre = "nowind/"
    select = "multi/nowind.csv"
else:
    pre = "windnoisy/"
    select = "multi/wind.csv"

language = "us"
# language = "us"
# us 代表英文，cn代表英文

d = -0.28

mins = ["1mins/", "3mins/", "5mins/"]
# mins = ["1mins/"]

filename = ["baseline.csv", "baselinepoints.csv", "power1.csv", "power2.csv", "power3.csv", "dqn.csv",
            "pid.csv", "pid_m.csv", "our approach.csv"]

if language == "cn":
    strategyName = ["CCS", "CCS_M", "低档位", "中档位", "高档位", "DQN", "pid", "pid_m", "RH-rainbow"]
else:
    strategyName = ["CCS", "CCS_M", "low setting", "medium setting", "high setting", "DQN", "PID", "PID_M",
                    "RH-rainbow"]
    strategyName1 = ["CCS", "CCS_M", "low \n setting", "medium \n setting", "high \n setting", "DQN", "PID", "PID_M",
                     "RH- \n rainbow"]


# df = pd.DataFrame(pd.read_csv(select, index_col=0, header=0))


def numtoRHReward(pandasList):
    return pandasList.iloc[:, 12:].apply(lambda x: sum([abs(i - 40) for i in x]), axis=1)


def getdata(i):
    baseline = pd.read_csv(pre + mins[i] + filename[0])
    baseline_M = pd.read_csv(pre + mins[i] + filename[1])
    Power1 = pd.read_csv(pre + mins[i] + filename[2])
    Power2 = pd.read_csv(pre + mins[i] + filename[3])
    Power3 = pd.read_csv(pre + mins[i] + filename[4])
    dqn = pd.read_csv(pre + mins[i] +filename[5])
    pid = pd.read_csv(pre + mins[i] + filename[6], encoding='ISO-8859-1')
    pid_m = pd.read_csv(pre + mins[i] + filename[7], encoding='ISO-8859-1')
    our = pd.read_csv(pre + mins[i] + filename[8])

    IfElseRHRewardList = numtoRHReward(baseline)
    IfElseRHRewardList_M = numtoRHReward(baseline_M)
    Power1RHRewardList = numtoRHReward(Power1)
    Power2RHRewardList = numtoRHReward(Power2)
    Power3RHRewardList = numtoRHReward(Power3)
    dqnRHRewardList = numtoRHReward(dqn)
    pidRHRewardList = numtoRHReward(pid)
    pid_mRHRewardList = numtoRHReward(pid_m)
    points6RHRewardList = numtoRHReward(our)

    RHRewardList = [IfElseRHRewardList / 15, IfElseRHRewardList_M / 15, Power1RHRewardList / 15,
                    Power2RHRewardList / 15,
                    Power3RHRewardList / 15, dqnRHRewardList / 15, pidRHRewardList / 15, pid_mRHRewardList / 15,
                    points6RHRewardList / 15]

    return RHRewardList


# Color = ["r", 'gold', 'orange', 'lightgreen', "b", "indigo", "c", "black"]
# Linesty1e = ['-', '-', '-', '-', '-', '-', '-', '-']
# markers = ['o', '^', 's', 'p', '*', 'h', 'H', '+', 'x', 'X', 'D', 'd', '|', '_']


Color = ["r", 'gray', 'gold', 'orange', 'lightgreen', "b", "darkblue", "chocolate", "c"]
Linesty1e = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
markers = ['o', '^', 's', 'p', '*', 'h', 'H', '+', 'x', 'X', 'D',
           'd', '|', '_']

plt.figure(1, figsize=(12, 3), dpi=600)
# 设置xtick和ytick的方向：in、out、inout
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
import matplotlib.pyplot as plt

if language == "cn":
    plt.rc('font', size=10)
else:
    plt.rc('font', family='Times New Roman', size=11)

ax1 = plt.subplot(131)

for m in range(len(filename)):
    # ax1.plot(getdata(0)[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.4, marker=markers[m])
    ax1.plot(getdata(0)[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.4)

if language == "cn":
    ax1.set_title('不同策略的平均绝对湿度差变化曲线', fontsize=10)
    ax1.set_xlabel('时刻（时间间隔为1分钟）', fontsize=10)
    ax1.set_ylabel('平均绝对湿度差（%）', fontsize=10)
else:
    # ax1.set_title('The change curve of the average absolute humidity difference of different strategies')
    ax1.set_title('(a)', y=d)
    ax1.set_xlabel('Step (1 minute each time interval)')
    ax1.set_ylabel('Mean absolute difference of humidity (%)')

plt.xticks()
plt.yticks()
plt.legend(loc="upper right", fontsize=8)
plt.tight_layout()

ax2 = plt.subplot(132)

for m in range(len(filename)):
    # ax2.plot(getdata(1)[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.4, marker=markers[m])
    ax2.plot(getdata(1)[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.4)

if language == "cn":
    ax2.set_title('不同策略的平均绝对湿度差下降曲线', fontsize=10)
    ax2.set_xlabel('时刻（时间间隔为3分钟）', fontsize=10)
    ax2.set_ylabel('平均绝对湿度差（%）', fontsize=10)
else:
    # ax2.set_title('The change curve of the average absolute humidity difference of different strategies')
    ax2.set_title('(b)', y=d)
    ax2.set_xlabel('Step (3 minute each time interval)')
    ax2.set_ylabel('Mean absolute difference of humidity (%)')

plt.xticks()
plt.yticks()
plt.legend(loc="upper right", fontsize=8)
plt.tight_layout()

ax3 = plt.subplot(133)

for m in range(len(filename)):
    # ax3.plot(getdata(2)[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.4, marker=markers[m])
    ax3.plot(getdata(2)[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.4)

if language == "cn":
    ax3.set_title('不同策略的平均绝对湿度差下降曲线', fontsize=10)
    ax3.set_xlabel('时刻（时间间隔为5分钟）', fontsize=10)
    ax3.set_ylabel('平均绝对湿度差（%）', fontsize=10)
else:
    # ax3.set_title('The change curve of the average absolute humidity difference of different strategies')
    ax3.set_title('(c)', y=d)
    ax3.set_xlabel('Step (5 minute each time interval)')
    ax3.set_ylabel('Mean absolute difference of humidity (%)')

num1 = 1.01
num2 = 0
num3 = 3
num4 = 0

plt.xticks()
plt.yticks()
plt.legend(loc="upper right", fontsize=8)
# plt.legend(bbox_to_anchor=(num1, num2), loc=num3, borderaxespad=num4, fontsize=10)
plt.tight_layout()
plt.subplots_adjust(bottom=0.19, left=0.05)
plt.savefig('Fig18.tiff')

# ax4 = plt.subplot(224)
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
#
# # ax4.bar(df.index, df['1 min'], label='1 min')
# # ax4.bar(df.index, df['3 mins'], label='3 mins')
# # ax4.bar(df.index, df['5 mins'], label='5 mins')
# # ax4.bar(df)
# # df.plot.bar(alpha=0.7)
# from matplotlib import pyplot as plt
#
# x = np.arange(len(df)) + 1
# # hatchs = ["/", "o", ".", "\\", "*"]
# # plt.bar(x - 0.2, df['CCS'], alpha=0.6, width=0.1, label=strategyName[0], color=Color[0], hatch=hatchs[0],edgecolor='black')
# # plt.bar(x - 0.1, df['low gear'], alpha=0.6, width=0.1, label=strategyName[1], lw=1, color=Color[1], hatch=hatchs[1],edgecolor='black')
# # plt.bar(x, df['middle gear'], alpha=0.6, width=0.1, label=strategyName[2], lw=1, color=Color[2], hatch=hatchs[2],edgecolor='black')
# # plt.bar(x + 0.1, df['high gear'], alpha=0.6, width=0.1, label=strategyName[3], color=Color[3], hatch=hatchs[3],edgecolor='black')
# # plt.bar(x + 0.2, df['RH-rainbow'], alpha=0.6, width=0.1, label=strategyName[4], lw=1, color=Color[4], hatch=hatchs[4],edgecolor='black')
#
# plt.bar(x - 0.2, df['CCS'], alpha=0.6, width=0.1, label=strategyName[0], color=Color[0], edgecolor='black')
# plt.bar(x - 0.1, df['low gear'], alpha=0.6, width=0.1, label=strategyName[1], lw=1, color=Color[1], edgecolor='black')
# plt.bar(x, df['middle gear'], alpha=0.6, width=0.1, label=strategyName[2], lw=1, color=Color[2], edgecolor='black')
# plt.bar(x + 0.1, df['high gear'], alpha=0.6, width=0.1, label=strategyName[3], color=Color[3], edgecolor='black')
# plt.bar(x + 0.2, df['RH-rainbow'], alpha=0.6, width=0.1, label=strategyName[4], lw=1, color=Color[4], edgecolor='black')
#
# plt.legend(loc="upper left")
#
# if language == "cn":
#     plt.title('不同策略不同时间片的总功耗对比', fontsize=10)
#     plt.xlabel('不同的策略', fontsize=10)
#     plt.ylabel('恒湿机总功耗（KW.h）', fontsize=10)
# else:
#     plt.title('(d)', y=d)
#     plt.xlabel('Different time interval ')
#     plt.ylabel('Energy consumption(kw.h)')
#
# plt.xticks([1, 2, 3], ['1min', '3mins', '5mins'])
#
# plt.yticks()
# plt.savefig(pre + '不同策略不同时间片的总功耗对比.png')
plt.show()
