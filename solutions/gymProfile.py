# 定义调用starccm命令设置服务端的host和端口号方便连接，并且一直放后台挂着

# linux 环境前缀:
ospath = '/opt/Siemens/14.02.010-R8/STAR-CCM+14.02.010-R8/star/bin/starccm+'

# win10 环境前缀:
# ospath = 'starccm+'

# star-ccm+服务端的命令前缀
ospath_server = ospath + " -server "
# star-ccm+客户端的命令前缀
ospath_batch = ospath + " -batch "
# 仿真仿真环境sim文件
simulink_file_Name = ' humidity.sim '
# 自己要跑代码的主机名
host_name_4号机 = ' -host bupt-PowerEdge-R730 '
host_name_自己的电脑 = ' -host DESKTOP-R8U2SOG '

host_name_2号机 = ' -host ubuntu '
host_name_5号机 = ' -host user-Precision-5820-Tower '

import random

# star-ccm+ 客户端和服务端的端口号
port_num = ' -port 48' + str(random.randint(100, 1000)) + ' '
# star-ccm+ 在客户端执行宏文件1后不关闭服务端
Noexit = ' -noexit '
# 不回显控制台输出的信息
noecho = ' >NUL 2>NUL '
# 存放java宏文件路径
javafilepath = './javafile/'
# 重置仿真环境的Java宏文件
resetfilename = javafilepath + 'reset.java'
resetfile = javafilepath + 'reset.java,'
# 修改并运行一步仿真环境的Java宏文件s
editandrunfile = javafilepath + 'editandrun_15.java'
# editandrunfile = javafilepath + 'editandrun_9.java'
# editandrunfile = javafilepath + 'editandrun.java'

'''
    多步调用Java宏文件:./javafile/checkinfo.java,./javafile/editandrun.java,......
    （.java后面的逗号不能去除否则会变成 ./javafile/checkinfo.java./javafile/editandrun.java......）
    checkinfo.java: 检查信使文件info.txt,如果info.txt文件内容为true，就放行，否则就等待
    editandrun_9.java:    仿真环境跑一步并生成  csv 等有关环境的信息，同时让info.txt的信息为false
'''
editandrun_str = javafilepath + "checkinfo.java," + editandrunfile + ","
# Python调用Java宏文件生成的csv文件
RHfile = javafilepath + "RHfile.csv"

"""

    打开star-ccm+ 服务端语句:  starccm+ -server filename.sim -port 48000 

"""
start_starccm_server = ospath_server + simulink_file_Name + port_num

"""

    打开star-ccm+ 客户端并调用宏文件语句:  starccm+ -batch filename.java  -host your_host -port your_port 
    
"""
# 主机和端口号以及其他功能
NoexitAndHostPort = host_name_5号机 + port_num + Noexit +noecho
# 重置仿真环境语句
reset_gymGame_command = ospath_batch + resetfilename + NoexitAndHostPort
# 执行仿真环境一步语句
runOneStep_gymGame_command = ospath_batch + editandrunfile + NoexitAndHostPort

# runforStep_gymGame_command = ospath_batch + editandrun_str * 20 + NoexitAndHostPort

# 21代表是执行21次 editandrun_str 的宏命令，其中第一步是环境初始化的step,后面20步是后面仿真一个episode的步数
runforStep_gymGame_command = ospath_batch + resetfile + editandrun_str * 21 + NoexitAndHostPort


runforStepTest_gymGame_command = ospath_batch + editandrun_str * 51 + NoexitAndHostPort

runforStepTest_100step = ospath_batch + editandrun_str * 101 + NoexitAndHostPort
"""
    
    用于保存reward、FanPower文件路径
    
"""
savefilepath = 'out/'
# 记录'Reward总和'随着回合次数的变化表
episode_reward_history_csv = savefilepath + "episode_reward_history.csv"
# 记录每个回合中，reward随着步数step次数的变化表
each_episode_rewards_history_csv = savefilepath + "each_episode_rewards_history.csv"
# 记录'FanPower总和'随着回合次数的变化表
FanPower_history_csv = savefilepath + "FanPower_history.csv"
# 记录每个回合中，fanpower随着步数step次数的变化表
each_FanPower_history_csv = savefilepath + "each_FanPower_history.csv"

Loss_history_csv = savefilepath + "Loss_history.csv"
