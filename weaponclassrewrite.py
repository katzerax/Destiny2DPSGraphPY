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

    def __init__(self, name, fire_rate, reload_time, damage_per_shot, mag_cap, ammo_total, delay_first_shot, burst_weapon, burst_bullets, swap_group, swap_time, perk_indices=None, buff_indices=None):
        self.name = name
        self.fire_rate = fire_rate
        self.reload_time = reload_time
        self.damage_per_shot = damage_per_shot
        self.mag_cap = mag_cap
        self.ammo_total = ammo_total

        self.delay_first_shot = delay_first_shot
        self.burst_weapon = burst_weapon

        self.swap_group = swap_group
        self.swap_time = swap_time

        if burst_weapon == True:
            self.burst_bullets = burst_bullets
        else:
            self.burst_bullets = 1


        if perk_indices is None:
            self.perk_indices = []
        else:
            self.perk_indices = perk_indices

        if buff_indices is None:
            self.buff_indices = []
        else:
            self.buff_indices = buff_indices

        #figured this saves time as it just automatically adds a self to the list rather than make a new object every time or something yknow
        value = self
        value = self.add_to_list(value)

    # adds a weapon to a list
    #def add_weapon(self, name, fire_rate, reload_time, damage_per_shot, mag_cap, ammo_total, delay_first_shot, burst_weapon, burst_bullets, swap_group, swap_time, perk_indices, buff_indices):
        #value = Weapon(name, fire_rate, reload_time, damage_per_shot, mag_cap, ammo_total, delay_first_shot, burst_weapon, burst_bullets, swap_group, swap_time, perk_indices, buff_indices)
        #value = self.add_to_list(value)

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
            if Weapon.weapon_list[z].get_swap_group() == 0:
                t_dmg = []
                time_elapsed = 0
                total_damage = 0
                ammo_fired = 0
                burst_shot = 0

                delay_first_shot = Weapon.weapon_list[z].get_dfs()
                burst_weapon = Weapon.weapon_list[z].get_burst_variable()

                fire_stale = Weapon.weapon_list[z].get_fire_rate()

                if burst_weapon == False:
                    fire_delay = round(60/fire_stale, cls.round_coeff)

                #this rate of fire calculation may need some looking at :P, but basically it takes a rate of fire and then
                #just cuts it in half, half to shoot in a burst, the other to pause between shots..
                #for delay first shot, might just have it be equal to the normal fire delay? who knows.
                #5 minutes later roxy here: i made DFS burst weapons have to complete a full charge sequence despite '120 RPM' not actually meaning 120 rpm... it just means 500ms charge time (since 500ms = 2 shots/second = 120rpm? idfk)
                elif burst_weapon == True:
                    burst_bullets = Weapon.weapon_list[z].get_burst_bullets()
                    fire_delay = round((60/fire_stale)/2, cls.round_coeff)
                    burst_delay = round(((60/fire_stale)/2)/burst_bullets, cls.round_coeff)

                dfs_delay = round(60/fire_stale, cls.round_coeff)

                fire_timer = dfs_delay if delay_first_shot else 0
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


                    if burst_weapon == False:
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


                    elif burst_weapon == True:
                        if ammo_total == 0:
                            total_damage = total_damage
                        elif ammo_magazine == 0:
                            fire_timer += reload_time
                            fire_timer -= fire_delay if delay_first_shot == True else 0
                            fire_timer = round(fire_timer, cls.round_coeff)
                            ammo_fired = 0
                            ammo_magazine = mag_cap
                        elif time_elapsed == fire_timer:
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
                                print("name:", Weapon.weapon_list[z].get_name(), "| damage at", (i/100) ,"seconds:", t_dmg[i], "| dps:[",round(t_dmg[i]/(i/100), 1),"]","| per shot:<", dmg_output, ">")
                                stale_val = t_dmg[i]


                
                dps = [0]
                for i in range(cls.ticks):
                    if i != 0:
                        dps.append(t_dmg[i] / cls.x[i])
                
                
                #print("name:", Weapon.weapon_list[z].get_name(), "| dps at 10 seconds:", dps[999])
                #print("name:", Weapon.weapon_list[z].get_name(), "| dps at 13 seconds:", dps[1299])
                #print("name:", Weapon.weapon_list[z].get_name(), "| dps at 20 seconds:", dps[1999])


    #im going to cry myself to sleep trying to figure out what the hell this is going to do for me!!!
    #this can likely be integrated into the main function that just checks for whether swap_group = 0 or not
    
    swap_group1 = []
    swap_group2 = []
    swap_group3 = []
    swap_groups = [swap_group1, swap_group2, swap_group3]

    @classmethod
    def DamageCalculateMulti(cls):
        for z in range(len(Weapon.get_list())):
            if Weapon.weapon_list[z].get_swap_group() > 0:

                #could be expanded ig but i just wanna see if this even works

                if Weapon.weapon_list[z].get_swap_group() == 1:
                    cls.swap_group1.append(Weapon.weapon_list[z])

                if Weapon.weapon_list[z].get_swap_group() == 2:
                    cls.swap_group2.append(Weapon.weapon_list[z])

                if Weapon.weapon_list[z].get_swap_group() == 3:
                    cls.swap_group3.append(Weapon.weapon_list[z])

        for z in range(len(cls.swap_groups)):

            #'global' variables
            t_dmg = []
            time_elapsed = 0
            total_damage = 0
            stale_val = 0

            #weapon 1
            if len(cls.swap_groups[z]) >= 1 == True:
                ammo_fired1 = 0
                burst_shot1 = 0

                delay_first_shot1 = cls.swap_groups[z][0].get_dfs()
                burst_weapon1 = cls.swap_groups[z][0].get_burst_variable()
                fire_stale1 = cls.swap_groups[z][0].get_fire_rate()

                if burst_weapon1 == True:
                    burst_bullets1 = cls.swap_groups[z][0].get_burst_bullets()
                    fire_delay1 = round((60/fire_stale1)/2, cls.round_coeff)
                    burst_delay1 = round(((60/fire_stale1)/2)/burst_bullets1, cls.round_coeff)

                elif burst_weapon1 == False:
                    fire_delay1 = round(60/fire_stale1, cls.round_coeff)

                dfs_delay1 = round(60/fire_stale1, cls.round_coeff)
                fire_timer1 = dfs_delay1 if delay_first_shot1 else 0
                reload_time1 = cls.swap_groups[z][0].get_reload_time()
                swap_time1 = cls.swap_groups[z][0].get_swap_time()

                mag_cap1 = cls.swap_groups[z][0].get_mag_cap()
                ammo_magazine1 = mag_cap1

                ammo_total1 = cls.swap_groups[z][0].get_ammo_total()

                damage_per_shot1 = cls.swap_groups[z][0].get_damage_per_shot()
                dmg_output1 = damage_per_shot1

                applied_perks1 = cls.swap_groups[z][0].get_perks()
                number_to_flag1 = {1: "TT_On", 2: "FTTC_On", 3: "VS_On", 10: "FL_On", 15: "BNS_On"}
                flags1 = {"TT_On": False, "FTTC_On": False, "VS_On": False, "FL_On": False, "BNS_On": False}

                for number in applied_perks1:
                    if number in number_to_flag1:
                        flags1[number_to_flag1[number]] = True


            #weapon 2
            if len(cls.swap_groups[z]) >= 2 == True:
                ammo_fired2 = 0
                burst_shot2 = 0

                delay_first_shot2 = cls.swap_groups[z][1].get_dfs()
                burst_weapon2 = cls.swap_groups[z][1].get_burst_variable()
                fire_stale2 = cls.swap_groups[z][1].get_fire_rate()

                if burst_weapon2 == True:
                    burst_bullets2 = cls.swap_groups[z][1].get_burst_bullets()
                    fire_delay2 = round((60/fire_stale2)/2, cls.round_coeff)
                    burst_delay2 = round(((60/fire_stale2)/2)/burst_bullets2, cls.round_coeff)

                elif burst_weapon2 == False:
                    fire_delay2 = round(60/fire_stale2, cls.round_coeff)

                dfs_delay2 = round(60/fire_stale2, cls.round_coeff)
                fire_timer2 = dfs_delay2 if delay_first_shot2 else 0
                reload_time2 = cls.swap_groups[z][1].get_reload_time()
                swap_time2 = cls.swap_groups[z][1].get_swap_time()

                mag_cap2 = cls.swap_groups[z][1].get_mag_cap()
                ammo_magazine2 = mag_cap2

                ammo_total2 = cls.swap_groups[z][1].get_ammo_total()

                damage_per_shot2 = cls.swap_groups[z][1].get_damage_per_shot()
                dmg_output2 = damage_per_shot2

                applied_perks2 = cls.swap_groups[z][1].get_perks()
                number_to_flag2 = {1: "TT_On", 2: "FTTC_On", 3: "VS_On", 10: "FL_On", 15: "BNS_On"}
                flags2 = {"TT_On": False, "FTTC_On": False, "VS_On": False, "FL_On": False, "BNS_On": False}

                for number in applied_perks2:
                    if number in number_to_flag2:
                        flags2[number_to_flag2[number]] = True


            #weapon 3
            if len(cls.swap_groups[z]) >= 3 == True:
                ammo_fired3 = 0
                burst_shot3 = 0

                delay_first_shot3 = cls.swap_groups[z][2].get_dfs()
                burst_weapon3 = cls.swap_groups[z][2].get_burst_variable()
                fire_stale3 = cls.swap_groups[z][2].get_fire_rate()

                if burst_weapon3 == True:
                    burst_bullets3 = cls.swap_groups[z][2].get_burst_bullets()
                    fire_delay3 = round((60/fire_stale3)/2, cls.round_coeff)
                    burst_delay3 = round(((60/fire_stale3)/2)/burst_bullets3, cls.round_coeff)

                elif burst_weapon3 == False:
                    fire_delay3 = round(60/fire_stale3, cls.round_coeff)

                dfs_delay3 = round(60/fire_stale3, cls.round_coeff)
                fire_timer3 = dfs_delay3 if delay_first_shot3 else 0
                reload_time3 = cls.swap_groups[z][2].get_reload_time()
                swap_time3 = cls.swap_groups[z][2].get_swap_time()

                mag_cap3 = cls.swap_groups[z][2].get_mag_cap()
                ammo_magazine3 = mag_cap3

                ammo_total3 = cls.swap_groups[z][2].get_ammo_total()

                damage_per_shot3 = cls.swap_groups[z][2].get_damage_per_shot()
                dmg_output3 = damage_per_shot3

                applied_perks3 = cls.swap_groups[z][2].get_perks()
                number_to_flag3 = {1: "TT_On", 2: "FTTC_On", 3: "VS_On", 10: "FL_On", 15: "BNS_On"}
                flags3 = {"TT_On": False, "FTTC_On": False, "VS_On": False, "FL_On": False, "BNS_On": False}

                for number in applied_perks1:
                    if number in number_to_flag3:
                        flags3[number_to_flag3[number]] = True


            for i in range(cls.ticks):
                
                #dmg_output1 = damage_per_shot1
                #dmg_output2 = damage_per_shot2
                #dmg_output3 = damage_per_shot3

                #perks for weapon 1
                if flags1["TT_On"]:
                    ammo_magazine1, ammo_total1, ammo_fired1 = Damage.TripleTap(ammo_magazine1, ammo_total1, ammo_fired1)



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
the = Weapon("The", 120, 1.43, 50000, 5, 21, True, False, 0, 0, 1.5, [1,3,10], [2])
#the.add_weapon(the.name, the.fire_rate, the.reload_time, the.damage_per_shot, the.mag_cap, the.ammo_total, the.delay_first_shot, the.burst_weapon, the.burst_bullets, the.swap_group, the.swap_time, the.perk_indices, the.buff_indices)

