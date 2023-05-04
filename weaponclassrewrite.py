import stat
import math
import random

# Myssto:
#
# Migrated a couple things:
# I changed the way you list and retrieve weapons
# Before you were storing each instance of Weapon in each instance of Weapon (if that makes sense)
# This kinda defeats the purpose of OOP in the first place :P
# - classmethods list_weapon and add_to_list
# + global function create_weapon
# + global dictionary weapons_list
# Now you have a global list of Weapons where each instance is only added a single time
# I changed your test cases at the bottom to show correct usage :)
# PLUS IT MAKES WORKING WITH THE FRONTEND SO MUCH EASIER!!!
# AND IT SETS UP THE SKELETON FOR LOADING WEAPON CONFIGS!!!

PERKS_LIST = {
    0: ("Null", "No selection"),
    1: ("Triple Tap", "Landing 3 precision hits refunds 1 ammo back to the magazine for free."),
    2: ("Fourth Times the Charm", "Landing 4 precision hits refunds 2 ammo back to the magazine for free."),
    3: ("Perk 3", "Description"),
    4: ("Perk 4", "Description"),
}

BUFFS_LIST = {
    0: ("Null", "No selection"),
    1: ("Well of Radiance", "Super that gives healing and damage bonus in an area.")
}

weapons_list = {

}

def create_weapon(weapon_settings: dict):
    new_weapon = Weapon(**weapon_settings)
    weapons_list[str(weapon_settings['name'])] = new_weapon

class Weapon:
    def __init__(self, name:str, fire_rate:float, reload_time:float, damage_per_shot:int, mag_cap:int, ammo_total:int, delay_first_shot:bool=False, burst_weapon:bool=False, burst_bullets:int=0, swap_group:int=0, swap_time:float=0, perk_indices:list=[], buff_indices:list=[]):
        # Set positional args
        self.name = name
        self.fire_rate = fire_rate
        self.reload_time = reload_time
        self.damage_per_shot = damage_per_shot
        self.mag_cap = mag_cap
        self.ammo_total = ammo_total

        # Set variadic args
            # These are validated inherintly by typing and defaulting in the constructor :)
        self.perk_indices = perk_indices
        self.buff_indices = buff_indices

        # This input validation for burst and swap may be redundant
        # because we will need to validate in the frontend anyway
        if not burst_weapon or not burst_bullets:
            self.burst_weapon = False
            self.burst_bullets = 0
        else:
            if burst_bullets <= 0:
                self.burst_weapon = 0
                self.burst_bullets = 0
            else:
                self.burst_weapon = burst_weapon
                self.burst_bullets = burst_bullets

        if swap_time <= 0:
            self.swap_group = 0
            self.swap_time = 0
        else:
            self.swap_group = swap_group
            self.swap_time = swap_time

        if delay_first_shot is None:
            self.delay_first_shot = 0
        else:
            self.delay_first_shot = delay_first_shot

    def add_perk(self, perk_index):
        if perk_index not in self.perk_indices and perk_index in PERKS_LIST:
            self.perk_indices.append(perk_index)

    def remove_perk(self, perk_index):
        if perk_index in self.perk_indices:
            self.perk_indices.remove(perk_index)

    def has_perk(self, perk_index):
        return perk_index in self.perk_indices

    def get_perks(self):
        return self.perk_indices

    def set_dfs(self, boolean):
        self.delay_first_shot = boolean

    def get_any_perk_description(self, perk_index):
        return PERKS_LIST.get(perk_index)
    
    # Getting the individual attributes
    def get_name(self):
        return self.name

    def get_fire_rate(self):
        return self.fire_rate

    def get_reload_time(self):
        return self.reload_time

    def get_damage_per_shot(self):
        return self.damage_per_shot

    def get_mag_cap(self):
        return self.mag_cap

    def get_ammo_total(self):
        return self.ammo_total
    
    def get_dfs(self):
        return self.delay_first_shot
    
    def get_burst_variable(self):
        return self.burst_weapon
    
    def get_burst_bullets(self):
        return self.burst_bullets
    
    def get_swap_group(self):
        return self.swap_group
    
    def get_swap_time(self):
        return self.swap_time
    
