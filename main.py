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
    modifier = 0
    modifiers = []
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
        weapon["add_modifiers"] = bool(int(input("Enter wether to apply modifiers (1 - true, 0 - false): ")))
        
        if weapon["add_modifiers"] == True:
            while(modifier!=-1):
                modifier = int(input("Enter a modifier from the following list to add (-1 to stop)\n1) TripleTap\n2) FTTC\n3) VorpalWeapon\n4) FocusedFury\n5) HighImpactReserves\n6) FiringLine\n7) WellOfRadiance\n"))
                if((modifier!=-1) and ((modifier>=1) and (modifier<=7))): #change upper bound with new modifiers
                    modifiers.append(modifier)
            weapon["modifiers"] = modifiers

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

def plot_dps_graph(fire_rate, reload_time, damage_per_shot, magazine_capacity, ammo_reserve, legend_label, delay_first_shot, add_modifiers, modifiers):
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
    

    # Calculate total damage over time
    for i in range(data_points):
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
            shots_left_mag -= 1
            shots_left_reserve -= 1
        else: #non statement if the gun is out of ammo, but keeps the cycle running so the rest of the graph works
            total_damage = total_damage
        time_elapsed += x_increments
        time_elapsed = round(time_elapsed, roundingcoeff)

#idk if it should go here but fuck it we ball
#roxy here - fix your fucking code !!!!
#        if(add_modifiers==True):
#           total_damage = applyModifiers(modifiers, total_damage, time_elapsed, shots_left_mag, shots_left_reserve, shot_dmg_output, shots_fired, magazine_capacity, damage_per_shot) #add to with whatever the functions need
        

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


#def applyModifiers(modifiers, total_damage, time_elapsed, shots_left_mag, shots_left_reserve, shot_dmg_output, shots_fired, magazine_capacity, damage_per_shot):
#    i = 0
#    modifier = 0
#    total_damage = total_damage
#    for i in range(modifiers):
#        modifier = modifiers[i]
#        if(modifier == 1):
#            total_damage = TripleTap(shots_fired,shots_left_mag,shots_left_reserve)
#        elif(modifier == 2):
#            total_damage = FTTC(shots_fired,shots_left_mag,shots_left_reserve)
#        elif(modifier == 3):
#            total_damage = VorpalWeapon(shot_dmg_output) #vorpalactive is not a variable yet? so not passing it, same with other "Active" vars later
#        elif(modifier == 4):
#            total_damage = FocusedFury(shots_fired,magazine_capacity,damage_per_shot,time_elapsed)
#        elif(modifier == 5):
#            total_damage = HighImpactReserves(shots_left_mag,magazine_capacity,damage_per_shot)
#        elif(modifier == 6):
#            total_damage = FiringLine(shot_dmg_output)
#        elif(modifier == 7):
#            total_damage = WellofRadiance()
#        modifier = 0
#    return(total_damage) #example of what this function will be like. 


for weapon in weaponData['weapons']:
	plot_dps_graph(weapon['fire_rate'], weapon['reload_time'], weapon['damage_per_shot'], weapon['magazine_capacity'], weapon['ammo_reserve'], weapon['name'], weapon['delay_first_shot'], weapon['add_modifiers'], weapon['modifiers'])

# Add a legend with all labels
plt.legend(legend_labels)

# Show the plot
plt.show()
