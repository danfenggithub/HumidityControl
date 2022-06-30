import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

lr = ["0.005/", "0.008/", "0.01/"]
proname = ["dqn/", "dqn_double/", "dqn_dueling/", "dqn_noisy/", "dqn_nstep/", "dqn_prioritized/", "dqn_rainbow/"]

li = 6

File = ["episode_reward_history.csv",
        "FanPower_history.csv",
        "each_episode_rewards_history.csv",
        "each_FanPower_history.csv"]

from scipy.interpolate import make_interp_spline


def smoothline(filen, findmax=False, num=40):
    filen = filen.iloc[-1][0]
    filen = filen.split(",")
    del (filen[0])
    filen = list(map(float, filen))

    filen = [float(ii) for ii in filen if ii <= 10000 and ii >= -10000]
    if findmax is True:
        maxDataIndex = np.argmax(filen)
        print(maxDataIndex, np.argmin(filen))
    else:
        maxDataIndex = 0
    filenx = []
    fileny = []
    for i in range(0, len(filen), num):
        filenx.append(i)
        fileny.append(np.mean(filen[i:i + num]))

    x_smooth = np.linspace(min(filenx), max(filenx), 300)
    y_smooth = make_interp_spline(filenx, fileny)(x_smooth)
    return x_smooth, y_smooth, maxDataIndex


def draw(flag):
    for nt in range(3):

        file1 = pd.read_csv(lr[nt] + proname[li] + File[0], 'r', error_bad_lines=False)
        file2 = pd.read_csv(lr[nt] + proname[li] + File[1], 'r', error_bad_lines=False)
        file3 = pd.read_csv(lr[nt] + proname[li] + File[2], 'r', error_bad_lines=False)
        file4 = pd.read_csv(lr[nt] + proname[li] + File[3], 'r', error_bad_lines=False)

        x1_smooth, y1_smooth, maxDataIndex = smoothline(file1, findmax=True)
        x2_smooth, y2_smooth, _ = smoothline(file2)

        file3 = file3.iloc[maxDataIndex * 2].values.tolist()[0]
        file3 = file3.split(",")
        del (file3[0])
        file3 = list(map(float, file3))

        file3x = []
        file3y = file3
        for i in range(0, len(file3)):
            file3x.append(i)

        x3_smooth = np.linspace(min(file3x), max(file3x), 300)
        y3_smooth = make_interp_spline(file3x, file3y)(x3_smooth)

        file4 = file4.loc[maxDataIndex * 2].values.tolist()[0]
        file4 = file4.split(",")
        del (file4[0])
        file4 = list(map(float, file4))

        Color = ["b", 'gold', 'orange', 'lightgreen', "r", "gold", "b"]
        Linesty1e = ['-', '-', '-', '-', '-', '-.', ':']
        if flag == 1:
            ax1.plot(x1_smooth, y1_smooth, color=Color[nt], ls=Linesty1e[nt],
                     label=lr[nt].split("/")[0] + " " + proname[li].split("/")[0])
        if flag == 2:
            ax2.plot(x2_smooth, y2_smooth, color=Color[nt], ls=Linesty1e[nt],
                     label=lr[nt].split("/")[0] + " " + proname[li].split("/")[0])
        if flag == 3:
            ax3.plot(x3_smooth, y3_smooth, color=Color[nt], ls=Linesty1e[nt],
                     label=lr[nt].split("/")[0] + " " + proname[li].split("/")[0])
        if flag == 4:
            ax4.plot(file4, color=Color[nt], ls=Linesty1e[nt],
                     label=lr[nt].split("/")[0] + " " + proname[li].split("/")[0], drawstyle='steps-post')


plt.figure(0)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(10, 8), dpi=180)
ax1 = plt.subplot(111)
draw(1)
ax1.set_title('每个回合的奖励总和值', fontsize=20)
ax1.set_xlabel('episode', fontdict={'family': 'Times New Roman', 'size': 20})
ax1.set_ylabel('reward', fontdict={'family': 'Times New Roman', 'size': 20})
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.legend(loc="lower right", fontsize=20)
plt.tight_layout()
plt.show()

plt.figure(1)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(10, 8), dpi=180)
ax2 = plt.subplot(111)
draw(2)
ax2.set_title('每个回合的功耗', fontsize=20)
ax2.set_xlabel('step', fontdict={'family': 'Times New Roman', 'size': 20})
ax2.set_ylabel('SumFanPower', fontdict={'family': 'Times New Roman', 'size': 20})
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.legend(loc="upper right", fontsize=20)
plt.tight_layout()
plt.show()

plt.figure(2)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(10, 8), dpi=180)
ax3 = plt.subplot(111)
draw(3)
ax3.set_title('奖励最高的那个回合的每步step得到的回报', fontsize=20)
ax3.set_xlabel('step', fontdict={'family': 'Times New Roman', 'size': 20})
ax3.set_ylabel('reward', fontdict={'family': 'Times New Roman', 'size': 20})
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.legend(loc="lower right", fontsize=20)
plt.tight_layout()
plt.show()

plt.figure(3)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.figure(figsize=(10, 8), dpi=180)
ax4 = plt.subplot(111)
draw(4)
ax4.set_title('奖励最高的那个回合的每步step功耗', fontsize=20)
ax4.set_xlabel('episode', fontdict={'family': 'Times New Roman', 'size': 20})
ax4.set_ylabel('fanpower', fontdict={'family': 'Times New Roman', 'size': 20})
plt.xticks(fontproperties='Times New Roman', size=20)
plt.yticks(fontproperties='Times New Roman', size=20)
plt.legend(loc="lower left", fontsize=20)
plt.tight_layout()
plt.show()
