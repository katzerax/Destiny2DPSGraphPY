import stat
import math
import random

PERKS_LIST = {
    0: ("Null", "No selection"),
    1: ("Triple Tap", "Landing 3 precision hits refunds 1 ammo back to the magazine."),
    2: ("Fourth Times the Charm", "Landing 4 precision hits refunds 2 ammo back to the magazine."),
    4: ('Clown Cartridge', 'Randomly grants 10-50%% increased mag capacity on reload.'),
    5: ('Overflow', 'Upon picking up special or heavy ammo magazine gets overflowed to 200%% of its regular capacity from reserves.'),
    6: ('Rapid Hit', 'Gain 1 stack up to 5 for every precision hit. Scales at 5 | 30 | 35 | 42 | 60 reload speed for 2 seconds.'),
    7: ("Vorpal Weapon", "Flat damage increase of 10% to heavies, 15% to specials, and 20% to primaries."),
    10: ("Firing Line", "Gain 20%% increased precision damage when within 15 meters of 2 or more allies."),
    15: ("Bait and Switch", "10 seconds of 35%% increased damage upon dealing damage with all 3 weapons within 3 seconds."),
}

BUFFS_LIST = {
    0: ("Null", "No selection"),
    1: ("Well of Radiance", "Super that gives healing and damage bonus in an area.")
}

weapons_list = {

}

def create_weapon(weapon_settings: dict):
    try:
        new_weapon = Weapon(**weapon_settings)
    except Exception as e:
        print(e)
        return False
    weapons_list[str(weapon_settings['name'])] = new_weapon
    return True

