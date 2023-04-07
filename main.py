import numpy as np
from matplotlib import pyplot as plt
import random
import cvxpy as cp

# Variables
wind_power_capacity = cp.Variable()
solar_power_capacity = cp.Variable()
battery_capacity = cp.Variable()
energy_in_battery = cp.Variable(24)

# Constants
# right now, the sun variables approximates the sun in Fairview Park, Ohio on July 15
x = np.linspace(-np.pi + 8 * np.pi/24, np.pi + 8 * np.pi/24, 24)
sun = np.sin(x)
for index, elem in np.ndenumerate(sun):
    if elem < 0:
        sun[index] = 0
# print(sun)

# there are eleven cloudy days in July in Cleveland Ohio
# if it is cloudy, it is cloudy all day.
# if it is cloudy, solar panels work at 0.25 efficiency.
# with this setup, we'll have to run the optimizer multiple (many) times.
cloudy_days_in_July_in_Cleveland = 11
total_days_in_July_in_Cleveland = 31
cloudy_factor = 1.0
if np.random.random() < cloudy_days_in_July_in_Cleveland / total_days_in_July_in_Cleveland:
    cloudy_factor = 0.25

# average wind speed in Ohio in July is 2.5 m/s
average_wind_speed_in_Ohio_in_July = 2.5
# I'm not sure what standard deviation to use for wind speed.  From looking at a graph I found, it could be as high
# as 3 m/s. I found some text that suggested it could be as low as 0.4 or even 0.08. we'll go with 1.5 m/s
wind_speed_standard_deviation = 1.5
today_wind_speed = random.gauss(average_wind_speed_in_Ohio_in_July, wind_speed_standard_deviation)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/