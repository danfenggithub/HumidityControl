import os


os.environ['CUDA_VISIBLE_DEVICES'] = '0'

import tensorflow as tf


gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_virtual_device_configuration(
    gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=300)])

from HumidityControl.solutions.memories import PrioritizedNStepMemory
from HumidityControl.solutions.networks import NoisyDuelingNetwork
import HumidityControl.solutions.gymRoom as gymRoom
from HumidityControl.solutions.run import *

env = gymRoom.roomex()
mem = PrioritizedNStepMemory(int(1e5), n=3, update_every=30, gamma=0.99)
a = DQNAgent(state_size=env.statesize, hidden_sizes=[256, 256],
             action_size=env.actionsize, replay_memory=mem,
             double=True, Architecture=NoisyDuelingNetwork)
run(env, a)