#fttc + bns (cataclysmic)
piss = Weapon("Piss", 120, 1.43, 50000, 6, 20, True, False, 0, 0, 1.5, [2,15], [1])
#piss.add_weapon(piss.name, piss.fire_rate, piss.reload_time, piss.damage_per_shot, piss.mag_cap, piss.ammo_total, piss.delay_first_shot, piss.burst_weapon, piss.burst_bullets, piss.swap_group, piss.swap_time, piss.perk_indices, the.buff_indices)

#stormchaser ? (i am cheating since burst lfrs use 1 bullet for 3 rather than 3 for 3 so this is wacky :/)
storm = Weapon("storm", 120, 1.43, 20000, 15, 63, True, True, 3, 0, 1.5, [10], [1])
#storm.add_weapon(storm.name, storm.fire_rate, storm.reload_time, storm.damage_per_shot, storm.mag_cap, storm.ammo_total, storm.delay_first_shot, storm.burst_weapon, storm.burst_bullets, storm.swap_group, storm.swap_time, storm.perk_indices, storm.buff_indices)

#debug
gun1_group1 = Weapon("1.1", 120, 1.43, 50000, 6, 20, True, False, 0, 1, 1.84, [2,15], [1])
#gun1_group1.add_weapon(gun1_group1.name, gun1_group1.fire_rate, gun1_group1.reload_time, gun1_group1.damage_per_shot, gun1_group1.mag_cap, gun1_group1.ammo_total, gun1_group1.delay_first_shot, gun1_group1.swap_group, gun1_group1.swap_time, gun1_group1.perk_indices, gun1_group1.buff_indices)
gun2_group1 = Weapon("1.2", 120, 1.43, 50000, 6, 20, True, False, 0, 1, 1.84, [2,15], [1])
#gun2_group1.add_weapon(gun2_group1.name, gun2_group1.fire_rate, gun2_group1.reload_time, gun2_group1.damage_per_shot, gun2_group1.mag_cap, gun2_group1.ammo_total, gun2_group1.delay_first_shot, gun2_group1.swap_group, gun2_group1.swap_time, gun2_group1.perk_indices, gun2_group1.buff_indices)
gun1_group2 = Weapon("2.1", 120, 1.43, 50000, 6, 20, True, False, 0, 2, 1.84, [2,15], [1])
#gun1_group2.add_weapon(gun1_group2.name, gun1_group2.fire_rate, gun1_group2.reload_time, gun1_group2.damage_per_shot, gun1_group2.mag_cap, gun1_group2.ammo_total, gun1_group2.delay_first_shot, gun1_group2.swap_group, gun1_group2.swap_time, gun1_group2.perk_indices, gun1_group2.buff_indices)
gun2_group2 = Weapon("2.2", 120, 1.43, 50000, 6, 20, True, False, 0, 2, 1.84, [2,15], [1])
#gun2_group2.add_weapon(gun2_group2.name, gun2_group2.fire_rate, gun2_group2.reload_time, gun2_group2.damage_per_shot, gun2_group2.mag_cap, gun2_group2.ammo_total, gun2_group2.delay_first_shot, gun2_group2.swap_group, gun2_group2.swap_time, gun2_group2.perk_indices, gun2_group2.buff_indices)
gun1_group3 = Weapon("3.1", 120, 1.43, 50000, 6, 20, True, False, 0, 3, 1.84, [2,15], [1])
#gun1_group3.add_weapon(gun1_group3.name, gun1_group3.fire_rate, gun1_group3.reload_time, gun1_group3.damage_per_shot, gun1_group3.mag_cap, gun1_group3.ammo_total, gun1_group3.delay_first_shot, gun1_group3.swap_group, gun1_group3.swap_time, gun1_group3.perk_indices, gun1_group3.buff_indices)
gun2_group3 = Weapon("3.2", 120, 1.43, 50000, 6, 20, True, False, 0, 3, 1.84, [2,15], [1])
#gun2_group3.add_weapon(gun2_group3.name, gun2_group3.fire_rate, gun2_group3.reload_time, gun2_group3.damage_per_shot, gun2_group3.mag_cap, gun2_group3.ammo_total, gun2_group3.delay_first_shot, gun2_group3.swap_group, gun2_group3.swap_time, gun2_group3.perk_indices, gun2_group3.buff_indices)


#calculate damage function
Damage.DamageCalculate()

Damage.DamageCalculateMulti()

#keeping this for reference of how to call weapon instances i guess but idk
#Damage(the).print_weapon_instance()