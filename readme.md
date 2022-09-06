
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

HumidityControl

-- DifferentArithmetic
+ Model training of DQN, Rainbow, and Rainbow ablation algorithms

-- DifferentSetpoints
+ Experiments at different monitoring points (6, 9 and 15 humidity sensors) of model A.

-- DifferentTime
+ Experiment of different reporting time intervals (1, 3 and 5 minutes) of model A.

-- modelAtest
+ Test the effect of different algorithms in model A.

-- modelB
+ Test the effect of different algorithms in model B

-- pid
+ PID algorithm.

-- solutions
+ The module related to reinforcement learning and the module interacting with the model of STAR-CCM+.


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

HumidityControl

-- DifferentArithmetic
+ DQN、Rainbow、和Rainbow消融算法的模型训练

-- DifferentSetpoints
+ 模型A的不同监测点(6、9、15个湿度传感器)实验

-- DifferentTime
+ 模型A的不同上报时间间隔(1、3、5分钟)实验

-- modelAtest
+ 测试不同算法在模型A的效果

-- modelB
+ 测试不同算法在模型B的效果

-- pid
+ PID算法

-- solutions
+ 强化学习相关的模块,与STAR-CCM+的模型进行交互.