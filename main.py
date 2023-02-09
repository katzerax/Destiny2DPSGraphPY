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
    perk = 0
    perks = []
    # Loop to input weapon data
    while True:
        # Input weapon data
        perks = []
        perk = 0
        weapon = {}
        weapon["name"] = input("Enter weapon name: ")
        weapon["fire_rate"] = float(input("Enter Rounds Per Minute: "))
        weapon["reload_time"] = float(input("Enter reload time: "))
        weapon["damage_per_shot"] = float(input("Enter damage per shot: "))
        weapon["magazine_capacity"] = int(input("Enter magazine capacity: "))
        weapon["ammo_reserve"] = int(input("Enter ammo reserve: "))
        weapon["delay_first_shot"] = bool(int(input("Enter whether to delay the first shot (1 - true, 0 - false): ")))
        weapon["add_perks"] = bool(int(input("Enter whether to apply perks (1 - true, 0 - false): ")))
        
        if weapon["add_perks"] == True:
            weapon["enhanced_perks"] = bool(int(input("Assume all perks are enhanced? (1 - true, 0 - false): ")))
            weapon["weapon_class"] = int(input("Weapon Ammo Type (1 - Primary, 2 - Special, 3 - Heavy): "))
            print("Enter a perk from the following list to add:\n1) Triple Tap\n2) Fourth Time's\n3) Veist Stinger\n4) Clown Cartidge\n5) Overflow\n6) Rapid Hit\n7) Vorpal Weapon\n8) Focused Fury\n9) High Impact Reserves\n10) Firing Line\n11) Explosive Light\n12) Cascade Point\n13) Explosive Payload\nEnter -1 to Stop\n")
            teehee = 0
            while(perk!=-1):
                teehee += 1
                [print("Perk", teehee)]
                perk = int(input("input: "))
                if((perk!=-1) and ((perk>=1) and (perk<=13))): #change upper bound with new perks
                    perks.append(perk)
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

