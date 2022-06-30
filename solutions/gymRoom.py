import subprocess
import numpy as np
import pandas as pd
import time
from .utils import *
from .gymProfile import *


#################################################################################################
#
# # 旧的仿真模型布点编号列表
# state_21 = [j for j in range(1, 22)]
# state_15 = [2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20]
# state_9 = [2, 4, 6, 9, 11, 13, 16, 18, 20]
# state_6 = [3, 5, 10, 12, 17, 19]
#
# # 新的仿真模型布点编号列表
# state_36 = [j for j in range(1, 37)]
# state_20 = [1, 3, 5, 7, 9, 10, 12, 14, 16, 18, 19, 21, 23, 25, 27, 28, 30, 32, 34, 36]
# state_12 = [1, 5, 9, 10, 14, 18, 19, 23, 27, 28, 32, 36]

# # state_col表示应该选取的湿度点所在的列数索引
# state_col = [i + 8 for i in state_9]
################################################################################################

def FanPowerFunction(value):
    """
        恒湿机风扇的档位与功率的对应值
    :param value: 恒湿机风扇的档位 (int)
    :return: 恒湿机的功率（float）
    """
    if value == 1:
        FP = 0.12
    elif value == 2:
        FP = 0.22
    elif value == 3:
        FP = 0.32
    else:
        FP = 0.02
    return FP


