import os

# 启用 GPU 0
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import tensorflow as tf

# 限制 gpu 0 占用内存大小
gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_virtual_device_configuration(
    gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=300)])

import pandas as pd
import numpy as np
import shutil
from HumidityControl.solutions.networks import *
import HumidityControl.solutions.gymRoom as gymRoom
from HumidityControl.solutions.utils import *
from HumidityControl.solutions.gymProfile import *

import subprocess
import threading


def thread1():
    subprocess.call("cd javafile && " + start_starccm_server, shell=True)


def thread2():
    # 线程2是后台连续执行Java宏命令，每一轮循环代表一个回合
    subprocess.call(runforStepTest_gymGame_command, shell=True)


thread_thred1 = threading.Thread(target=thread1)
# 启动子线程
thread_thred1.start()

# 删除系统中存在的历史文件
checkExistFile()
time.sleep(2)

state_col_num = 15
# network_local = NoisyDuelingNetwork(output_size=64, hidden_sizes=[256, 256], input_size=state_col_num)
# network_local.build(input_shape=(None, state_col_num))
# network_local.load_weights("../../train/train_5mins2/out/savemodel/target/RHfile_2500")

# 修改信使，让 checkinfo.java 放行，执行下一个宏命令
with open("javafile/info.txt", "w") as f:
    f.write("false")  # 自带文件关闭功能，不需要再写f.close()

a_action = [40, 50, 60]
b_action = [0, 1, 2, 3]
c_action = [40, 50, 60]
d_action = [0, 1, 2, 3]
e_action = [40, 50, 60]
f_action = [0, 1, 2, 3]

rewards_history = []
episode_reward_history = []
FanPower_history = []
episode_count = 0
frame_count = 0

if os.path.exists(RHfile):
    os.remove(RHfile)
time.sleep(5)

env = gymRoom.roomex(15, 5 * 60)

env.reset(50)

each_FanPower_history = []
each_episode_rewards_history = []
episode_reward = 0

action = [50, 50, 50, 0, 0, 0]
env.make(action)
print(sys.path)
t_step = 0
time.sleep(5)
# 让宏命令挂在后台
thread_thred2 = threading.Thread(target=thread2)
thread_thred2.start()

while True:

    state, _ = env.state(t_step, test=True)

    print(state)
    frame_count += 1

    # state_tensor = tf.convert_to_tensor(state)
    # state_tensor = tf.expand_dims(state_tensor, 0)
    # action_values = network_local(tf.cast(state_tensor, dtype=tf.float32))
    # action_num = np.argmax(action_values.numpy())
    # action = [a_action[action_num // 64],
    #           c_action[action_num // 64],
    #           e_action[action_num // 64],
    #           b_action[(action_num % 64) // 16],
    #           d_action[(action_num % 64 % 16) // 4],
    #           f_action[(action_num % 64 % 16 % 4) // 1]]
    # action = [40, 40, 40,
    #           b_action[action_num // 16],
    #           d_action[(action_num % 16) // 4],
    #           f_action[(action_num % 16 % 4) // 1]]
    # action_a = action_b = action_c = 1

    if abs(state[0] - 40) < 1:
        action_a = 0
    else:
        action_a = 1
    if abs(state[1] - 40) < 1:
        action_b = 0
    else:
        action_b = 1
    if abs(state[2] - 40) < 1:
        action_c = 0
    else:
        action_c = 1

    action = [40, 40, 40, action_a, action_b, action_c]

    # CCS_M
    # if abs(np.average(state) - 40) < 1:
    #     action_a, action_b, action_c = 0, 0, 0
    # else:
    #     action_a, action_b, action_c = 1, 1, 1
    #
    # action = [40, 40, 40, action_a, action_b, action_c]

    if t_step == 30:
        state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 45, 1])
    else:
        state_next, reward, done, FanPower = env.steprun(action, t_step)

    # state_next, reward, done, FanPower = env.steprun(action, t_step)

    # print(state_next)
    state = np.array(state)
    state_next = np.array(state_next)

    each_FanPower_history.append(FanPower)

    episode_reward += reward

    print("t_step:", t_step, "action:", action, "reward:", reward, "fanpower:", FanPower)
    t_step += 1
    # if t_step == 16:
    #     break
