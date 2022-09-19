import subprocess
import numpy as np
import pandas as pd
import time
from .utils import *
from .gymProfile import *



def FanPowerFunction(value):
    """
        Corresponding value of the gear and power of the constant humidity fan
    :param value: constant humidity setting of fan (int)
    :return: Power of constant humidity machine (float)
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
        self.alpha1 = 0.9  # Weight ratio
        self.alpha2 = 1 - self.alpha1
        self.RHset = 40  # Humidity setting target
        # self.actionsize = 3 * 4 * 4 * 4  # Dimension of action
        self.actionsize = 4 * 4 * 4  # Dimension of action
        self.statesize = statesize  # Number of humidity sensors
        self.physicalTimeStep = physicalTimeStep  # Physical time of step in simulation environment (unit: s)
        self.IndoorAction = [25, 40, 0]

    def state(self, step, test=False):

        while True:
            try:
                dfs = pd.read_csv(RHfile)
                # Get final status data
                dfdata = dfs.iloc[-1, :]
                if test is False:
                    # Get the data after the 12th column as the state
                    state = dfdata[12:]
                else:
                    # Acquire the humidity value of the surrounding environment
                    # perceived by the humidistat machine in the test phase
                    state = dfdata[9:12]

                # Get the step steps of the real environment
                stepTotal = dfdata[0]
                state = np.array(state)
                state = [float('{:.1f}'.format(p)) for p in state]

                if int(stepTotal) == (step + 1) * self.physicalTimeStep:
                    break
                else:
                    # Modify the messenger to pass the checkinfo.java verification and execute the next macro command
                    with open("javafile/info.txt", "w") as f:
                        f.write("true")

                    time.sleep(0.1)
                    continue
            except Exception as e:
                # When the simulation environment is initialized, the csv file has not been generated
                with open("javafile/info.txt", "w") as f:
                    f.write("true")
                time.sleep(1)

        return state, stepTotal

    def reset(self, RHRESET=50):
        # Reset Simulation Environment
        #  Modify reset.java file
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

        with open(editandrunfile, "r+", encoding="utf-8") as f:
            flist = f.readlines()


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
            Modify the action of the constant humidity machine
            and let the simulation environment run a step
        :param action: action of agent
        :return: next_s, reward, done, FanPower
        """
        # Modify the action parameters of the constant humidity
        # machine in the editandrun.java file
        with open(editandrunfile, "r+", encoding="utf-8") as f:
            flist = f.readlines()

            # Dry bulb temperature 25°C, relative humidity, return h2o and air mass fraction
            MassF1 = getMassFraction(25, action[0])
            MassF2 = getMassFraction(25, action[1])
            MassF3 = getMassFraction(25, action[2])

            # Humidity of constant humidity machine
            flist[33 - 1] = '\tmassFractionProfile_1.getMethod(ConstantArrayProfileMethod.class).getQuantity().' \
                            'setArray(new DoubleVector(new double[] ' + str(MassF1) + '));\n'
            flist[45 - 1] = '\tmassFractionProfile_2.getMethod(ConstantArrayProfileMethod.class).getQuantity().' \
                            'setArray(new DoubleVector(new double[] ' + str(MassF2) + '));\n'
            flist[57 - 1] = '\tmassFractionProfile_3.getMethod(ConstantArrayProfileMethod.class).getQuantity().' \
                            'setArray(new DoubleVector(new double[] ' + str(MassF3) + '));\n'
            # Wind speed of constant humidity machine
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


                flist[72 - 1] = '\tStaticTemperatureProfile staticTemperatureProfile_0 = boundary_0.getValues()' \
                                '.get(StaticTemperatureProfile.class);\n'
                # Temperature of indoor
                flist[74 - 1] = '\tstaticTemperatureProfile_0.getMethod(ConstantScalarProfileMethod.class).' \
                                'getQuantity().setValue(' + str(IndoorAction[0]) + ');\n'
                flist[76 - 1] = '\tMassFractionProfile massFractionProfile_0 = boundary_0.getValues().' \
                                'get(MassFractionProfile.class);\n'
                # Humidity of indoor
                flist[78 - 1] = '\tmassFractionProfile_0.getMethod(ConstantArrayProfileMethod.class).getQuantity()' \
                                '.setArray(new DoubleVector(new double[] ' + \
                                str(getMassFraction(IndoorAction[0], IndoorAction[1])) + '));\n'
                flist[80 - 1] = '\tVelocityMagnitudeProfile velocityMagnitudeProfile_0 = ' \
                                'boundary_0.getValues().get(VelocityMagnitudeProfile.class);\n'
                # Wind speed of indoor
                flist[82 - 1] = '\tvelocityMagnitudeProfile_0.getMethod(ConstantScalarProfileMethod.class).' \
                                'getQuantity().setValue(' + str(IndoorAction[2]) + ');\n'
        with open(editandrunfile, "w+", encoding="utf-8") as f:
            f.writelines(flist)

        step = step + 1
        # Read the csv file generated by java macro
        next_s, stepTotal = self.state(step)

        """
        
            Set reward function: composed of the sum of the absolute values of 
            the difference between the 21 sensor humidity and the target humidity 
            and the sum of the power consumption of the constant humidity fan
        
        """
        # Obtain the total power consumption of three constant humidity machines
        FanPower = FanPowerFunction(action[3]) + FanPowerFunction(action[4]) + FanPowerFunction(action[5])

        RH_abs = []
        # RH_even = []
        # RH_abs_state = []
        for i in range(len(next_s)):
            RH_abs.append(abs(next_s[i] - self.RHset))
            # RH_even.append(abs(next_s[i] - np.mean(next_s)))

        reward1 = sum(RH_abs) / self.statesize  # 3 %
        # reward2 = 0.5 * (sum(RH_even) / len(next_s))
        # reward3 = sum(RH_abs_state) - sum(RH_abs)

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

            Set the ending conditions of this round

        """
        done = False if stepTotal <= self.physicalTimeStep * 20 else True

        return next_s, reward, done, FanPower
