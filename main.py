import numpy as np
from matplotlib import pyplot as plt
import random
import cvxpy as cp

# Variables
wind_power_capacity = cp.Variable()
solar_power_capacity = cp.Variable()
battery_capacity = cp.Variable()
energy_in_battery = cp.Variable(24)
starting_energy = 160000000

# Constants
# right now, the sun variables approximates the sun in Fairview Park, Ohio on July 15
x = np.linspace(-np.pi + 8 * np.pi / 24, np.pi + 8 * np.pi / 24, 24)
sun = np.sin(x)
for index, elem in np.ndenumerate(sun):
    if elem < 0:
        sun[index] = 0
print(sum(sun))

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
today_wind_speed = abs(random.gauss(average_wind_speed_in_Ohio_in_July, wind_speed_standard_deviation))

wind_cp = 0
if today_wind_speed > 12:
    wind_cp = 0.5
elif today_wind_speed < 3:
    wind_cp = 0
else:
    wind_cp = (0.5 / 9) * today_wind_speed - (1 / 6)
wind_cp *= 2

wind_cost_per_kw_in_usd = 1300
solar_cost_per_kw_in_usd = 3000
li_ion_battery_cost_per_kwh_in_usd = 153

cuyahoga_county_energy_requirement = np.array([40, 38.3, 36.6, 35, 33.3, 31.7,  # midnight to 5am
                                               30, 31.7, 33.3, 35, 36.6, 38.3,  # 6am to 11am
                                               40, 43.3, 45, 46.7, 48.3, 51,  # noon to 5pm
                                               49.3, 46.7, 45, 43.3, 41.7, 40])  # 6pm to 11pm
cuyahoga_county_energy_requirement = cuyahoga_county_energy_requirement / 2  # oops.  I was off my a factor of two
# when I was typing all that in.  this line fixes it.
cuyahoga_county_energy_requirement *= 1000  # converting from GWh to MWh
cuyahoga_county_energy_requirement *= 1000  # converting from MWh to kWh

constraints = []
constraints += [solar_power_capacity >= 0]
constraints += [wind_power_capacity >= 0]
constraints += [battery_capacity >= starting_energy]

for i in range(24):
    constraints += [battery_capacity >= energy_in_battery[i]]
    # constraints += [energy_in_battery[i] >= 0]
    constraints += [energy_in_battery[i] >= cuyahoga_county_energy_requirement[i]]
    # Energy[hour i] = wind speed[hour i] * wind CP [wind speed[hour i]] * wind capacity
    # + solar capacity * sunlight[ hour i] * cloudiness factor[hour i] + energy[hour i - 1]
    # - requirement[hour i ]
    if i == 0:
        constraints += [energy_in_battery[i] == wind_cp * wind_power_capacity +
                        solar_power_capacity * cloudy_factor * sun[i] + starting_energy
                        - cuyahoga_county_energy_requirement[i]]
    else:
        constraints += [energy_in_battery[i] == today_wind_speed * wind_cp * wind_power_capacity +
                        solar_power_capacity * cloudy_factor * sun[i] + energy_in_battery[i - 1]
                        - cuyahoga_county_energy_requirement[i]]
    # constraints += [energy_in_battery[23] == starting_energy]

    cost = wind_cost_per_kw_in_usd * wind_power_capacity + solar_cost_per_kw_in_usd * solar_power_capacity \
           + li_ion_battery_cost_per_kwh_in_usd * battery_capacity

problem = cp.Problem(cp.Minimize(cost), constraints)

# print(wind_cost_per_kw_in_usd*wind_power_capacity + solar_cost_per_kw_in_usd*solar_power_capacity+li_ion_battery_cost_per_kwh_in_usd*battery_capacity)

problem.solve()

print(problem)
print("Cost: " + str(problem.value))
print("Solar kW: " + str(solar_power_capacity.value))
print("Wind kW: " + str(wind_power_capacity.value))
print("Battery kWh: " + str(battery_capacity.value))
print("Cloudiness Factor: " + str(cloudy_factor))
print("Wind speed: " + str(today_wind_speed))

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#    print(np.sum(cuyahoga_county_energy_requirement))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
