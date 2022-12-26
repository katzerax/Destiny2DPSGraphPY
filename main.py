import matplotlib.pyplot as plt

# Predefined variables used in the functions, modifiable
data_points = 4500  # please make data_points and xScale in multiples of 10
x_scale = 45  # scale of the X axis
y_scale = 300000  # scale of the Y axis
x_increments = x_scale / data_points

# graph limits
plt.xlim(0, x_scale)
plt.ylim(0, 150000)

# establish x array
x = []
for i in range(data_points):  
    x.append(round(i * x_increments, 5))

# Initialize list to store legend labels
legend_labels = []

def plot_dps_graph(fire_delay, reload_time, damage_per_shot, mag_cap, ammo_reserve, legend_label):
  # Initialize t_dmg list
  t_dmg = []

  shots_fired = 0
  next_fire = fire_delay
  total_damage = 0
  time_elapsed = 0
  shots_fired_total = 0

  for i in range(data_points):
      if shots_fired_total == ammo_reserve:
          total_damage = total_damage
      else:
          if shots_fired == mag_cap:
              next_fire += reload_time
              shots_fired = 0
          elif time_elapsed == next_fire:
              total_damage += damage_per_shot
              next_fire += fire_delay
              next_fire = round(next_fire, 5)
              shots_fired += 1
              shots_fired_total += 1
          else:
              total_damage = total_damage
      time_elapsed += x_increments
      time_elapsed = round(time_elapsed, 8)
      t_dmg.append(total_damage)

  dps = [0]
  for z in range(data_points):
      if z != 0:
          dps.append(t_dmg[z] / x[z])

  plt.plot(x, dps)
  plt.xlabel("Time (Seconds)")
  plt.ylabel("Damage Per Second")

  # Add legend label to list
  legend_labels.append(legend_label)

# example function calls
plot_dps_graph(0.7, 0.5, 56000, 7, 20, "dps 1")
plot_dps_graph(0.6, 0.4, 55000, 8, 25, "dps 2")
plot_dps_graph(0.5, 0.3, 54000, 9, 30, "dps 3")

# Add a legend with all labels
plt.legend(legend_labels)

# Show the plot
plt.show()