class Damage:
    def __init__(self, weapon_instance):
        self.weapon_instance = weapon_instance

    def print_weapon_instance(self):
        print(self.weapon_instance.get_perks())

    # Graph config
    ticks = 45000
    x_increments = 0.01
    x = []
    for i in range(ticks):
        x.append(round(i * x_increments, 5))
    round_coeff = len(str(x_increments).split(".")[1])

    @classmethod
    def DamageCalculate(cls):
        for weapon in weapons_list.values():
            if not weapon.get_swap_group():

                #general variables
                t_dmg = []
                time_elapsed = 0
                total_damage = 0

                Damage.TripleTapClear()
                Damage.FTTCClear()
                Damage.VeistStingerClear()
                Damage.BNSClear()

                #weapon variables
                ammo_fired = 0
                burst_shot = 0

                delay_first_shot = weapon.get_dfs()
                burst_weapon = weapon.get_burst_variable()

                fire_stale = weapon.get_fire_rate()

                if not burst_weapon:
                    fire_delay = round(60/fire_stale, cls.round_coeff)

                #this rate of fire calculation may need some looking at :P, but basically it takes a rate of fire and then
                #just cuts it in half, half to shoot in a burst, the other to pause between shots..
                #for delay first shot, might just have it be equal to the normal fire delay? who knows.
                #5 minutes later roxy here: i made DFS burst weapons have to complete a full charge sequence despite '120 RPM' not actually meaning 120 rpm... it just means 500ms charge time (since 500ms = 2 shots/second = 120rpm? idfk)
                elif burst_weapon:
                    burst_bullets = weapon.get_burst_bullets()
                    fire_delay = round((60/fire_stale)/2, cls.round_coeff)
                    burst_delay = round(((60/fire_stale)/2)/burst_bullets, cls.round_coeff)

                dfs_delay = round(60/fire_stale, cls.round_coeff)

                fire_timer = dfs_delay if delay_first_shot else 0
                reload_time = weapon.get_reload_time()

                mag_cap = weapon.get_mag_cap()
                ammo_magazine = mag_cap

                ammo_total = weapon.get_ammo_total()

                damage_per_shot = weapon.get_damage_per_shot()
                dmg_output = damage_per_shot

                applied_perks = weapon.get_perks()
                number_to_flag = {1: "TT_On", 2: "FTTC_On", 3: "VS_On", 10: "FL_On", 15: "BNS_On"}
                flags = {"TT_On": False, "FTTC_On": False, "VS_On": False, "FL_On": False, "BNS_On": False} 

                stale_val = 0

                for number in applied_perks:
                    if number in number_to_flag:
                        flags[number_to_flag[number]] = True

                for i in range(cls.ticks):

                    dmg_output = damage_per_shot

                    if flags["TT_On"]: #1
                        ammo_magazine, ammo_total = Damage.TripleTap(ammo_magazine, ammo_total, ammo_fired)
                    if flags["FTTC_On"]: #2
                        ammo_magazine, ammo_total = Damage.FourthTimesTheCharm(ammo_magazine, ammo_total, ammo_fired)
                    if flags["VS_On"]: #3
                        ammo_magazine = Damage.VeistStinger(ammo_fired, ammo_magazine, mag_cap)
                    if flags["FL_On"]: #10
                        dmg_output = Damage.FiringLine(dmg_output)
                    if flags["BNS_On"]: #15
                        dmg_output = Damage.BaitNSwitch(ammo_fired, dmg_output, time_elapsed)

                    if not burst_weapon:
                        if ammo_total == 0:
                            total_damage = total_damage
                        elif ammo_magazine == 0:
                            fire_timer += reload_time
                            fire_timer -= fire_delay if delay_first_shot == True else 0
                            fire_timer = round(fire_timer, cls.round_coeff)
                            ammo_fired = 0
                            ammo_magazine = mag_cap
                        elif time_elapsed >= fire_timer:
                            total_damage += dmg_output
                            fire_timer += fire_delay
                            fire_timer = round(fire_timer, cls.round_coeff)
                            ammo_fired += 1
                            ammo_magazine -= 1
                            ammo_total -= 1
                            #print("damage:",total_damage,"| fire timer:", fire_timer, "| magazine:", ammo_magazine)
                        
                        time_elapsed += cls.x_increments
                        time_elapsed = round(time_elapsed, 5)
                        t_dmg.append(total_damage)
                        if stale_val != t_dmg[i]:
                            if i != 0:
                                print("name:", weapon.get_name(), "| damage at", (i/100) ,"seconds:", t_dmg[i], "| dps:[",round(t_dmg[i]/(i/100), 1),"]","| per shot:<", dmg_output, ">")
                                stale_val = t_dmg[i]

                    elif burst_weapon:
                        if ammo_total == 0:
                            total_damage = total_damage
                        elif ammo_magazine == 0:
                            fire_timer += reload_time
                            fire_timer -= fire_delay if delay_first_shot else 0
                            fire_timer = round(fire_timer, cls.round_coeff)
                            ammo_fired = 0
                            ammo_magazine = mag_cap
                        elif time_elapsed >= fire_timer:
                            if burst_shot >= 0 and burst_shot < burst_bullets:

                                fire_timer += burst_delay
                                fire_timer = round(fire_timer, cls.round_coeff)
                                total_damage += dmg_output
                                burst_shot += 1

                                ammo_fired += 1
                                ammo_magazine -= 1
                                ammo_total -= 1
                            elif burst_shot >= burst_bullets:
                                burst_shot = 0
                                fire_timer += (dfs_delay - burst_delay) if delay_first_shot else fire_delay
                                fire_timer = round(fire_timer, cls.round_coeff)
                    
                        time_elapsed += cls.x_increments
                        time_elapsed = round(time_elapsed, 5)
                        t_dmg.append(total_damage)
                        if stale_val != t_dmg[i]:
                            if i != 0:
                                print("name:", weapon.get_name(), "| damage at", (i/100) ,"seconds:", t_dmg[i], "| dps:[",round(t_dmg[i]/(i/100), 1),"]","| per shot:<", dmg_output, ">")
                                stale_val = t_dmg[i]

                dps = [0]
                for i in range(cls.ticks):
                    if i != 0:
                        dps.append(t_dmg[i] / cls.x[i])

                #print("name:", weapons_list[z].get_name(), "| dps at 10 seconds:", dps[999])
                #print("name:", weapons_list[z].get_name(), "| dps at 13 seconds:", dps[1299])
                #print("name:", weapons_list[z].get_name(), "| dps at 20 seconds:", dps[1999])

    #im going to cry myself to sleep trying to figure out what the hell this is going to do for me!!!
    #this can likely be integrated into the main function that just checks for whether swap_group = 0 or not

    #triple tap - 1
    tt_addcheck = 0
    tt_ammocheck = 0

    @classmethod
    def TripleTapClear(cls):
        cls.tt_addcheck = 0
        cls.tt_ammocheck = 0

    @classmethod
    def TripleTap(cls, ammo_magazine, ammo_total, ammo_fired):

        if ammo_fired != 0:
            if cls.tt_addcheck == 0:
                if ammo_fired % 3 == 0:
                    ammo_magazine += 1
                    ammo_total += 1
                    cls.tt_addcheck = 1
                    cls.tt_ammocheck = ammo_fired
            else:
                if cls.tt_ammocheck != ammo_fired:
                    cls.tt_addcheck = 0

        return ammo_magazine, ammo_total
    
    #fourth times the charm - 2
    fttc_addcheck = 0
    fttc_ammocheck = 0

    @classmethod
    def FTTCClear(cls):
        cls.fttc_addcheck = 0
        cls.fttc_ammocheck = 0

    @classmethod
    def FourthTimesTheCharm(cls, ammo_magazine, ammo_total, ammo_fired):

        if ammo_fired != 0:
            if cls.fttc_addcheck == 0:
                if ammo_fired % 4 == 0:
                    ammo_magazine += 2
                    ammo_total += 2
                    #print("oops! ammo! adck:", cls.fttc_addcheck, "amck:", cls.fttc_ammocheck, "mag, tot, fir", ammo_magazine,ammo_total,ammo_fired)
                    cls.fttc_addcheck = 1
                    cls.fttc_ammocheck = ammo_fired
            else:
                if cls.fttc_ammocheck != ammo_fired:
                    cls.fttc_addcheck = 0

        return ammo_magazine, ammo_total

    #veist stinger - 3
    veist_check = 0

    @classmethod
    def VeistStingerClear(cls):
        cls.veist_check = 0

    @classmethod
    def VeistStinger(cls, ammo_fired, ammo_magazine, mag_cap):

        if ammo_fired != cls.veist_check:
            veist_proc = round(random.randrange(1,100), 5)
            cls.veist_check = ammo_fired
            if ammo_magazine == 0:
                veist_proc = 1
            if veist_proc >= 90:
                veist_bonus = math.floor(mag_cap * 0.25)
                ammo_magazine += veist_bonus

        return ammo_magazine
    
    #firing line - 10

    @classmethod
    def FiringLine(cls, dmg_output):
        dmg_output *= 1.2
        return dmg_output


    #bait n switch - 15
    bns_proc = 0
    bns_timer = 0
    ammo_fired_bns = 0

    @classmethod
    def BNSClear(cls):
        cls.bns_proc = 0
        cls.bns_timer = 0
        cls.ammo_fired_bns = 0

    @classmethod
    def BaitNSwitch(cls, ammo_fired, dmg_output, time_elapsed):

        if cls.bns_proc == 0:
            if (ammo_fired - cls.ammo_fired_bns) >= 1:
                dmg_output *= 1.35
                cls.bns_proc = 1
                cls.bns_timer = time_elapsed
        elif cls.bns_proc == 1:
            if (time_elapsed - cls.bns_timer) <= 10:
                dmg_output *= 1.35
            elif (time_elapsed - cls.bns_timer) > 10:
                cls.bns_proc = 0
                cls.ammo_fired_bns = ammo_fired
        
        return dmg_output

                # NOTE could add a bns_proc = 2 segment for handling lockouts if i ever figure out how that might work