class Weapon:
    def __init__(self, name:str, fire_rate:float, reload_time:float, damage_per_shot:int, 
                 mag_cap:int, ammo_total:int, ammo_type:int=1, elemental_type:int=1, 
                 enhanced_perks:bool=False, delay_first_shot:bool=False, burst_weapon:bool=False, 
                 burst_bullets:int=0, swap_group:int=0, swap_time:float=0, perk_indices:list=[], buff_indices:list=[]):
        # Set positional args
        self.name = name
        self.fire_rate = fire_rate
        self.reload_time = reload_time
        self.damage_per_shot = damage_per_shot
        self.mag_cap = mag_cap
        self.ammo_total = ammo_total

        self.enhanced_perks = enhanced_perks

        # Set variadic args
            # These are validated inherintly by typing and defaulting in the constructor :)
        self.perk_indices = perk_indices
        self.buff_indices = buff_indices

        # For ammo_type this is specifically getting added for Vorpal, figured I would add on elemental damge too
        self.ammo_type = ammo_type
        # Still will need to figure which type is what, but figuring 1 - Kinetic, 2 - Solar, 3 - Arc, etc..
        self.elemental_type = elemental_type

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
    
    def get_ammo_type(self):
        return self.ammo_type
    
    def get_elemental_type(self):
        return self.elemental_type
    
    def get_enhanced_perks(self):
        return self.enhanced_perks
    
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
    
    def get_full_settings(self):
        return {
            'name': self.name,
            'fire_rate': self.fire_rate,
            'reload_time': self.reload_time,
            'damage_per_shot': self.damage_per_shot,
            'mag_cap': self.mag_cap,
            'ammo_total': self.ammo_total,
            'ammo_type': self.ammo_type,
            'elemental_type': self.elemental_type,
            'delay_first_shot': self.delay_first_shot,
            'burst_weapon': self.burst_weapon,
            'burst_bullets': self.burst_bullets,
            'perk_indices': self.perk_indices,
            'enhance1': self.enhanced_perks,
            'enhance2': self.enhanced_perks,
            'buff_indices': self.buff_indices,
        }
    
    def get_pruned_settings(self):
        settings = self.get_full_settings()
        for key, value in settings.copy().items():
            if value == False or 0 or not bool(value):
                del settings[key]
        return settings
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

                # General Variables
                t_dmg = []
                time_elapsed = 0
                total_damage = 0

                # Clearing relevant perk class functions for each new weapon
                Damage.TripleTapClear()
                Damage.FTTCClear()
                Damage.VeistStingerClear()
                Damage.BNSClear()

                # Fired Variables
                ammo_fired = 0
                burst_shot = 0

                # Boolean Values
                enhanced_perks = weapon.get_enhanced_perks()
                delay_first_shot = weapon.get_dfs()
                burst_weapon = weapon.get_burst_variable()

                # Fire Rate Calculations
                fire_stale = weapon.get_fire_rate()

                if not burst_weapon:
                    fire_delay = round(60/fire_stale, cls.round_coeff)

                #this rate of fire calculation may need some looking at :P, but basically it takes a rate of fire and then
                #just cuts it in half, half to shoot in a burst, the other to pause between shots..
                #for delay first shot, might just have it be equal to the normal fire delay? who knows. <--- this is what i did
                #5 minutes later rox here: i made DFS burst weapons have to complete a full charge sequence despite '120 RPM' not actually meaning 120 rpm... it just means 500ms charge time (since 500ms = 2 shots/second = 120rpm? idfk)
                elif burst_weapon:
                    burst_bullets = weapon.get_burst_bullets()
                    fire_delay = round((60/fire_stale)/2, cls.round_coeff)
                    burst_delay = round(((60/fire_stale)/2)/burst_bullets, cls.round_coeff)

                dfs_delay = round(60/fire_stale, cls.round_coeff)

                fire_timer = dfs_delay if delay_first_shot else 0
                reload_time = weapon.get_reload_time()

                # Ammunition
                mag_cap = weapon.get_mag_cap()
                ammo_magazine = mag_cap
                ammo_total = weapon.get_ammo_total()

                # Perks
                applied_perks = weapon.get_perks()
                number_to_flag = {1: "TT_On", 2: "FTTC_On", 3: "VS_On", 4: "CC_On", 5: "OF_On", 10: "FL_On", 15: "BNS_On"}
                flags = {"TT_On": False, "FTTC_On": False, "VS_On": False, "CC_On": False, "OF_On": False, "FL_On": False, "BNS_On": False} 

                # For print statement (stores last hit damage value to crosscheck when to print a new statement)
                stale_val = 0

                for number in applied_perks:
                    if number in number_to_flag:
                        flags[number_to_flag[number]] = True

                for i in range(cls.ticks):

                    # Resets damage so weapons don't do e+17 :)
                    dmg_output = weapon.get_damage_per_shot()

                    # Checks for active perks
                    if flags["TT_On"]: #1
                        ammo_magazine, ammo_total = Damage.TripleTap(ammo_magazine, ammo_total, ammo_fired)
                    if flags["FTTC_On"]: #2
                        ammo_magazine, ammo_total = Damage.FourthTimesTheCharm(ammo_magazine, ammo_total, ammo_fired)
                    if flags["VS_On"]: #3
                        ammo_magazine = Damage.VeistStinger(ammo_fired, ammo_magazine, mag_cap)
                    if flags["CC_On"]: #4
                        ammo_magazine = Damage.ClownCartridge(mag_cap, ammo_magazine, ammo_fired, total_damage)
                    if flags["OF_On"]: #5
                        ammo_magazine = Damage.Overflow(mag_cap, ammo_magazine, enhanced_perks)
                    if flags["FL_On"]: #10
                        dmg_output = Damage.FiringLine(dmg_output)
                    if flags["BNS_On"]: #15
                        dmg_output = Damage.BaitNSwitch(ammo_fired, dmg_output, time_elapsed, enhanced_perks)

                    # Standard Weapon
                    if not burst_weapon:
                        # Checks to make sure there is still ammo left
                        if ammo_total == 0:
                            total_damage = total_damage
                        # Checks to see if weapon needs a reload
                        elif ammo_magazine == 0:
                            fire_timer += reload_time
                            fire_timer -= fire_delay if delay_first_shot == True else 0
                            fire_timer = round(fire_timer, cls.round_coeff)
                            ammo_fired = 0
                            ammo_magazine = mag_cap
                        # Checks to fire
                        elif time_elapsed >= fire_timer:
                            total_damage += dmg_output
                            fire_timer += fire_delay
                            fire_timer = round(fire_timer, cls.round_coeff)
                            ammo_fired += 1
                            ammo_magazine -= 1
                            ammo_total -= 1

                        # Increments time value and appends total damage to a list to calculate over the index points later                        
                        time_elapsed += cls.x_increments
                        time_elapsed = round(time_elapsed, 5)
                        t_dmg.append(total_damage)
                        if stale_val != t_dmg[i]:
                            if i != 0:
                                print("name:", weapon.get_name(), "| damage at", (i/100) ,"seconds:", t_dmg[i], "| dps:[",round(t_dmg[i]/(i/100), 1),"]","| per shot:<", dmg_output, ">")
                                stale_val = t_dmg[i]

                    # Burst type weapon
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
                            # Checks to ensure that weapon is still within burst timing/bullet ammount
                            if burst_shot >= 0 and burst_shot < burst_bullets:
                                fire_timer += burst_delay
                                fire_timer = round(fire_timer, cls.round_coeff)
                                total_damage += dmg_output
                                burst_shot += 1
                                ammo_fired += 1
                                ammo_magazine -= 1
                                ammo_total -= 1
                            # Once weapon passes this, it gets the rest of the standard fire delay
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
    
    #clown cartridge - 4
    @classmethod
    def ClownCartridge(cls, mag_cap, ammo_magazine, ammo_fired, total_damage):
        
        if not ammo_fired and total_damage:
            ClownCoeff = round(random.randrange(1,100))
            if ClownCoeff <= 25:
                ammo_magazine = math.ceil(mag_cap * 1.1)
            elif ClownCoeff <= 50:
                ammo_magazine = math.ceil(mag_cap *1.2)
            elif ClownCoeff <= 75:
                ammo_magazine = math.ceil(mag_cap *1.3)
            elif ClownCoeff >= 76:
                ammo_magazine = math.ceil(mag_cap * 1.45)

        return ammo_magazine

    #overflow - 5
    overflow_check = 0

    @classmethod
    def Overflow(cls, mag_cap, ammo_magazine, enhanced_perks):

        if not cls.overflow_check and not enhanced_perks:
            ammo_magazine = math.floor(mag_cap * 2)
            cls.overflow_check = 1

        elif not cls.overflow_check and enhanced_perks:
            ammo_magazine = math.floor(mag_cap * 2.3)
            cls.overflow_check = 1

        return ammo_magazine
    
    #rapid hit - 6
    @classmethod
    def RapidHit(cls):
        pass

    #vorpal weapon - 7
    @classmethod
    def VorpalWeapon(cls):
        pass

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
    def BaitNSwitch(cls, ammo_fired, dmg_output, time_elapsed, enhanced_perks):

        if cls.bns_proc == 0:
            if (ammo_fired - cls.ammo_fired_bns) >= 1:
                dmg_output *= 1.35
                cls.bns_proc = 1
                cls.bns_timer = time_elapsed

        elif cls.bns_proc == 1 and not enhanced_perks:
            if (time_elapsed - cls.bns_timer) <= 10:
                dmg_output *= 1.35
            elif (time_elapsed - cls.bns_timer) > 10:
                cls.bns_proc = 2
                cls.ammo_fired_bns = ammo_fired

        elif cls.bns_proc == 1 and enhanced_perks:
            if (time_elapsed - cls.bns_timer) <= 11:
                dmg_output *= 1.35
            elif (time_elapsed - cls.bns_timer) > 11:
                cls.bns_proc = 2
                cls.ammo_fired_bns = ammo_fired

        elif cls.bns_proc == 2:
            pass
        # I could easily add something else here to tie in how to re-proc, but to keep things real
        # For single weapon, it will only be proc'd once
        
        return dmg_output

                # NOTE could add a bns_proc = 2 segment for handling lockouts if i ever figure out how that might work

