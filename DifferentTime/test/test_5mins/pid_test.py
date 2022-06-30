from HumidityControl.pid import pid_m
# 15个点，时间间隔维5min
pid_m.pid(15,  5*60)


# from HumidityControl.pid import pid
# # # 单个点，时间间隔维5min
# pid.pid(15,  5*60)