class roomex(object):
    def __init__(self, statesize=15, physicalTimeStep=30):
        self.alpha1 = 0.9  # 权重占比
        self.alpha2 = 1 - self.alpha1
        self.RHset = 40  # 湿度设定的目标
        # self.actionsize = 3 * 4 * 4 * 4  # action维度
        self.actionsize = 4 * 4 * 4  # action维度
        self.statesize = statesize  # 湿度传感器的数量
        self.physicalTimeStep = physicalTimeStep  # 仿真环境中step的物理时间(单位：s)
        self.IndoorAction = [25, 40, 0]

    def state(self, step, test=False):

        while True:
            try:
                dfs = pd.read_csv(RHfile)
                # 获取末状态数据
                dfdata = dfs.iloc[-1, :]
                if test is False:
                    # 获取第12列以后的数据作为state
                    state = dfdata[12:]
                else:
                    # 测试阶段获取恒湿机感知周围环境的湿度值
                    state = dfdata[9:12]

                # 获取真实环境的step步数
                stepTotal = dfdata[0]
                state = np.array(state)
                state = [float('{:.1f}'.format(p)) for p in state]
                # 根据t_step 判断当前仿真环境有没有执行t_step对应的仿真环境的物理时间
                if int(stepTotal) == (step + 1) * self.physicalTimeStep:
                    break
                else:
                    # 修改信使，让 checkinfo.java 放行，执行下一个宏命令
                    with open("javafile/info.txt", "w") as f:
                        f.write("true")  # 自带文件关闭功能，不需要再写f.close()
                    # print("等待仿真环境的执行")

                    time.sleep(0.1)
                    continue
            except Exception as e:
                # 仿真环境初始化的时候，还没生成csv文件才会跑到这里
                with open("javafile/info.txt", "w") as f:
                    f.write("true")  # 自带文件关闭功能，不需要再写f.close()
                time.sleep(1)
                # print(e)
                # print("等待环境初始化")
        return state, stepTotal

    def reset(self, RHRESET=50):
        # 重置仿真环境
        # 修改 reset.java 文件
        with open(resetfilename, "r+", encoding="utf-8") as f:
            flist = f.readlines()
            MassF = getMassFraction(25, RHRESET)
            flist[33 - 1] = '\tmassFractionProfile_0.getMethod(ConstantArrayProfileMethod.class).getQuantity().setArray' \
                            '(new DoubleVector(new double[] ' + str(MassF) + '));\n'
        with open(resetfilename, "w+", encoding="utf-8") as f:
            f.writelines(flist)

        subprocess.call(reset_gymGame_command, shell=True)

    def make(self, action):
        """
            初始化仿真环境
        :param action:
        :return: None
        """
        # 修改editandrun.java文件恒湿机的动作参数
        with open(editandrunfile, "r+", encoding="utf-8") as f:
            flist = f.readlines()

            # 干球温度25°C、相对湿度,返回h2o和空气的质量分数
            MassF1 = getMassFraction(25, action[0])
            MassF2 = getMassFraction(25, action[1])
            MassF3 = getMassFraction(25, action[2])

            # 恒湿机湿度
            flist[33 - 1] = '\tmassFractionProfile_1.getMethod(ConstantArrayProfileMethod.class).getQuantity().' \
                            'setArray(new DoubleVector(new double[] ' + str(MassF1) + '));\n'
            flist[45 - 1] = '\tmassFractionProfile_2.getMethod(ConstantArrayProfileMethod.class).getQuantity().' \
                            'setArray(new DoubleVector(new double[] ' + str(MassF2) + '));\n'
            flist[57 - 1] = '\tmassFractionProfile_3.getMethod(ConstantArrayProfileMethod.class).getQuantity().' \
                            'setArray(new DoubleVector(new double[] ' + str(MassF3) + '));\n'
            # 恒湿机风速
            flist[37 - 1] = '\tvelocityMagnitudeProfile_1.getMethod(ConstantScalarProfileMethod.class).getQuantity().' \
                            'setValue(' + str(action[3]) + ');\n'
            flist[49 - 1] = '\tvelocityMagnitudeProfile_2.getMethod(ConstantScalarProfileMethod.class).getQuantity().' \
                            'setValue(' + str(action[4]) + ');\n'
            flist[61 - 1] = '\tvelocityMagnitudeProfile_3.getMethod(ConstantScalarProfileMethod.class).getQuantity().' \
                            'setValue(' + str(action[5]) + ');\n'

        with open(editandrunfile, "w+", encoding="utf-8") as f:
            f.writelines(flist)

    def steprun(self, action, step, IndoorAction=None):
        """
            修改恒湿机动作并让仿真环境跑一步
        :param action: agent动作
        :return: next_s, reward, done, FanPower
        """
        # 修改editandrun.java文件恒湿机的动作参数
        with open(editandrunfile, "r+", encoding="utf-8") as f:
            flist = f.readlines()

            # 干球温度25°C、相对湿度,返回h2o和空气的质量分数
            MassF1 = getMassFraction(25, action[0])
            MassF2 = getMassFraction(25, action[1])
            MassF3 = getMassFraction(25, action[2])

            # 恒湿机湿度
            flist[33 - 1] = '\tmassFractionProfile_1.getMethod(ConstantArrayProfileMethod.class).getQuantity().' \
                            'setArray(new DoubleVector(new double[] ' + str(MassF1) + '));\n'
            flist[45 - 1] = '\tmassFractionProfile_2.getMethod(ConstantArrayProfileMethod.class).getQuantity().' \
                            'setArray(new DoubleVector(new double[] ' + str(MassF2) + '));\n'
            flist[57 - 1] = '\tmassFractionProfile_3.getMethod(ConstantArrayProfileMethod.class).getQuantity().' \
                            'setArray(new DoubleVector(new double[] ' + str(MassF3) + '));\n'
            # 恒湿机风速
            flist[37 - 1] = '\tvelocityMagnitudeProfile_1.getMethod(ConstantScalarProfileMethod.class).getQuantity().' \
                            'setValue(' + str(action[3]) + ');\n'
            flist[49 - 1] = '\tvelocityMagnitudeProfile_2.getMethod(ConstantScalarProfileMethod.class).getQuantity().' \
                            'setValue(' + str(action[4]) + ');\n'
            flist[61 - 1] = '\tvelocityMagnitudeProfile_3.getMethod(ConstantScalarProfileMethod.class).getQuantity().' \
                            'setValue(' + str(action[5]) + ');\n'

            if IndoorAction is None:

                flist[68 - 1] = '\tWallBoundary wallBoundary_0 = ((WallBoundary) simulation_0.get' \
                                '(ConditionTypeManager.class).get(WallBoundary.class));\n'
                flist[70 - 1] = '\tboundary_0.setBoundaryType(wallBoundary_0);\n'

                for i in range(72, 83):
                    flist[i - 1] = '\n'
            else:

                flist[68 - 1] = '\tInletBoundary inletBoundary_0 = ((InletBoundary) simulation_0.get' \
                                '(ConditionTypeManager.class).get(InletBoundary.class));\n'
                flist[70 - 1] = '\tboundary_0.setBoundaryType(inletBoundary_0);\n'

                # Indoor 扰动
                flist[72 - 1] = '\tStaticTemperatureProfile staticTemperatureProfile_0 = boundary_0.getValues()' \
                                '.get(StaticTemperatureProfile.class);\n'
                # Indoor温度
                flist[74 - 1] = '\tstaticTemperatureProfile_0.getMethod(ConstantScalarProfileMethod.class).' \
                                'getQuantity().setValue(' + str(IndoorAction[0]) + ');\n'
                flist[76 - 1] = '\tMassFractionProfile massFractionProfile_0 = boundary_0.getValues().' \
                                'get(MassFractionProfile.class);\n'
                # Indoor湿度
                flist[78 - 1] = '\tmassFractionProfile_0.getMethod(ConstantArrayProfileMethod.class).getQuantity()' \
                                '.setArray(new DoubleVector(new double[] ' + \
                                str(getMassFraction(IndoorAction[0], IndoorAction[1])) + '));\n'
                flist[80 - 1] = '\tVelocityMagnitudeProfile velocityMagnitudeProfile_0 = ' \
                                'boundary_0.getValues().get(VelocityMagnitudeProfile.class);\n'
                # Indoor风速
                flist[82 - 1] = '\tvelocityMagnitudeProfile_0.getMethod(ConstantScalarProfileMethod.class).' \
                                'getQuantity().setValue(' + str(IndoorAction[2]) + ');\n'
        with open(editandrunfile, "w+", encoding="utf-8") as f:
            f.writelines(flist)

        step = step + 1
        # 读取java宏生成的csv文件
        next_s, stepTotal = self.state(step)

        """
        
            设置奖励函数:     由 21个传感器湿度与目标湿度的差值的绝对值之和 与 恒湿机风扇的功耗 之和构成
        
        """
        # 获取三个恒湿机的总功耗
        FanPower = FanPowerFunction(action[3]) + FanPowerFunction(action[4]) + FanPowerFunction(action[5])

        RH_abs = []
        # RH_even = []
        # RH_abs_state = []
        for i in range(len(next_s)):
            RH_abs.append(abs(next_s[i] - self.RHset))
            # RH_even.append(abs(next_s[i] - np.mean(next_s)))

        reward1 = sum(RH_abs) / self.statesize  # 3 %
        # reward2 = 0.5 * (sum(RH_even) / len(next_s))  # 均匀
        # reward3 = sum(RH_abs_state) - sum(RH_abs)  # 快速

        # alpha = 0.9
        # reward = - pow(reward1 / 20, 1 / 2) * alpha - ((FanPower - 0.02 * 3) / 0.9) * (1 - alpha)

        if reward1 < 10:
            reward = - (reward1 / 10) * self.alpha1 - ((FanPower - 0.06) / 0.9) * self.alpha2
        else:
            reward = -1

        # reward = - (reward1 / 420) * 0.95 - ((FanPower - 0.06) / 0.9) * 0.05

        # if reward1 < 21:
        #     reward = - (reward1 / 21) * 0.5 - ((FanPower - 0.06) / 0.9) * 0.5
        # else:
        #     reward = -1
        # if reward1 < 105:
        #     reward = - reward1 / 210 - ((FanPower - 0.06) / 0.9) * 0.5
        # else:
        #     reward = -1
        # if sum(RH_abs) < 10:
        #     if FanPower > 0.36:
        #         reward = reward - FanPower * 10

        """

            设置这个回合的结束条件:    10分钟后就结束循环

        """
        done = False if stepTotal <= self.physicalTimeStep * 20 else True

        return next_s, reward, done, FanPower
