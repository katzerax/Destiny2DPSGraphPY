import sys
from modifiers import *

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib is not installed\npip install matplotlib")
    sys.exit()

import argparse, json

agp = argparse.ArgumentParser()
agp.add_argument("-im", "--input-mode", default="file", choices=["file", "cli"], type=str, help="mode for inputting data. options: 'file' or 'cli'. default: 'file'")
agp.add_argument("-rf", "--read-file", default="weapons.json", type=str, help="file of weapon information to read. default: weapons.json")
agp.add_argument("-d", "--dialogue", default="y", choices=["y","n"], type=str, help="beginner friendly dialogue to choose between input modes. options: 'y' or 'n'. default: 'y'")

args = agp.parse_args()

if args.dialogue == "y":
    print("*Note: this dialogue can be toggled off using '-d n' or '--dialogue n' from the command line")
    choice = ""
    while choice not in ("cli", "file"):
        choice = input("Choose an input mode:\n\tcli - input weapon information via command line\n\tfile - input weapon information via the 'weapons.json' file\n")
    args.input_mode = choice

if args.input_mode == "cli":
    # Initialize list to store weapon dictionaries
    weapons = []
    
    # Loop to input weapon data
    while True:
        # Input weapon data
        weapon = {}
        weapon["name"] = input("Enter weapon name: ")
        weapon["fire_rate"] = float(input("Enter Rounds Per Minute: "))
        weapon["reload_time"] = float(input("Enter reload time: "))
        weapon["damage_per_shot"] = float(input("Enter damage per shot: "))
        weapon["magazine_capacity"] = int(input("Enter magazine capacity: "))
        weapon["ammo_reserve"] = int(input("Enter ammo reserve: "))
        weapon["delay_first_shot"] = bool(int(input("Enter wether to delay the first shot (1 - true, 0 - false): ")))
        
        # Add weapon to list
        weapons.append(weapon)
        
        # Check if user wants to add more weapons
        add_more = input("Add more weapons? (y/n) ")
        if add_more.lower() != "y":
            break
    
    # Write weapons data to JSON file
    with open(args.read_file, "w") as f:
        json.dump({"weapons": weapons}, f)

# Read weapon data from JSON file
with open(args.read_file, "r") as f:
    weaponData = json.load(f)


# Predefined variables used in the functions, modifiable
data_points = 45000  # please make data_points and x_scale in multiples of 10
x_scale = 45  # scale of the X axis
y_scale = 300000  # scale of the Y axis // roxy: could we find the peak of the graph and set this to be 105% of said peak?
x_increments = x_scale / data_points

# graph limits
plt.xlim(0, x_scale)
plt.ylim(0, y_scale)

# establish x array
x = []
for i in range(data_points):  
    x.append(round(i * x_increments, 5))

# Initialize list to store legend labels
legend_labels = []

def plot_dps_graph(fire_rate, reload_time, damage_per_shot, magazine_capacity, ammo_reserve, legend_label, delay_first_shot):
    # Initialize t_dmg list
    t_dmg = []
    roundingcoeff = len(str(x_increments).split(".")[1])
    fire_delay = round(60/fire_rate, roundingcoeff) #conversion from RPM to time in seconds between shots
    next_fire = fire_delay
    total_damage = 0 if delay_first_shot else damage_per_shot
    time_elapsed = 0
    shots_left_reserve = ammo_reserve if delay_first_shot else (ammo_reserve - 1)
    shots_left_mag = magazine_capacity if delay_first_shot else (magazine_capacity - 1)
    shots_fired = 0 if delay_first_shot else 1
    

    # Calculate total damage over time
    for i in range(data_points):
        if shots_left_reserve == 0:
            total_damage = total_damage
        elif shots_left_mag == 0:
            next_fire += reload_time
            next_fire -= fire_delay if delay_first_shot == 0 else 0 #roxy: previously was waiting for fire delay, 
            next_fire = round(next_fire, 5) #even when the weapon would not be a charge weapon (contributed to rockets looking bad)
            shots_fired = 0 #resetting shots fired for triple tap and fourth times the charm
            shots_left_mag = magazine_capacity
        elif time_elapsed == next_fire:
            total_damage += damage_per_shot
            next_fire += fire_delay
            next_fire = round(next_fire, 5)
            shots_left_mag -= 1
            shots_left_reserve -= 1
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

for weapon in weaponData['weapons']:
	plot_dps_graph(weapon['fire_rate'], weapon['reload_time'], weapon['damage_per_shot'], weapon['magazine_capacity'], weapon['ammo_reserve'], weapon['name'], weapon['delay_first_shot'])

# Add a legend with all labels
plt.legend(legend_labels)

# Show the plot
plt.show()