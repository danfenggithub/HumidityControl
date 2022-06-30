import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

FILE = ["dqn/", "no_double/", "no_dueling/", "no_noisy/", "no_nstep/", "no_prioritized/", "rainbow/"]
proname = ["DQN/", "no_double/", "no_dueling/", "no_noisy/", "no_nstep/", "no_prioritized/", "RH-rainbow/"]
File = ["episode_reward_history.csv",
        "FanPower_history.csv",
        "each_episode_rewards_history.csv",
        "each_FanPower_history.csv"]

mylist = [0,1,2,3,4,5,6]

from scipy.interpolate import make_interp_spline


def smoothline(filen, findmax=False, num=40, filter=False):
    filen = filen.iloc[-1][0]
    filen = filen.split(",")
    del (filen[0])
    filen = list(map(float, filen))

    # if filter is True:
    #     filen = [float(ii) for ii in filen if ii <= -500 and ii >= -10000]
    if findmax is True:
        maxDataIndex = np.argmax(filen)
        print(maxDataIndex, np.argmin(filen))
    else:
        maxDataIndex = 0
    filenx = []
    fileny = []
    for i in range(0, 2500, num):
        filenx.append(i)
        fileny.append(np.mean(filen[i:i + num]))
    print(filenx, fileny)
    x_smooth = np.linspace(min(filenx), max(filenx), 300)
    y_smooth = make_interp_spline(filenx, fileny)(x_smooth)
    return x_smooth, y_smooth, maxDataIndex


def draw(flag):
    for nt in mylist:

        file1 = pd.read_csv(FILE[nt] + File[0], 'r', error_bad_lines=False)
        file2 = pd.read_csv(FILE[nt] + File[1], 'r', error_bad_lines=False)
        file3 = pd.read_csv(FILE[nt] + File[2], 'r', error_bad_lines=False)
        file4 = pd.read_csv(FILE[nt] + File[3], 'r', error_bad_lines=False)

        x1_smooth, y1_smooth, maxDataIndex = smoothline(file1, findmax=True, filter=True)
        x2_smooth, y2_smooth, _ = smoothline(file2)

        file3 = file3.iloc[maxDataIndex * 2].values.tolist()[0]
        file3 = file3.split(",")
        del (file3[0])
        file3 = list(map(float, file3))

        file3x = []
        file3y = file3
        for i in range(0, len(file3)):
            file3x.append(i)
        print(file3x, file3y)
        x3_smooth = np.linspace(min(file3x), max(file3x), 300)
        y3_smooth = make_interp_spline(file3x, file3y)(x3_smooth)

        file4 = file4.loc[maxDataIndex * 2].values.tolist()[0]
        file4 = file4.split(",")
        del (file4[0])
        file4 = list(map(float, file4))

        Color = ["b", 'gold', 'orange', 'lightgreen', "r", "gold", "b", "r", "gold", "b"]
        Linesty1e = ['-', '-', '-', '-', '-', '-.', ':', '-', '-.', ':']
        if flag == 1:
            ax1.plot(x1_smooth, y1_smooth, color=Color[nt], ls=Linesty1e[nt], label=proname[nt].split("/")[0])
        if flag == 2:
            ax2.plot(x2_smooth, y2_smooth, color=Color[nt], ls=Linesty1e[nt], label=proname[nt].split("/")[0])
        if flag == 3:
            ax3.plot(x3_smooth, y3_smooth, color=Color[nt], ls=Linesty1e[nt], label=proname[nt].split("/")[0])
        if flag == 4:
            ax4.plot(file4, color=Color[nt], ls=Linesty1e[nt], label=proname[nt].split("/")[0], drawstyle='steps-post')


plt.figure(0)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 设置xtick和ytick的方向：in、out、inout
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
import matplotlib.pyplot as plt
plt.rc('font',family='Times New Roman',size=8)


plt.figure(figsize=(4, 3), dpi=600)
ax1 = plt.subplot(111)
draw(1)
# ax1.set_title('每个回合的奖励总和值', fontsize=20)
# ax1.set_title('The sum of rewards for each episode')
ax1.set_xlabel('Episode')
ax1.set_ylabel('Reward')
plt.xticks()
plt.yticks()
plt.legend(loc="lower right")
plt.tight_layout()
plt.subplots_adjust(bottom=0.11,left=0.1)

plt.savefig('Fig8.tiff')

plt.show()

# plt.figure(1)
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# plt.figure(figsize=(10, 8), dpi=180)
# ax2 = plt.subplot(111)
# draw(2)
# ax2.set_title('每个回合的功耗', fontsize=20)
# ax2.set_xlabel('step', fontdict={'family': 'Times New Roman', 'size': 20})
# ax2.set_ylabel('SumFanPower', fontdict={'family': 'Times New Roman', 'size': 20})
# plt.xticks(fontproperties='Times New Roman', size=20)
# plt.yticks(fontproperties='Times New Roman', size=20)
# plt.legend(loc="upper right", fontsize=20)
# plt.tight_layout()
# plt.show()
#
# plt.figure(2)
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# plt.figure(figsize=(10, 8), dpi=180)
# ax3 = plt.subplot(111)
# draw(3)
# ax3.set_title('奖励最高的那个回合的每步step得到的回报', fontsize=20)
# ax3.set_xlabel('step', fontdict={'family': 'Times New Roman', 'size': 20})
# ax3.set_ylabel('reward', fontdict={'family': 'Times New Roman', 'size': 20})
# plt.xticks(fontproperties='Times New Roman', size=20)
# plt.yticks(fontproperties='Times New Roman', size=20)
# plt.legend(loc="lower right", fontsize=20)
# plt.tight_layout()
# plt.show()
#
# plt.figure(3)
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# plt.figure(figsize=(10, 8), dpi=180)
# ax4 = plt.subplot(111)
# draw(4)
# ax4.set_title('奖励最高的那个回合的每步step功耗', fontsize=20)
# ax4.set_xlabel('episode', fontdict={'family': 'Times New Roman', 'size': 20})
# ax4.set_ylabel('fanpower', fontdict={'family': 'Times New Roman', 'size': 20})
# plt.xticks(fontproperties='Times New Roman', size=20)
# plt.yticks(fontproperties='Times New Roman', size=20)
# plt.legend(loc="lower left", fontsize=20)
# plt.tight_layout()
plt.show()