def plot_dps_graph(fire_rate, reload_time, damage_per_shot, magazine_capacity, ammo_reserve, legend_label, delay_first_shot, add_perks, perks, enhanced_perks, weapon_class):
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
    output_reload_time = round(reload_time, roundingcoeff) #same as above :p

    #debug_counter = 0

    #perk variables that so suck
    #1 - Triple Tap
    tt_delay = 0 #god please work
    tt_delay_check = 0 #IT WORKED HAHAHAHAHAHAH
    #2 - Fourth Time's the Charm
    fttc_delay = 0
    fttc_delay_check = 0
    #3 - Veist Stinger
    veist_overflow_cross = 0
    veist_check = 0 #arbitrary number that isnt 0 so the logic works, there is probably better way like assuming if shots is 0 or something idk
    #4 - Clown Cartridge
    clown_check = 0
    reload_count = 0
    #5 - Overflow
    of_check = 0
    #6 - Rapid Hit
    rh_stacks = 0
    #8 - Focused Fury
    ff_time_check = 0
    FFActive = 0
    shots_fired_ff = 0
    #12 - Cascade Point
    cascade_fr = 0

    #it was sobbing that i didnt declare ones that were not flagged as true
    TT_On = False
    FTTC_On = False
    VS_On = False
    CC_On = False
    OF_On = False
    RH_On = False
    VW_On = False
    FF_On = False
    HIR_On = False
    FL_On = False
    EL_On = False
    CasP_On = False
    EP_On = False

    #debug
    stale_value = 0

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
            elif number == 10:
                FL_On = True
            elif number == 11:
                EL_On = True
            elif number == 12:
                CasP_On = True
            elif number == 13:
                EP_On = True


    # Calculate total damage over time
    for i in range(data_points):

        #perks
        shot_dmg_output = damage_per_shot
        fire_delay = round(60/fire_rate, roundingcoeff)
        output_reload_time = round(reload_time, roundingcoeff)
        if TT_On: #1
            shots_left_mag, shots_left_reserve, tt_delay, tt_delay_check = TripleTap(shots_fired,shots_left_mag,shots_left_reserve,tt_delay,tt_delay_check)
        if FTTC_On: #2
            shots_left_mag, shots_left_reserve, fttc_delay, fttc_delay_check = FTTC(shots_fired,shots_left_mag,shots_left_reserve,fttc_delay,fttc_delay_check)
        if VS_On: #3
            shots_left_mag, veist_check = VeistStinger(shots_fired,shots_left_mag,magazine_capacity,veist_overflow_cross,veist_check)
        if CC_On: #4
            clown_check, shots_left_mag = ClownCartridge(magazine_capacity, shots_left_mag, clown_check, reload_count)
        if OF_On: #5
            shots_left_mag, of_check, veist_overflow_cross = Overflow(shots_left_mag,of_check,delay_first_shot,veist_overflow_cross,magazine_capacity)
        if RH_On: #6
            if shots_left_mag == 0:
                output_reload_time = RapidHit(output_reload_time,rh_stacks,shots_fired,roundingcoeff)
        if VW_On: #7
            shot_dmg_output = VorpalWeapon(weapon_class,shot_dmg_output)
        if FF_On: #8
            shot_dmg_output, FFActive, ff_time_check, shots_fired_ff = FocusedFury(FFActive,shots_fired_ff,magazine_capacity,time_elapsed,shot_dmg_output,ff_time_check)
        if HIR_On: #9
            if enhanced_perks == 1:
                shot_dmg_output = HIREnhanced(shots_left_mag,magazine_capacity,shot_dmg_output)
            else:
                shot_dmg_output = HighImpactReserves(shots_left_mag,magazine_capacity,shot_dmg_output)
        if FL_On: #10
            shot_dmg_output = FiringLine(shot_dmg_output)
        #if EL_On: #11
        if CasP_On: #12
            fire_delay = CascadePoint(fire_delay,roundingcoeff,fire_rate,cascade_fr)
        if EP_On: #13
            shot_dmg_output = ExplosivePayload(shot_dmg_output)

        #debug on seeing how the damage changes
        #if weapon['name'] == ('all'):
            #if stale_value != shot_dmg_output:
                #stale_value = shot_dmg_output
                #print(weapon['name'], "dmg: ", shot_dmg_output, "time: ", time_elapsed)

        #weapon firing
        if shots_left_reserve == 0: # reserve check
            total_damage = total_damage
        elif shots_left_mag == 0: # reload
            next_fire += output_reload_time
            next_fire -= fire_delay if delay_first_shot == 0 else 0 #roxy: previously was waiting for fire delay, 
            next_fire = round(next_fire, roundingcoeff) #even when the weapon would not be a charge weapon (contributed to rockets looking bad)
            shots_fired = 0 #resetting shots fired for triple tap and fourth times the charm on reload
            reload_count += 1 #so Clown knows to not check
            shots_left_mag = magazine_capacity
        elif time_elapsed == next_fire: # checks for weapon fire rate
            total_damage += shot_dmg_output
            next_fire += fire_delay
            next_fire = round(next_fire, roundingcoeff) #rounding because i love python
            shots_fired += 1
            shots_fired_ff += 1 #for focused fury specifically :P
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
        plot_dps_graph(weapon['fire_rate'], weapon['reload_time'], weapon['damage_per_shot'], weapon['magazine_capacity'], weapon['ammo_reserve'], weapon['name'], weapon['delay_first_shot'], weapon['add_perks'], weapon['perks'], weapon['enhanced_perks'], weapon['weapon_class'])
    else:
        perks = []
        plot_dps_graph(weapon['fire_rate'], weapon['reload_time'], weapon['damage_per_shot'], weapon['magazine_capacity'], weapon['ammo_reserve'], weapon['name'], weapon['delay_first_shot'], weapon['add_perks'], perks)

# Add a legend with all labels
plt.legend(legend_labels)

# Show the plot
plt.show()