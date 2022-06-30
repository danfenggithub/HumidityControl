import os

# 启用 GPU 0
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import tensorflow as tf

# 限制 gpu 0 占用内存大小
gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_virtual_device_configuration(
    gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=300)])

import HumidityControl.solutions.gymRoom as gymRoom
from HumidityControl.solutions.memories import VanillaMemory
from HumidityControl.solutions.run import *

env = gymRoom.roomex()
mem = VanillaMemory(int(1e5))
a = DQNAgent(state_size=env.statesize,
             action_size=env.actionsize, replay_memory=mem)
run(env, a)
