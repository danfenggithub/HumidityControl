import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from HumidityControl.solutions.gymRoom import *

pre = "csv/"  # Single interference
#
# pre = "csv100/"  # Multiple interference

# language = "cn"
language = "us"

filename = ["baseline.csv", "baselinepoints.csv", "power1.csv", "power2.csv", "power3.csv", "dqn_15.csv",
            "pid.csv", "pid_m.csv", "6points.csv", "9points.csv", "15points.csv"]

if language == "cn":
    strategyName = ["CCS", "CCS_M", "低档位", "中档位", "高档位", "DQN", "PID", "PID_M", "6个点(RH-rainbow)", "9个点(RH-rainbow)",
                    "15个点(RH-rainbow)"]
else:
    strategyName = ["CCS", "CCS_M", "low setting", "medium setting", "high setting", "DQN", "PID", "PID_M",
                    "6 points(RH-rainbow)", "9 points (RH-rainbow)", "15 points (RH-rainbow)"]

    strategyName1 = ["CCS", "CCS_M", "low \n setting", "medium \n setting", "high \n setting", "DQN", "PID", "PID_M",
                     "6 points(RH-rainbow)", "9 points (RH-rainbow)", "15 points (RH-rainbow)"]

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


filename = ["baseline.csv", "baselinepoints.csv", "power1.csv", "power2.csv", "power3.csv", "dqn_15.csv",
            "pid.csv", "pid_m.csv", "6points.csv", "9points.csv", "15points.csv"]

baseline = pd.read_csv(pre + filename[0])
baseline_M = pd.read_csv(pre + filename[1])
Power1 = pd.read_csv(pre + filename[2])
Power2 = pd.read_csv(pre + filename[3])
Power3 = pd.read_csv(pre + filename[4])
dqn = pd.read_csv(pre + filename[5])
pid = pd.read_csv(pre + filename[6], encoding='ISO-8859-1')
pid_m = pd.read_csv(pre + filename[7], encoding='ISO-8859-1')
points6 = pd.read_csv(pre + filename[8])
points9 = pd.read_csv(pre + filename[9])
points15 = pd.read_csv(pre + filename[10])

IfElsePowerList = numtofanpower(baseline)
IfElsePowerList_M = numtofanpower(baseline_M)
Power1PowerList = numtofanpower(Power1)
Power2PowerList = numtofanpower(Power2)
Power3PowerList = numtofanpower(Power3)
dqnPowerList = numtofanpower(dqn)
pidPowerList = numtofanpower(pid)
pid_mPowerList = numtofanpower(pid_m)
points6PowerList = numtofanpower(points6)
points9PowerList = numtofanpower(points9)
points15PowerList = numtofanpower(points15)

PowerList = [IfElsePowerList, IfElsePowerList_M, Power1PowerList, Power2PowerList,
             Power3PowerList, dqnPowerList, pidPowerList, pid_mPowerList, points6PowerList, points9PowerList,
             points15PowerList]

IfElseRHRewardList = numtoRHReward(baseline)
IfElseRHRewardList_M = numtoRHReward(baseline_M)
Power1RHRewardList = numtoRHReward(Power1)
Power2RHRewardList = numtoRHReward(Power2)
Power3RHRewardList = numtoRHReward(Power3)
dqnRHRewardList = numtoRHReward(dqn)
pidRHRewardList = numtoRHReward(pid)
pid_mRHRewardList = numtoRHReward(pid_m)
points6RHRewardList = numtoRHReward(points6)
points9RHRewardList = numtoRHReward(points9)
points15RHRewardList = numtoRHReward(points15)

RHvar = [numtovar(baseline), numtovar(baseline_M), numtovar(Power1), numtovar(Power2), numtovar(Power3),
         numtovar(dqn), numtovar(pid), numtovar(pid_m), numtovar(points6), numtovar(points9), numtovar(points15)]

RHRewardList = [IfElseRHRewardList / 9, IfElseRHRewardList_M / 9, Power1RHRewardList / 15, Power2RHRewardList / 15,
                Power3RHRewardList / 15, dqnRHRewardList / 15, pidRHRewardList / 9, pid_mRHRewardList / 9,
                points6RHRewardList / 6, points9RHRewardList / 9, points15RHRewardList / 15]

plt.figure(1)

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import matplotlib.pyplot as plt

if language == "cn":
    plt.rc('font', size=17)
else:
    plt.rc('font', family='Times New Roman', size=12)

plt.figure(figsize=(8, 3), dpi=600)

ax1 = plt.subplot(111)

Color = ["r", 'gray', 'gold', 'orange', 'lightgreen', "b", "darkblue", "chocolate", "c", "m", "pink"]
Linesty1e = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
markers = ['o', '^', 's', 'p', '*', 'h', 'H', '+', 'x', 'X', 'D',
           'd', '|', '_']

for m in range(len(filename)):
    # x1_smooth, y1_smooth = smoothline(RHRewardList[m])
    # ax1.plot(RHRewardList[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.4, marker=markers[m])
    ax1.plot(RHRewardList[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.4)

if language == "cn":
    ax1.set_title('不同策略的平均绝对湿度差变化曲线')
    ax1.set_xlabel('时刻（时间间隔为30秒）')
    ax1.set_ylabel('平均绝对湿度差（%）')
else:
    # ax1.set_title('The change curve of the average absolute humidity difference of different strategies')
    # ax1.set_title('(a)', y=-0.25)
    ax1.set_xlabel('Step (30 seconds each time interval)')
    ax1.set_ylabel('Mean absolute difference of humidity (%)')

plt.xticks(fontproperties='Times New Roman')
plt.yticks(fontproperties='Times New Roman')
# plt.legend(loc="upper right", fontsize=8)

num1 = 1.02
num2 = 0
num3 = 3
num4 = 0

plt.legend(bbox_to_anchor=(num1, num2), loc=num3, borderaxespad=num4, fontsize=7)
plt.tight_layout()
plt.subplots_adjust(bottom=0.14, left=0.1)

plt.savefig('Fig16.tiff')

plt.show()

plt.figure(2)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# plt.figure(figsize=(15, 5), dpi=180)
ax2 = plt.subplot(111)

time_slot = 30

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
# merge_data.to_csv("result.csv", sep=',', encoding='utf-8')

if pre == "csv100/":
    steps = 100
else:
    steps = 50

lens = len(filename)
df1 = pd.DataFrame(merge_data['mean'][:lens].values, columns=['FV'], index=strategyName)
df2 = pd.DataFrame(merge_data['sum'][lens:2 * lens].values, columns=['EC'], index=strategyName)
df3 = pd.DataFrame(merge_data['mean'][2 * lens:].values, columns=['UF'], index=strategyName)
df4 = pd.DataFrame(-((df1.values/10)*0.9+((df2.values/steps*3600/5/30-0.06)/0.9)*0.1)*steps, columns=['R'], index=strategyName)
df_ = df1.join(df2).join(df3).join(df4)
savepic = pre + "pic/"
df_.T.to_csv(savepic + "result.csv", sep=',', encoding='utf-8')