
# Intelligent Distributed Humidity Control #

---------------


## Project Introduction ##

This project is a distributed intelligent 
humidity control system that regulates 
and controls the wind speed of multiple 
humidifiers based on the rainbow algorithm. 
Simcenter STAR-CCM+ software and TensorFlow2 
dependent packages need to be installed to 
run this project.

## Installation, Configuration & Deployment ##

1. Download [Simcenter STAR-CCM+](https://www.plm.automation.siemens.com/global/en/products/simcenter/STAR-CCM.html)

2. [Steps to install STAR-CCM+](https://wiki.anl.gov/tracc/Speeding_up_STAR-CCM%2B)

3. Configure the project environment

* Add an environment variable PYTHONPATH to the ".bashrc" file 
in the user's home directory.

```shell
  $ gedit ~/.bashrc
```

*  Add an environment variable named PYTHONPATH
```
  export PYTHONPATH=<your path>:$PATH'
```
>If you put the project named "HumidityControl" under the path of '/home/user/', 
the added path is:
>> export PYTHONPATH=/home/user/HumidityControl:$PYTHONPATH

* Saving and refreshing environment variables.
```shell
  $ source ~/.bashrc
```


4. Install tensorflow2 framework. See requirements.txt 
for the dependent package version.
Related link: https://github.com/tensorflow/tensorflow

5. After completing the above basic environment 
configuration, you can run the specific programs 
in each folder.

## File Directory ##

- HumidityControl
  + DifferentArithmetic
    > Model training of DQN, Rainbow, and Rainbow ablation algorithms
  + DifferentSetpoints
    > Experiments at different monitoring points (6, 9 and 15 humidity sensors) of model A.
  + DifferentTime
    > Experiment of different reporting time intervals (1, 3 and 5 minutes) of model A.
  + modelAtest
    > Test the effect of different algorithms in model A.
  + modelB
    > Test the effect of different algorithms in model B
  + pid
    > PID algorithm.
  + solutions
    > The module related to reinforcement learning and the module interacting with the model of STAR-CCM+.
  
## Folder Details  ##

Only the data and file descriptions in the directory of the rainbow algorithm are described here. 
The file storage methods of other algorithms are the same.

The specific location of the rainbow directory:

- HumidityControl
  + DifferentArithmetic
    + rainbow

The description under the rainbow folder:

- javafile 
  > Store simulation models and macro commands.
  + checkinfo.java 
    > Check the info.txt file operation.
  + editandrun.java 
    > Modify the boundary conditions related to the CFD model, such as the temperature, 
    humidity and wind speed of the constant humidity machine.
  + info.txt 
    > The time verification file maintains the physical time consistency between the simulation model and the agent.
  + reset.java 
    > Reset the macro command of the simulation environment.
  + RHfile.csv 
    > Interactive data of the current episode.
  + humidity.sim 
    > CFD simulation model.
- out 
  > Storing history files (model data and agent strategy)
  + csvfile 
    >Record the interactive data of each episode.
  + logs 
    >Record the output of the console.
  + savemodel 
    >Target network for saving historical agents.
  + each_episode_rewards_history.csv
    > Detailed data of historical reward.
  + each_FanPower_history.csv
    > Detailed data of historical energy consumption of constant humidity machine
  + episode_reward_history.csv
    > Historical reward.
  + FanPower_history.csv
    > Historical energy consumption of constant humidity machine.
  + Loss_history.csv
    > Historical data of loss value.
  + mypython.out
    > Output information of the console.

## Data description ##

Data column description of 'csvfile' directory.

- "Physical Time: Physical Time (s)"
    > Simulation physical time.
- "InletDoor Monitor: Surface Average of RH"
    > Humidity at gate entrance.
- "InletRHa Monitor: Surface Average of RH","InletRHb Monitor: Surface Average of RH"
,"InletRHc Monitor: Surface Average of RH"
    > Humidity of air outlet of constant humidity machine a, b, c.
- "InletVelDoor Monitor: Surface Average of Velocity: Magnitude (m/s)"
,"InletVela Monitor: Surface Average of Velocity: Magnitude (m/s)"
,"InletVelb Monitor: Surface Average of Velocity: Magnitude (m/s)"
,"InletVelc Monitor: Surface Average of Velocity: Magnitude (m/s)"
    > Wind speed at the gate entrance and the outlets of a, b, c constant humidity machine.
- "点10RH Monitor: Sum of RH","点2RH Monitor: Sum of RH",......,"点21RH Monitor: Sum of RH"
    > Humidity of 21 sensors in the room.


---------------


# 分布式智能湿度控制 #
> 中文版  Chinese Version
---------------


## 项目介绍  ##

本项目是分布式智能湿度控制,基于Rainbow算法对多个恒湿机进行风速调控.

运行该项目需要基于linux操作系统且需要下载安装 Simcenter STAR-CCM+软件,
安装TensorFlow2相关的依赖包

## 安装、配置和部署 ##

1. [下载STAR-CCM+](https://www.plm.automation.siemens.com/global/en/products/simcenter/STAR-CCM.html)
2. [安装STAR-CCM+](https://wiki.anl.gov/tracc/Speeding_up_STAR-CCM%2B)
3. 配置项目环境.
* 添加PYTHONPATH,否则运行该项目可能会"找不到模块的错误".
在用户主目录下的.bashrc文件中添加名为PYTHONPATH的环境变量,

```shell
  $ gedit ~/.bashrc
```

* 添加名为PYTHONPATH的环境变量
```
    export PYTHONPATH=<你的路径>:$PATH
```
>如果你把名为‘HumidityControl’的项目放在'/home/user/'的路径下，那么添加的路径为：
>>export PYTHONPATH=/home/user/HumidityControl:$PYTHONPATH

* 保存和刷新环境变量
```shell
  $ source ~/.bashrc
```

4. 安装TensorFlow2相关的依赖包，各依赖包版本详见requirements.txt. 
相关链接：https://github.com/tensorflow/tensorflow

5. 完成以上基本的环境配置后就能运行每个文件夹中具体的程序

## 文件目录 ##

- HumidityControl
  + DifferentArithmetic
    >DQN、Rainbow、和Rainbow消融算法的模型训练
  + DifferentSetpoints
    > 模型A的不同监测点(6、9、15个湿度传感器)实验
  + DifferentTime
    > 模型A的不同上报时间间隔(1、3、5分钟)实验
  + modelAtest
    > 测试不同算法在模型A的效果
  + modelB
    > 测试不同算法在模型B的效果
  + pid
    > PID算法
  + solutions
    > 强化学习相关的模块,与STAR-CCM+的模型进行交互.

## 文件详细说明 ##

此处只说明rainbow算法目录下的数据和文件说明，其他算法的文件存放方式与其一致。

rainbow目录的具体位置：

- HumidityControl
  + DifferentArithmetic
    + rainbow

rainbow文件夹下的说明：

- javafile 
  > 存放仿真模型和宏命令
  + checkinfo.java 
    > 检查info.txt文件操作. 
  + editandrun.java 
    > 修改CFD模型相关的边界条件，比如修改恒湿机的温度、湿度、风速.
  + info.txt 
    > 时间校验文件，维持仿真模型和agent的物理时间一致性.
  + reset.java 
    > 重置仿真环境的宏命令.
  + RHfile.csv 
    > 当前episode的交互数据
  + humidity.sim 
    > CFD仿真模型.
- out 
  > 存放历史文件（模型的数据和agent的策略）
  + csvfile 
    >记录历史每个episode的交互数据
  + logs 
    >记录控制台的相关信息
  + savemodel 
    >保存历史智能体的target网络
  + each_episode_rewards_history.csv
    > 历史reward详细数据
  + each_FanPower_history.csv
    > 恒湿机的历史能耗详细数据
  + episode_reward_history.csv
    > 历史reward
  + FanPower_history.csv
    > 恒湿机的历史能耗
  + Loss_history.csv
    > loss值的历史数据
  + mypython.out
    > 控制台的输出信息

## 数据说明 ##

csvfile目录的数据列说明

- "Physical Time: Physical Time (s)"
    > 仿真物理时间
- "InletDoor Monitor: Surface Average of RH"
    > 大门入口的湿度
- "InletRHa Monitor: Surface Average of RH","InletRHb Monitor: Surface Average of RH"
,"InletRHc Monitor: Surface Average of RH"
    > 恒湿机a,b,c的出风口的湿度
- "InletVelDoor Monitor: Surface Average of Velocity: Magnitude (m/s)"
,"InletVela Monitor: Surface Average of Velocity: Magnitude (m/s)"
,"InletVelb Monitor: Surface Average of Velocity: Magnitude (m/s)"
,"InletVelc Monitor: Surface Average of Velocity: Magnitude (m/s)"
    > 分别是大门入口、恒湿机a,b,c出风口的风速
- "点10RH Monitor: Sum of RH","点2RH Monitor: Sum of RH",......,"点21RH Monitor: Sum of RH"
    > 房间内传感器的湿度（21个）
