from HumidityControl.pid import pid_m
# 15 points at 30 second intervals
pid_m.pid(21,  30)

# from HumidityControl.pid import pid
# # A single point with a time interval of 30 seconds
# pid.pid(21,  30)