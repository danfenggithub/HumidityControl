import os

# 启用 GPU 0
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import tensorflow as tf

# 限制 gpu 0 占用内存大小
gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_virtual_device_configuration(
    gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=300)])

from HumidityControl.solutions.memories import PrioritizedNStepMemory
from HumidityControl.solutions.networks import DuelingNetwork
import HumidityControl.solutions.gymRoom as gymRoom
from HumidityControl.solutions.run import *

env = gymRoom.roomex()
mem = PrioritizedNStepMemory(int(1e5), n=3, update_every=30, gamma=0.99)
a = DQNAgent(state_size=env.statesize,
             action_size=env.actionsize, replay_memory=mem,
             double=True, Architecture=DuelingNetwork)
run(env, a)
