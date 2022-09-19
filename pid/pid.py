import os


os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import tensorflow as tf
import numpy as np
import HumidityControl.solutions.gymRoom as gymRoom
from HumidityControl.solutions.utils import *
from HumidityControl.solutions.gymProfile import *
import subprocess
import threading


def thread1():
    subprocess.call("cd javafile && " + start_starccm_server, shell=True)


def thread2():

    subprocess.call(runforStepTest_gymGame_command, shell=True)
    # 21 steps
    # subprocess.call(runforStep_gymGame_command, shell=True)
    # 100 steps
    # subprocess.call(runforStepTest_100step, shell=True)

class PIDController:


    def __init__(self, target_val, kp, ki, kd):
        self.target_val = target_val
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.out_put_arr = [0]
        self.observed_val_arr = []

        self.now_val = 0
        self.sum_err = 0
        self.now_err = 0
        self.last_err = 0

        self.integral = 0
        self.dt = 1
        self.pre_error = 0

    def iterate(self, state):
        # The input is a single point state and the output is a single action

        self.observed_val_arr.append(state)
        error = self.target_val - self.observed_val_arr[-1]
        Pout = self.kp * error  # Kp * e(t)
        self.integral += error * self.dt  # ∑e(t)*△t
        Iout = self.ki * self.integral  # Ki * ∑e(t)*△t
        derivative = (error - self.pre_error) / self.dt  # (e(t)-e(t-1))/△t
        Dout = self.kd * derivative  # Kd * (e(t)-e(t-1))/△t

        out_put = Pout + Iout + Dout  # PID：u(t) = Kp*e(t) + Ki * ∑e(t)*△t + Kd * (e(t)-e(t-1))/△t

        out_put = round(out_put)
        # print(out_put)
        if out_put > 3:
            out_put = 3
        elif out_put <= 0:
            out_put = 0
        self.pre_error = error
        self.out_put_arr.append(out_put)

        return out_put


def pid(statesize=15, physicalTimeStep=30):
    # Limit the memory occupied by gpu 0
    gpus = tf.config.experimental.list_physical_devices('GPU')
    tf.config.experimental.set_virtual_device_configuration(
        gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=600)])

    # Create a path to the generated file.
    # out/logs/mainly stores log files.
    # out/csvfile/ is the record of each round.
    # out/savemodel/ is used to save super parameters of model.
    all_log_path = ['out/logs/', 'out/csvfile/']
    for pathName in all_log_path:
        if not os.path.exists(pathName):
            os.makedirs(pathName)

    thread_thred1 = threading.Thread(target=thread1)
    # Start sub thread
    thread_thred1.start()

    # Delete historical files existing in the system
    checkExistFile()
    time.sleep(2)

    # Initialize the pid, the target value is 40, Kp=-0.5, Ki=0, Kd=0.1
    controller1 = PIDController(40, -0.5, 0, 0.1)
    controller2 = PIDController(40, -0.5, 0, 0.1)
    controller3 = PIDController(40, -0.5, 0, 0.1)


    with open("javafile/info.txt", "w") as f:
        f.write("false")

    if os.path.exists(RHfile):
        os.remove(RHfile)
    time.sleep(5)

    env = gymRoom.roomex(statesize=statesize, physicalTimeStep=physicalTimeStep)

    env.reset(50)

    action = [50, 50, 50, 0, 0, 0]
    env.make(action)

    t_step = 0
    time.sleep(5)
    # Let macro commands hang in the background
    thread_thred2 = threading.Thread(target=thread2)
    thread_thred2.start()

    while True:
        state, _ = env.state(t_step, test=True)
        print(state)

        action1 = controller1.iterate(state[0])
        action2 = controller2.iterate(state[1])
        action3 = controller3.iterate(state[2])
        action = [40, 40, 40, action1, action2, action3]

        """
           Common to all interference free experiments
        """
        # state_next, reward, done, FanPower  = env.steprun(action, t_step)

        """
            Model A interference experiment
        """
        # if t_step == 14:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 55, 1])
        # else:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step)
        ##########################################################################################################

        """
            Model B interference experiment
        """

        # if t_step == 15:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 55, 1])
        # else:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step)
        ##########################################################################################################

        """
            Different time intervals
        """

        # ##  1-minute interference test
        # if t_step == 15:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 60, 1])
        # else:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step)

        # ##  3-minute interference test
        # if t_step == 15:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 55, 1])
        # else:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step)

        # ##  5-minute interference test
        # if t_step == 30:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 45, 1])
        # else:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step)
        ##########################################################################################################

        """
            9points
        """
        # Single interference
        if t_step == 14:
            state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 55, 1])
        else:
            state_next, reward, done, FanPower = env.steprun(action, t_step)


        # # Multiple interferences
        # if t_step == 15:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 45, 1])
        # elif t_step == 30:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 50, 1])
        # elif t_step == 45:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 55, 1])
        # elif t_step == 60:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 60, 1])
        # elif t_step == 75:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step, IndoorAction=[25, 55, 1])
        # else:
        #     state_next, reward, done, FanPower = env.steprun(action, t_step)
        ##########################################################################################################


        t_step += 1
        print("t_step:", t_step, "action:", action)
        # if done is True:
        #     break
