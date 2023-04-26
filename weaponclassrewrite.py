import stat
import math
import random


PERKS = {
    1: "Triple Tap: Landing 3 precision hits refunds 1 ammo back to the magazine for free.",
    2: "Fourth Times the Charm: Landing 4 precision hits refunds 2 ammo back to the magazine for free.",
    3: "Perk 3 Description",
    4: "Perk 4 Description",
}

BUFFS = {
    1: "Well of Radiance: Super that gives healing and damage bonus in an area."
}

class Weapon:
    
    weapon_list = []

    def __init__(self, name, fire_rate, reload_time, damage_per_shot, mag_cap, ammo_total, delay_first_shot, perk_indices=None, buff_indices=None):
        self.name = name
        self.fire_rate = fire_rate
        self.reload_time = reload_time
        self.damage_per_shot = damage_per_shot
        self.mag_cap = mag_cap
        self.ammo_total = ammo_total

        self.delay_first_shot = delay_first_shot

        if perk_indices is None:
            self.perk_indices = []
        else:
            self.perk_indices = perk_indices

        if buff_indices is None:
            self.buff_indices = []
        else:
            self.buff_indices = buff_indices

    # adds a weapon to a list
    def add_weapon(self, name, fire_rate, reload_time, damage_per_shot, mag_cap, ammo_total, delay_first_shot, perk_indices, buff_indices):
        value = Weapon(name, fire_rate, reload_time, damage_per_shot, mag_cap, ammo_total, delay_first_shot, perk_indices, buff_indices)
        value = self.add_to_list(value)

    @classmethod
    def add_to_list(cls, value): # adds the weapon to the list itself within the class
        cls.weapon_list.append(value)

    @classmethod
    def get_list(cls): # for finding the listed objects
        return cls.weapon_list

    def add_perk(self, perk_index):
        if perk_index not in self.perk_indices and perk_index in PERKS:
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
        return PERKS.get(perk_index)
    
    #getting the individual attributes
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
    

class Damage:
    def __init__(self, weapon_instance):
        self.weapon_instance = weapon_instance

    def print_weapon_instance(self):
        print(self.weapon_instance.get_perks())


    #graph stuff
    ticks = 45000
    x_increments = 0.01
    x = []
    for i in range(ticks):
        x.append(round(i * x_increments, 5))
    
    round_coeff = len(str(x_increments).split(".")[1])

    @classmethod
    def DamageCalculate(cls):
        for z in range(len(Weapon.get_list())):
            
            t_dmg = []
            time_elapsed = 0
            total_damage = 0
            ammo_fired = 0

            delay_first_shot = Weapon.weapon_list[z].get_dfs()

            fire_stale = Weapon.weapon_list[z].get_fire_rate()
            fire_delay = round(60/fire_stale, cls.round_coeff)
            fire_timer = fire_delay if delay_first_shot else 0
            reload_time = Weapon.weapon_list[z].get_reload_time()

            mag_cap = Weapon.weapon_list[z].get_mag_cap()
            ammo_magazine = mag_cap

            ammo_total = Weapon.weapon_list[z].get_ammo_total()

            damage_per_shot = Weapon.weapon_list[z].get_damage_per_shot()
            dmg_output = damage_per_shot

            number_to_flag = {1: "TT_On", 2: "FTTC_On", 3: "VS_On", 10: "FL_On", 15: "BNS_On"}

            applied_perks = Weapon.weapon_list[z].get_perks()

            flags = {"TT_On": False, "FTTC_On": False, "VS_On": False, "FL_On": False, "BNS_On": False} 

            stale_val = 0

            for number in applied_perks:
                if number in number_to_flag:
                    flags[number_to_flag[number]] = True

            for i in range(cls.ticks):

                dmg_output = damage_per_shot

                if flags["TT_On"]: #1
                    ammo_magazine, ammo_total, ammo_fired = Damage.TripleTap(ammo_magazine, ammo_total, ammo_fired)
                if flags["FTTC_On"]: #2
                    ammo_magazine, ammo_total, ammo_fired = Damage.FourthTimesTheCharm(ammo_magazine, ammo_total, ammo_fired)
                if flags["VS_On"]: #3
                    ammo_magazine = Damage.VeistStinger(ammo_fired, ammo_magazine, mag_cap)
                if flags["FL_On"]: #10
                    dmg_output = Damage.FiringLine(dmg_output)
                if flags["BNS_On"]: #15
                    dmg_output = Damage.BaitNSwitch(ammo_fired, dmg_output, time_elapsed)

                if ammo_total == 0:
                    total_damage = total_damage
                elif ammo_magazine == 0:
                    fire_timer += reload_time
                    fire_timer -= fire_delay if delay_first_shot == True else 0
                    fire_timer = round(fire_timer, cls.round_coeff)
                    ammo_fired = 0
                    ammo_magazine = mag_cap
                elif time_elapsed == fire_timer:
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
                        print("name:", Weapon.weapon_list[z].get_name(), "| damage at", (i/100) ,"seconds:", t_dmg[i], "| dps:[",round(t_dmg[i]/(i/100), 1),"]","| per shot:<", dmg_output, ">")
                        stale_val = t_dmg[i]

            
            dps = [0]
            for i in range(cls.ticks):
                if i != 0:
                    dps.append(t_dmg[i] / cls.x[i])
            
            
            #print("name:", Weapon.weapon_list[z].get_name(), "| dps at 10 seconds:", dps[999])
            #print("name:", Weapon.weapon_list[z].get_name(), "| dps at 13 seconds:", dps[1299])
            #print("name:", Weapon.weapon_list[z].get_name(), "| dps at 20 seconds:", dps[1999])


    #triple tap - 1
    tt_addcheck = 0
    tt_ammocheck = 0

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

        return ammo_magazine, ammo_total, ammo_fired
    
    #fourth times the charm - 2
    fttc_addcheck = 0
    fttc_ammocheck = 0

    @classmethod
    def FourthTimesTheCharm(cls, ammo_magazine, ammo_total, ammo_fired):

        if ammo_fired != 0:
            if cls.fttc_addcheck == 0:
                if ammo_fired % 4 == 0:
                    ammo_magazine += 2
                    ammo_total += 2
                    cls.fttc_addcheck = 1
                    cls.fttc_ammocheck = ammo_fired
            else:
                if cls.fttc_ammocheck != ammo_fired:
                    cls.tt_addcheck = 0

        return ammo_magazine, ammo_total, ammo_fired

    #veist stinger - 3
    veist_check = 0

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

                #could add a bns_proc = 2 segment for handling lockouts if i ever figure out how that might work


#triple tap + firing line + veist (taipan)
the = Weapon("The", 120, 1.43, 50000, 5, 21, False, [1,3,10], [2])
the.add_weapon(the.name, the.fire_rate, the.reload_time, the.damage_per_shot, the.mag_cap, the.ammo_total, the.delay_first_shot, the.perk_indices, the.buff_indices)

#fttc + bns (cataclysmic)
piss = Weapon("Piss", 120, 1.43, 50000, 6, 20, True, [2,15], [1])
piss.add_weapon(piss.name, piss.fire_rate, piss.reload_time, piss.damage_per_shot, piss.mag_cap, piss.ammo_total, piss.delay_first_shot, piss.perk_indices, the.buff_indices)


#calculate damage function
Damage.DamageCalculate()

#keeping this for reference of how to call weapon instances i guess but idk
#Damage(the).print_weapon_instance()