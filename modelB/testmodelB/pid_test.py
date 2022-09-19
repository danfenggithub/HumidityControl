from HumidityControl.pid import pid_m

# 15 points at 30 second intervals
pid_m.pid(15, 30)

from HumidityControl.pid import pid

# Single point, 30 second interval

# pid.pid(15,  30)
