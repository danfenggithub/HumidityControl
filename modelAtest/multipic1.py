import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from HumidityControl.solutions.gymRoom import *

pre = "windnoisy/"
# pre = "nowind/"

# us 代表英文，cn代表英文
# us stands for English, and cn stands for Chinese
# language = "cn"
language = "us"

csvpath = pre + "csv/"
savepic = pre + "pic/"
time_slot = 30
point_num = 21
filename = ["baseline.csv", "baselinepoints.csv", "power1.csv", "power2.csv", "power3.csv", "dqn.csv",
            "pid.csv", "pid_m.csv", "our approach.csv"]

if language == "cn":
    strategyName = ["CCS", "CCS_M", "低档位", "中档位", "高档位", "DQN", "pid", "pid_m", "RH-rainbow"]
else:
    strategyName = ["CCS", "CCS_M", "low setting", "medium setting", "high setting", "DQN", "PID", "PID_M",
                    "RH-rainbow"]
    strategyName1 = ["CCS", "CCS_M", "low \n setting", "medium \n setting", "high \n setting", "DQN", "PID", "PID_M",
                     "RH- \n rainbow"]


def numtofanpower(pandasList):
    return pandasList.iloc[:, 6:9].apply(lambda x: sum([FanPowerFunction(i) for i in x]), axis=1)


def numtoRHReward(pandasList):
    return pandasList.iloc[:, 12:].apply(lambda x: sum([abs(i - 40) for i in x]), axis=1)


def numtovar(pandasList):
    return pandasList.iloc[:, 12:].apply(lambda x: np.var([i for i in x]), axis=1)


baseline = pd.read_csv(csvpath + filename[0], encoding='ISO-8859-1')
baseline_M = pd.read_csv(csvpath + filename[1])
Power1 = pd.read_csv(csvpath + filename[2])
Power2 = pd.read_csv(csvpath + filename[3])
Power3 = pd.read_csv(csvpath + filename[4])
dqn = pd.read_csv(csvpath + filename[5])
pid = pd.read_csv(csvpath + filename[6], encoding='ISO-8859-1')
pid_m = pd.read_csv(csvpath + filename[7], encoding='ISO-8859-1')
our = pd.read_csv(csvpath + filename[8])

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

RHRewardList = [IfElseRHRewardList / point_num, IfElseRHRewardList_M / point_num, Power1RHRewardList / point_num,
                Power2RHRewardList / point_num, Power3RHRewardList / point_num, dqnRHRewardList / point_num,
                pidRHRewardList / point_num, pid_mRHRewardList / point_num, points6RHRewardList / point_num]

plt.figure(1, figsize=(5, 3), dpi=600)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 设置xtick和ytick的方向：in、out、inout
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
import matplotlib.pyplot as plt

if language == "cn":
    plt.rc('font', size=17)
else:
    plt.rc('font', family='Times New Roman', size=12)
y = -0.25

ax1 = plt.subplot(1, 1, 1)

Color = ["r", 'gray', 'gold', 'orange', 'lightgreen', "b", "darkblue", "chocolate", "c"]
Linesty1e = ['-', '-', '-', '-', '-', '-', '-', '-', '-']
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
    # ax1.set_title('(a)', y=y)
    ax1.set_xlabel('Step (30 seconds each time interval)')
    ax1.set_ylabel('Mean absolute difference of humidity (%)')

plt.xticks()
plt.yticks()
plt.legend(loc="upper right", fontsize=9)
plt.tight_layout()
plt.savefig('Fig12.tiff')

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

if pre == "nowind/":
    steps = 20
else:
    steps = 50

lens = len(filename)
df1 = pd.DataFrame(merge_data['mean'][:lens].values, columns=['FV'], index=strategyName)
df2 = pd.DataFrame(merge_data['sum'][lens:2 * lens].values, columns=['EC'], index=strategyName)
df3 = pd.DataFrame(merge_data['mean'][2 * lens:].values, columns=['UF'], index=strategyName)
df4 = pd.DataFrame(-((df1.values / 10) * 0.9 + ((df2.values / steps * 3600 / 5 / 30 - 0.06) / 0.9) * 0.1) * steps,
                   columns=['R'], index=strategyName)
df_ = df1.join(df2).join(df3).join(df4)

df_.T.to_csv(savepic + "result.csv", sep=',', encoding='utf-8')

plt.subplots_adjust(bottom=0.14, left=0.1)
plt.savefig(savepic + "mean absolute difference of humidity and total power consumption.png")
plt.show()
