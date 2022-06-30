from HumidityControl.pid import pid_m
# 15个点，时间间隔30秒
pid_m.pid(21,  30)

# from HumidityControl.pid import pid
# # # 单个点，时间间隔30秒
# pid.pid(21,  30)