# triple tap + firing line + veist (taipan)
taipan = {
    'name': 'taipan',
    'fire_rate': 120,
    'reload_time': 1.43,
    'damage_per_shot': 50000,
    'mag_cap': 5,
    'ammo_total': 21,
    'delay_first_shot': True,
    'perk_indices': [1,3,10]
}
create_weapon(taipan)

# fttc + bns (cataclysmic)
cataclysmic = {
    'name': 'cataclysmic',
    'fire_rate': 120,
    'reload_time': 1.43,
    'damage_per_shot': 50000,
    'mag_cap': 6,
    'ammo_total': 20,
    'delay_first_shot': True,
    'perk_indices': [2, 15]
}
create_weapon(cataclysmic)

# stormchaser ? (i am cheating since burst lfrs use 1 bullet for 3 rather than 3 for 3 so this is wacky :/)
stormchaser = {
    'name': 'stormchaser',
    'fire_rate': 120,
    'reload_time': 1.43,
    'damage_per_shot': 20000,
    'mag_cap': 15,
    'ammo_total': 63,
    'delay_first_shot': True,
    'burst_weapon': True,
    'burst_bullets': 3,
    'perk_indices': [10]
}
create_weapon(stormchaser)

#debug
# create_weapon("1.1", 120, 1.43, 50000, 6, 20, True, False, 0, 1, 1.84, [2,15], [1])
# create_weapon("1.2", 120, 1.43, 50000, 6, 20, True, False, 0, 1, 1.84, [2,15], [1])
# create_weapon("2.1", 120, 1.43, 50000, 6, 20, True, False, 0, 2, 1.84, [2,15], [1])
# create_weapon("2.2", 120, 1.43, 50000, 6, 20, True, False, 0, 2, 1.84, [2,15], [1])
# create_weapon("3.1", 120, 1.43, 50000, 6, 20, True, False, 0, 3, 1.84, [2,15], [1])
# create_weapon("3.2", 120, 1.43, 50000, 6, 20, True, False, 0, 3, 1.84, [2,15], [1])

#calculate damage function
Damage.DamageCalculate()

#keeping this for reference of how to call weapon instances i guess but idk
#Damage(the).print_weapon_instance()