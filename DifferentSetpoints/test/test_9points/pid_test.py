from HumidityControl.pid import pid_m
# 9个点，时间间隔30秒
pid_m.pid(9,  30)
#
# from HumidityControl.pid import pid
# # # 单个点，时间间隔30秒
# pid.pid(9,  30)