import numpy as np
from matplotlib import pyplot as plt
import random
import cvxpy as cp

trials = 1000
cost_array = []

for i in range(trials):

    # Variables
    wind_power_capacity = cp.Variable()
    solar_power_capacity = cp.Variable()
    battery_capacity = cp.Variable()

    sunny_hours = 7.3  # these are the equivalent hours during which the solar panels can work at full power

    cloudy_days_in_July_in_Cleveland = 11
    total_days_in_July_in_Cleveland = 31
    cloudy_factor = 1.0
    if np.random.random() < cloudy_days_in_July_in_Cleveland / total_days_in_July_in_Cleveland:
        cloudy_factor = 0.25

    # average wind speed in Ohio in July is 2.5 m/s
    average_wind_speed_in_Ohio_in_July = 4.9 # 2.5
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

    cuyahoga_county_energy_requirement = 481000000  # kWh.  for one day in July

    constraints = []
    constraints += [cuyahoga_county_energy_requirement == 24 * wind_cp * wind_power_capacity + sunny_hours * cloudy_factor * solar_power_capacity] # + battery_capacity]
    cost = wind_cost_per_kw_in_usd * wind_power_capacity + solar_cost_per_kw_in_usd * solar_power_capacity # \
              #  + li_ion_battery_cost_per_kwh_in_usd  * battery_capacity
    # constraints += [battery_capacity >= 0]
    constraints += [solar_power_capacity >= 0]
    constraints += [wind_power_capacity >= 0]

    problem = cp.Problem(cp.Minimize(cost), constraints)

    problem.solve()

    print(problem)
    print("Cost: " + str(problem.value))
    print("Solar kW: " + str(solar_power_capacity.value))
    print("Wind kW: " + str(wind_power_capacity.value))
    print("Battery kWh: " + str(battery_capacity.value))
    print("Cloudiness Factor: " + str(cloudy_factor))
    print("Wind speed: " + str(today_wind_speed))

    cost_array.append(problem.value)

print("Average cost: " + str(sum(cost_array) / len(cost_array)))

print("Min cost: " + str(min(cost_array)))

print("Max cost: " + str(max(cost_array)))
