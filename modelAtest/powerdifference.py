import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from HumidityControl.solutions.gymRoom import *

pre = "windnoisy/"
csvpath = pre + "csv/"
savepic = pre + "pic/"
time_slot = 30
filename = ["baseline.csv", "power1.csv", "power2.csv", "power3.csv", "our approach.csv"]
strategyName = ["CCS", "low gear", "middle gear", "high gear", "RH-rainbow"]

from scipy.interpolate import make_interp_spline


# def smoothline(filen, num=1):
#     filen = list(map(float, filen))
#     filenx = []
#     fileny = []
#     for i in range(0, len(filen), num):
#         filenx.append(i)
#         fileny.append(np.mean(filen[i:i + num]))
#
#     x_smooth = np.linspace(min(filenx), max(filenx), 300)
#     y_smooth = make_interp_spline(filenx, fileny)(x_smooth)
#     return x_smooth, y_smooth


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
# points9 = pd.read_csv(csvpath + filename[5])

IfElsePowerList = numtofanpower(baseline)
Power1PowerList = numtofanpower(Power1)
Power2PowerList = numtofanpower(Power2)
Power3PowerList = numtofanpower(Power3)
points6PowerList = numtofanpower(points6)
# points9PowerList = numtofanpower(points9)

PowerList = [IfElsePowerList, Power1PowerList, Power2PowerList,
             Power3PowerList, points6PowerList]

IfElseRHRewardList = numtoRHReward(baseline)
Power1RHRewardList = numtoRHReward(Power1)
Power2RHRewardList = numtoRHReward(Power2)
Power3RHRewardList = numtoRHReward(Power3)
points6RHRewardList = numtoRHReward(points6)
# points9RHRewardList = numtoRHReward(points9)

RHvar = [numtovar(baseline), numtovar(Power1), numtovar(Power2), numtovar(Power3), numtovar(points6)]

RHRewardList = [IfElseRHRewardList / 21, Power1RHRewardList / 21, Power2RHRewardList / 21,
                Power3RHRewardList / 21, points6RHRewardList / 21]

plt.figure(1)
plt.rcParams['font.sans-serif'] = ['SimHei']  # ??????????????????????????????
plt.rcParams['axes.unicode_minus'] = False  # ????????????????????????
plt.figure(figsize=(15, 5), dpi=180)
ax1 = plt.subplot(111)

Color = ["r", 'gold', 'orange', 'lightgreen', "b", "gold", "c"]
Linesty1e = ['-', '-', '-', '-', '-', '-', '-']

for m in range(len(filename)):
    # x1_smooth, y1_smooth = smoothline(RHRewardList[m])
    ax1.plot(RHRewardList[m], label=strategyName[m], color=Color[m], ls=Linesty1e[m], alpha=0.4)

ax1.set_title('????????????????????????????????????????????????', fontsize=20)
ax1.set_xlabel('?????????30???????????????', fontsize=20)
ax1.set_ylabel('?????????????????????', fontsize=20)
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.legend(loc="upper right", fontsize=20)
plt.tight_layout()
plt.savefig(savepic + "????????????????????????????????????????????????.png")
# plt.show()

plt.figure(2)
plt.rcParams['font.sans-serif'] = ['SimHei']  # ??????????????????????????????
plt.rcParams['axes.unicode_minus'] = False  # ????????????????????????
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
merge_data.to_csv(savepic + "result.csv", sep=',', encoding='utf-8')

for m in range(len(PowerList)):
    # print(PowerList[m].values)
    # print(PowerList[m].index)
    # PowerList[m].pop(0)
    # print(PowerList[m])
    ax2.fill_between(PowerList[m].index, PowerList[m].values, color=Color[m], step="post", alpha=0.2)
    ax2.step(PowerList[m].index, PowerList[m].values, label=strategyName[m], color=Color[m], ls=Linesty1e[m],
             alpha=0.4, where='post')

ax2.set_title('?????????????????????????????????', fontsize=20)
ax2.set_xlabel('?????????30???????????????', fontsize=20)
ax2.set_ylabel('??????????????????kw/h???', fontsize=20)
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.legend(loc="upper right", fontsize=20)
plt.tight_layout()
plt.savefig(savepic + "?????????????????????????????????.png")
# plt.show()

plt.figure(3)
plt.rcParams['font.sans-serif'] = ['SimHei']  # ??????????????????????????????
plt.rcParams['axes.unicode_minus'] = False  # ????????????????????????
plt.figure(figsize=(10, 8), dpi=180)
ax3 = plt.subplot(111)

plt.bar(range(len(sumPowerList)), sumPowerList, color=Color, tick_label=[mm for mm in strategyName],
        alpha=0.4)

ax3.set_title('??????????????????????????????', fontsize=20)
ax3.set_xlabel('???????????????', fontsize=20)
ax3.set_ylabel('?????????????????????KW.h???', fontsize=20)
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.tight_layout()
plt.savefig(savepic + "??????????????????????????????.png")
# plt.show()
