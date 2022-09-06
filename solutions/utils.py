def discounted_returns(returns, gamma=0.5):
    G = 0
    for i in range(len(returns)):
        G += returns[i] * gamma ** i
    return G


import json
import os


def getMassFraction(T, RH):
    """
        温度、湿度对应的空气水分子质量分数
    :param T: 室内某点的温度
    :param RH: 室内某点的湿度
    :return MFdata: 空气水分子质量分数
    """
    with open(os.path.dirname(os.path.realpath(__file__)) + "/MFdata.json", 'r') as f:
        data = json.load(f)
        T = str(T)
        RH = str(RH)

        # hum_ratio为含湿量
        # hum_ratio is moisture content
        hum_ratio = data[T][RH]
        h2o_ratio = float(hum_ratio) / 1000
        h2o_ratio = round(h2o_ratio, 7)
        air_ratio = float(1) - h2o_ratio

        # 格式化数据
        # Format data
        MFdata = '{' + str(h2o_ratio) + ',' + str(air_ratio) + '}'

        return MFdata

import sys
import time


# 控制台输出记录到文件
class Logger(object):
    def __init__(self, file_name="Default.log", stream=sys.stdout):
        self.terminal = stream
        self.log = open(file_name, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


def log():
    # Log file location setting
    # 自定义目录存放日志文件
    log_path = 'out/logs/'
    # 日志文件名按照程序运行时间设置
    log_file_name = log_path + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.log'
    # 记录正常的 print 信息
    sys.stdout = Logger(log_file_name)
    # 记录 traceback 异常信息
    sys.stderr = Logger(log_file_name)


from .gymProfile import *


def checkExistFile():
    # 删除系统中存在的历史文件
    # Delete history files
    if os.path.exists(episode_reward_history_csv):
        os.remove(episode_reward_history_csv)
    if os.path.exists(each_episode_rewards_history_csv):
        os.remove(each_episode_rewards_history_csv)
    if os.path.exists(FanPower_history_csv):
        os.remove(FanPower_history_csv)
    if os.path.exists(each_FanPower_history_csv):
        os.remove(each_FanPower_history_csv)
    if os.path.exists(Loss_history_csv):
        os.remove(Loss_history_csv)

