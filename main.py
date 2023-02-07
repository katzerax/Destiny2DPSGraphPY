import sys
import random
import math
from perks import *

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
    modifier = 0
    perks = []
    # Loop to input weapon data
    while True:
        # Input weapon data
        perks = []
        modifier = 0
        weapon = {}
        weapon["name"] = input("Enter weapon name: ")
        weapon["fire_rate"] = float(input("Enter Rounds Per Minute: "))
        weapon["reload_time"] = float(input("Enter reload time: "))
        weapon["damage_per_shot"] = float(input("Enter damage per shot: "))
        weapon["magazine_capacity"] = int(input("Enter magazine capacity: "))
        weapon["ammo_reserve"] = int(input("Enter ammo reserve: "))
        weapon["delay_first_shot"] = bool(int(input("Enter wether to delay the first shot (1 - true, 0 - false): ")))
        weapon["add_perks"] = bool(int(input("Enter wether to apply perks (1 - true, 0 - false): ")))
        
        if weapon["add_perks"] == True:
            while(modifier!=-1):
                modifier = int(input("Enter a modifier from the following list to add (-1 to stop)\n1) TripleTap\n2) FTTC\n3) VorpalWeapon\n4) FocusedFury\n5) HighImpactReserves\n6) FiringLine\n7) WellOfRadiance\n"))
                if((modifier!=-1) and ((modifier>=1) and (modifier<=7))): #change upper bound with new perks
                    perks.append(modifier)
            weapon["perks"] = perks

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

def plot_dps_graph(fire_rate, reload_time, damage_per_shot, magazine_capacity, ammo_reserve, legend_label, delay_first_shot, add_perks, perks):
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
    shot_dmg_output = damage_per_shot #this is to save the initial starting damage number, and calculate using another variable, makes it so much easier to revert buffs without killing damage
  
    #debug_counter = 0

    #perk variables that so suck
    
    tt_delay = 0 #god please work
    tt_delay_check = 0 #IT WORKED HAHAHAHAHAHAH
    fttc_delay = 0
    fttc_delay_check = 0

    TT_On = False
    FTTC_On = False
    VS_On = False
    CC_On = False
    OF_On = False
    RH_On = False
    VW_On = False
    FF_On = False
    HIR_On = False

    if(add_perks == True):
        for z in range(len(perks)):
            number = perks[z]
            if number == 1:
                TT_On = True
            elif number == 2:
                FTTC_On = True
            elif number == 3:
                VS_On = True
            elif number == 4:
                CC_On = True
            elif number == 5:
                OF_On = True
            elif number == 6:
                RH_On = True
            elif number == 7:
                VW_On = True
            elif number == 8:
                FF_On = True
            elif number == 9:
                HIR_On = True


    # Calculate total damage over time
    for i in range(data_points):
        shot_dmg_output = damage_per_shot
        if TT_On:
            shots_left_mag, shots_left_reserve, tt_delay, tt_delay_check = TripleTap(shots_fired,shots_left_mag,shots_left_reserve,tt_delay,tt_delay_check)
        if FTTC_On:
            shots_left_mag, shots_left_reserve, fttc_delay, fttc_delay_check = FTTC(shots_fired,shots_left_mag,shots_left_reserve,fttc_delay,fttc_delay_check)
        if VS_On:
            print("remove")
        if CC_On:
            print("remove")
        if OF_On:
            print("remove")
        if RH_On:
            print("remove")
        if VW_On:
            print("remove")
        if FF_On:
            print("remove")
        if HIR_On:
            shot_dmg_output = HighImpactReserves(shots_left_mag,magazine_capacity,shot_dmg_output)
        if shots_left_reserve == 0: # reserve check
            total_damage = total_damage
        elif shots_left_mag == 0: # reload
            next_fire += reload_time
            next_fire -= fire_delay if delay_first_shot == 0 else 0 #roxy: previously was waiting for fire delay, 
            next_fire = round(next_fire, roundingcoeff) #even when the weapon would not be a charge weapon (contributed to rockets looking bad)
            shots_fired = 0 #resetting shots fired for triple tap and fourth times the charm on reload
            shots_left_mag = magazine_capacity
        elif time_elapsed == next_fire: # checks for weapon fire rate
            total_damage += shot_dmg_output
            next_fire += fire_delay
            next_fire = round(next_fire, roundingcoeff) #rounding because i love python
            shots_fired += 1
            shots_left_mag -= 1
            shots_left_reserve -= 1
        time_elapsed += x_increments
        time_elapsed = round(time_elapsed, roundingcoeff)       

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
    if 'perks' in weapon:
        plot_dps_graph(weapon['fire_rate'], weapon['reload_time'], weapon['damage_per_shot'], weapon['magazine_capacity'], weapon['ammo_reserve'], weapon['name'], weapon['delay_first_shot'], weapon['add_perks'], weapon['perks'])
    else:
        perks = []
        plot_dps_graph(weapon['fire_rate'], weapon['reload_time'], weapon['damage_per_shot'], weapon['magazine_capacity'], weapon['ammo_reserve'], weapon['name'], weapon['delay_first_shot'], weapon['add_perks'], perks)
# Add a legend with all labels
plt.legend(legend_labels)

# Show the plot
plt.show()
