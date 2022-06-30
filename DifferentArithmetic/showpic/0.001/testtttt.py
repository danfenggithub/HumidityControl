import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

proname = ["dqn/", "no_double/", "no_dueling/", "no_noisy/", "no_nstep/", "no_prioritized/", "train_15points/"]
File = ["episode_reward_history.csv",
        "FanPower_history.csv",
        "each_episode_rewards_history.csv",
        "each_FanPower_history.csv"]
kkl = range(0,1)
from scipy.interpolate import make_interp_spline

plt.figure(0)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

plt.figure(figsize=(10, 10), dpi=480)
ax1 = plt.subplot(221)
ax2 = plt.subplot(222)
ax3 = plt.subplot(223)
ax4 = plt.subplot(224)


def smoothline(filen, findmax=False, filter=False):
    filen = filen.iloc[-1][0]
    filen = filen.split(",")
    del (filen[0])
    filen = list(map(float, filen))
    # if filter is True:
    #     filen = [float(ii) for ii in filen if ii <= -530 and ii >= -10000]

    if findmax is True:
        maxDataIndex = np.argmax(filen)
        print(maxDataIndex)
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


for nt in kkl:

    file1 = pd.read_csv(proname[nt] + File[0], 'r', error_bad_lines=False)
    file2 = pd.read_csv(proname[nt] + File[1], 'r', error_bad_lines=False)
    file3 = pd.read_csv(proname[nt] + File[2], 'r', error_bad_lines=False)
    file4 = pd.read_csv(proname[nt] + File[3], 'r', error_bad_lines=False)

    num = 10

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

    x3_smooth = np.linspace(min(file3x), max(file3x), 300)
    print(len(x3_smooth), file3x, file3y)
    y3_smooth = make_interp_spline(file3x, file3y)(x3_smooth)

    file4 = file4.loc[maxDataIndex * 2].values.tolist()[0]
    file4 = file4.split(",")
    del (file4[0])
    file4 = list(map(float, file4))

    Color = ["b", 'gold', 'orange', 'lightgreen', "r", "b", "b", 'gold', 'orange', 'lightgreen', "r"]
    Linesty1e = ['-', '-.', '-', '-', '-', '-.', ':', '-.', '-', '-', '-']
    Marker = ['*']
    ax1.plot(x1_smooth, y1_smooth, color=Color[nt], ls=Linesty1e[nt])
    ax2.plot(x2_smooth, y2_smooth, color=Color[nt], ls=Linesty1e[nt])
    ax3.plot(x3_smooth, y3_smooth, color=Color[nt], ls=Linesty1e[nt])
    ax4.plot(file4, color=Color[nt], drawstyle='steps-post', ls=Linesty1e[nt])

ax1.set_title('每个回合的奖励总和值')
ax1.set_xlabel('episode')
ax1.set_ylabel('reward')
plt.tight_layout()

# ax2.set_title('每个回合的功耗')
# ax2.set_xlabel('step')
# ax2.set_ylabel('SumFanPower')
# plt.tight_layout()

ax3.set_title('奖励最高的那个回合的每步step得到的回报')
ax3.set_xlabel('step')
ax3.set_ylabel('reward')
plt.tight_layout()

ax4.set_title('奖励最高的那个回合的每步step功耗')
ax4.set_xlabel('episode')
ax4.set_ylabel('fanpower')
plt.tight_layout()

plt.show()