# triple tap + firing line + veist (taipan)
# taipan = {
#     'name': 'taipan',
#     'fire_rate': 120,
#     'reload_time': 1.43,
#     'damage_per_shot': 50000,
#     'mag_cap': 5,
#     'ammo_total': 21,
#     'delay_first_shot': True,
#     'perk_indices': [1,3,10]
# }
# create_weapon(taipan)

# fttc + bns (cataclysmic)
cataclysmic_fttc = {
    'name': 'cataclysmic fttc',
    'fire_rate': 120,
    'reload_time': 1.43,
    'damage_per_shot': 50000,
    'mag_cap': 6,
    'ammo_total': 20,
    'delay_first_shot': True,
    'perk_indices': [2, 15]
}
create_weapon(cataclysmic_fttc)

cataclysmic_cc = {
    'name': 'cataclysmic cc',
    'fire_rate': 120,
    'reload_time': 1.43,
    'damage_per_shot': 50000,
    'mag_cap': 6,
    'ammo_total': 20,
    'delay_first_shot': True,
    'perk_indices': [4, 15],
}
create_weapon(cataclysmic_cc)

# stormchaser ? (i am cheating since burst lfrs use 1 bullet for 3 rather than 3 for 3 so this is wacky :/)
# stormchaser = {
#     'name': 'stormchaser',
#     'fire_rate': 120,
#     'reload_time': 1.43,
#     'damage_per_shot': 20000,
#     'mag_cap': 15,
#     'ammo_total': 63,
#     'delay_first_shot': True,
#     'burst_weapon': True,
#     'burst_bullets': 3,
#     'perk_indices': [10]
# }
# create_weapon(stormchaser)

#calculate damage function
Damage.DamageCalculate()