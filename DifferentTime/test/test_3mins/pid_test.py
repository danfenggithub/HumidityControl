from HumidityControl.pid import pid_m
# 15个点，时间间隔维3min (3*60s)
pid_m.pid(15, 3*60)

# from HumidityControl.pid import pid
# # # 单个点，时间间隔维3min
# pid.pid(15, 3 * 60)
