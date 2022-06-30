import pandas as pd
import numpy as np
import tensorflow as tf
import shutil
from .memories import VanillaMemory
from .agents import DQNAgent
from .gymRoom import *
from .utils import *
from .gymProfile import *

import subprocess
import threading


def thread1():
    # 在Linux后台挂载 starccm+服务器
    subprocess.call("cd javafile && " + start_starccm_server, shell=True)


def thread2():
    # 线程2是后台连续执行Java宏命令，每一轮循环代表一个回合
    for i in range(100000):
        subprocess.call(runforStep_gymGame_command, shell=True)


def run(env, a):
    # 修改信使，让 checkinfo.java 放行，执行下一个宏命令
    with open("javafile/info.txt", "w") as f:
        f.write("false")  # 自带文件关闭功能，不需要再写f.close()

    # 线程1是挂载 starccm+服务器 到后台
    thread_thred1 = threading.Thread(target=thread1)
    # 启动子线程
    thread_thred1.start()
    # 让线程1充分挂载好
    time.sleep(2)

    # 创建生成文件路径，out/logs/ 主要存放日志文件，out/csvfile/ 是每个回合的记录，out/savemodel/ 用于保存模型超参数
    all_log_path = ['out/logs/', 'out/csvfile/', 'out/tensorboard', 'out/savemodel/local/', 'out/savemodel/target/']
    for pathName in all_log_path:
        if not os.path.exists(pathName):
            os.makedirs(pathName)

    # 启用日志
    log()

    # 删除系统中存在的历史文件
    checkExistFile()

    Reward_history = []
    FanPower_history = []

    # 让宏命令挂在后台
    thread_thred2 = threading.Thread(target=thread2)
    thread_thred2.start()
    eposideFlag = True
    while True:  # Run until solved
        # print(threading.active_count())
        # 删除历史生成的 RHfile.csv
        if os.path.exists(RHfile):
            os.remove(RHfile)
        # 一个回合中rewards和fan_power的初始化
        rewards_history = []
        fan_power_history = []
        # 选择初始动作
        startAction = [50, 50, 50, 0, 0, 0]
        # 仿真环境初始化
        env.make(startAction)
        time.sleep(6)
        stepFlag = True

        while True:
            # 获取当前的环境
            state, _ = env.state(a.t_step)
            # 根据环境获取当前动作
            action = a.act(state)
            # 修改action并执行仿真环境
            state_next, reward, done, fan_power = env.steprun(action, a.t_step)
            # # 如果模型发散了，重新计算
            state_flag = np.mean(state_next)
            if state_flag > 61 or state_flag < 40:
                stepFlag = False
                break
            # 存储一个回合中每步的 reward 和 fan_power
            rewards_history.append(reward)
            fan_power_history.append(fan_power)

            print("timestep", a.t_step, "action:", action, "reward:", reward, "fanpower:",
                  fan_power)
            # 存储数据并训练模型
            a.step(state, action, reward, state_next, done)

            # 判断是否结束这个回合
            if done is True:
                break

        # 如果模型发散了，就不记录这个eposide
        if stepFlag is False:
            eposideFlag = False
            continue
        if eposideFlag is False:
            eposideFlag = True
            continue
        episode = a.episodes - 1
        # 一个回合的 reward总和 ：Reward 和 fanpower 总和：FanPower
        Reward_history.append(sum(rewards_history))
        FanPower_history.append(sum(fan_power_history))

        print('episode', episode, 'score', sum(rewards_history), 'score_max', max(Reward_history), "FanPowerSUM",
              sum(fan_power_history))

        # 保存episode_reward_history和each_episode_rewards_history数据

        name = [str(episode)]

        pd.DataFrame(data=[rewards_history], index=name). \
            to_csv(each_episode_rewards_history_csv, sep=',', mode='a', encoding='utf-8')

        pd.DataFrame(data=[fan_power_history], index=name). \
            to_csv(each_FanPower_history_csv, sep=',', mode='a', encoding='utf-8')

        pd.DataFrame(data=[Reward_history], index=name). \
            to_csv(episode_reward_history_csv, sep=',', encoding='utf-8')

        pd.DataFrame(data=[FanPower_history], index=name). \
            to_csv(FanPower_history_csv, sep=',', encoding='utf-8')

        pd.DataFrame(data=np.array([a.losses]).reshape(-1, 1)). \
            to_csv(Loss_history_csv, encoding='utf-8')

        # 把每一轮的 RHfile.csv 历史另存为 RHfile_episode.csv
        dstFile = all_log_path[1] + 'RHfile_' + str(episode) + '.csv'
        try:
            shutil.copyfile(RHfile, dstFile)
        except Exception as e:
            print(e)

        # 保存模型超参数
        if episode % 100 == 0:
            # a.network_local.save_weights(all_log_path[3] + 'RHfile_' + str(episode))
            a.network_target.save_weights(all_log_path[4] + 'RHfile_' + str(episode))

        # 判断模型收敛并结束训练的条件
        if len(Reward_history) >= 10 and (np.mean(Reward_history[-10:])) > 20:
            print("Solved at episode {}!".format(episode))
            break