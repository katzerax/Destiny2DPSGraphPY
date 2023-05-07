from operator import itemgetter
from perks import *
from buffs import *

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
                 enhance1:bool=False, enhance2:bool=False, fusion_weapon:bool=False, burst_weapon:bool=False, 
                 burst_bullets:int=0, swap_group:int=0, swap_time:float=0, perk_indices:list=[], buff_indices:list=[]):
        # Set positional args
        self.name = name
        self.fire_rate = fire_rate
        self.reload_time = reload_time
        self.damage_per_shot = damage_per_shot
        self.mag_cap = mag_cap
        self.ammo_total = ammo_total

        self.enhance1 = enhance1
        self.enhance2 = enhance2

        # Set variadic args
        # Still will need to figure which type is what, but figuring 1 - Kinetic, 2 - Solar, 3 - Arc, etc..
        self.ammo_type = ammo_type
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

        if fusion_weapon is None:
            self.fusion_weapon = 0
        else:
            self.fusion_weapon = fusion_weapon

        self.perk_indices = perk_indices
        self.has_perks = True if self.perk_indices else False
        self.buff_indices = buff_indices

        if self.has_perks:
            self.perk_literals = self.gen_perk_literals()

    def gen_perk_literals(self):
        fs = self.get_full_settings()
        enhance = [self.enhance1, self.enhance2]
        return [PERKS_LIST[perk_index][2](isenhanced=[enhance[idx]], **fs) for idx, perk_index in enumerate(self.perk_indices)]

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
            'fusion_weapon': self.fusion_weapon,
            'burst_weapon': self.burst_weapon,
            'burst_bullets': self.burst_bullets,
            'perk_indices': self.perk_indices,
            'enhance1': self.enhance1,
            'enhance2': self.enhance2,
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
        self.weapon = weapon_instance

        # Graph config
        self.ticks = 4500
        self.x_increments = 0.01
        self.x = [round(i * self.x_increments, 5) for i in range(self.ticks)]
        self.round_coeff = len(str(self.x_increments).split(".")[1])

    def print_weapon_instance(self):
        print(self.weapon_instance.get_perks())

    def DamageCalculate(self):
        # General Variables
        weapon = self.weapon

        # Damage variables
        t_dmg = []
        time_elapsed = 0
        total_damage = 0

        # Fired Variables
        ammo_fired = 0
        burst_shot = 0

        if not weapon.burst_weapon:
            fire_delay = round(60/weapon.fire_rate, self.round_coeff)
        else:
            #this rate of fire calculation may need some looking at :P, but basically it takes a rate of fire and then
            #just cuts it in half, half to shoot in a burst, the other to pause between shots..
            #for delay first shot, might just have it be equal to the normal fire delay? who knows. <--- this is what i did
            #5 minutes later rox here: i made DFS burst weapons have to complete a full charge sequence despite '120 RPM' not actually meaning 120 rpm... it just means 500ms charge time (since 500ms = 2 shots/second = 120rpm? idfk)
            burst_bullets = weapon.burst_bullets
            fire_delay = round((60/weapon.fire_rate)/2, self.round_coeff)
            burst_delay = round(((60/weapon.fire_rate)/2)/burst_bullets, self.round_coeff)

        fusion_delay = round(60/weapon.fire_rate, self.round_coeff)
        fire_timer = fusion_delay if weapon.fusion_weapon else 0

        # Reload
        reload_time = weapon.reload_time

        # Base Damage
        dmg_output = weapon.damage_per_shot

        #   Ammunition
        # Mag size
        mag_cap = weapon.mag_cap
        # Current mag
        ammo_magazine = weapon.mag_cap
        # All ammo
        ammo_total = weapon.ammo_total
        # Ammo type
        ammo_type = weapon.ammo_type
        
        # Start main sim loop
        for i in range(self.ticks):

            # Perks
            if weapon.has_perks:
                # On each perk
                for perk in weapon.perk_literals:
                    # If enabled
                    if perk.enabled:
                        # Gather tick info
                        tick_info = {
                            'ammo_magazine': ammo_magazine,
                            'ammo_total': ammo_total,
                            'ammo_type': ammo_type,
                            'ammo_fired': ammo_fired,
                            'mag_cap': mag_cap,
                            'reload_time': reload_time,
                            'time_elapsed': time_elapsed,
                            'dmg_output': dmg_output,
                            'total_dmg': total_damage,
                            'round_coeff': self.round_coeff,
                        }
                        # Run perk output
                        perk_output = perk.output(**tick_info)
                        # Replace old tick_info values for any new ones sent from perk
                        for key, value in perk_output.items():
                            tick_info[key] = value
                            
                        # Set variables to new info
                        # NOTE This is to conserve compute as for now, this will only replace possible
                        # outputs from any given perk. If a perk wanted to change the mag_cap for example,
                        # We would need to add it here to this list. I have some ideas on how this could
                        # be made better for the future
                        ammo_magazine, ammo_total, dmg_output, reload_time\
                             = (tick_info[k] for k in ('ammo_magazine','ammo_total', 'dmg_output', 'reload_time'))

            # Standard Weapon
            if not weapon.burst_weapon:
                # Checks to make sure there is still ammo left
                if ammo_total == 0:
                    total_damage = total_damage
                # Checks to see if weapon needs a reload
                elif ammo_magazine == 0:
                    fire_timer += reload_time
                    fire_timer -= fire_delay if weapon.fusion_weapon == True else 0
                    fire_timer = round(fire_timer, self.round_coeff)
                    ammo_fired = 0
                    ammo_magazine = mag_cap
                # Checks to fire
                elif time_elapsed >= fire_timer:
                    total_damage += dmg_output
                    fire_timer += fire_delay
                    fire_timer = round(fire_timer, self.round_coeff)
                    ammo_fired += 1
                    ammo_magazine -= 1
                    ammo_total -= 1

                # Increments time value and appends total damage to a list to calculate over the index points later                        
                time_elapsed += self.x_increments
                time_elapsed = round(time_elapsed, 5)
                t_dmg.append(total_damage)
                if stale_val != t_dmg[i]:
                    if i != 0:
                        print("name:", weapon.name, "| damage at", (i/100) ,"seconds:", t_dmg[i], "| dps:[",round(t_dmg[i]/(i/100), 1),"]","| per shot:<", dmg_output, ">")
                        stale_val = t_dmg[i]

            # Burst type weapon
            elif weapon.burst_weapon:

                if ammo_total == 0:
                    total_damage = total_damage

                elif ammo_magazine == 0:
                    fire_timer += reload_time
                    fire_timer -= fire_delay if weapon.fusion_weapon else 0
                    fire_timer = round(fire_timer, self.round_coeff)
                    # Rox: I want to test how things function without this 'ammo_fired' reset, as it may prove to be more beneficial to track specific needs within specific perks
                    #ammo_fired = 0
                    ammo_magazine = mag_cap

                elif time_elapsed >= fire_timer:
                    # Checks to ensure that weapon is still within burst timing/bullet ammount
                    if burst_shot >= 0 and burst_shot < burst_bullets:
                        fire_timer += burst_delay
                        fire_timer = round(fire_timer, self.round_coeff)
                        total_damage += dmg_output
                        burst_shot += 1
                        ammo_fired += 1
                        ammo_magazine -= 1
                        ammo_total -= 1
                    # Once weapon passes this, it gets the rest of the standard fire delay
                    elif burst_shot >= burst_bullets:
                        burst_shot = 0
                        fire_timer += (fusion_delay - burst_delay) if weapon.fusion_weapon else fire_delay
                        fire_timer = round(fire_timer, self.round_coeff)
            
                time_elapsed += self.x_increments
                time_elapsed = round(time_elapsed, 5)
                t_dmg.append(total_damage)
                if stale_val != t_dmg[i]:
                    if i != 0:
                        print("name:", weapon.name, "| damage at", (i/100) ,"seconds:", t_dmg[i], "| dps:[",round(t_dmg[i]/(i/100), 1),"]","| per shot:<", dmg_output, ">")
                        stale_val = t_dmg[i]

        dps = [t_dmg[i] / self.x[i] for i in range(self.ticks) if i != 0]
        return(dps)