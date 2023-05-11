from backend.perks import *
from backend.buffs import *
import time
import copy

VERSION = 6

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

def delete_weapon(wep_name):
    if wep_name in weapons_list.keys():
        del weapons_list[wep_name]
        return True
    else:
        return False
    
class Weapon:
    def __init__(self, name:str, fire_rate:float, reload_time:float, damage_per_shot:int, 
                 mag_cap:int, ammo_total:int, ammo_type:int=1, elemental_type:int=1, 
                 enhance1:bool=False, enhance2:bool=False, fusion_weapon:bool=False, burst_weapon:bool=False, 
                 burst_bullets:int=0, perk_indices:list=[], buff_indices:list=[]):
        # Positional args
        self.name = name
        self.fire_rate = fire_rate
        self.reload_time = reload_time
        self.damage_per_shot = damage_per_shot
        self.mag_cap = mag_cap
        self.ammo_total = ammo_total
        self.backend_version = VERSION

        # Variadic args
        # Still will need to figure which type is what, but figuring 1 - Kinetic, 2 - Solar, 3 - Arc, etc..
        self.ammo_type = ammo_type
        self.elemental_type = elemental_type
        self.enhance1 = enhance1
        self.enhance2 = enhance2

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

        self.fusion_weapon = True if fusion_weapon else False

        self.perk_indices = perk_indices
        self.has_perks = True if self.perk_indices else False
        self.buff_indices = buff_indices

        if self.has_perks:
            self.perk_literals = self.gen_perk_literals()
        
        self.cached_graph_data = None

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
    
    def DamageCalculate(self):
        # Check for cached data
        if self.cached_graph_data:
            if do_cmd_prints:
                print(f'Found cached graph data for weapon: {self.name}')
            return self.cached_graph_data
        
        # Logging
        if do_cmd_prints:
            print(f'Starting damage calculation for weapon: {self.name}')
            stale_dmg = 0
            realtime_elapsed = time.time()

        # perk bug !!!
        perks = copy.deepcopy(self.perk_literals) if self.has_perks else None

        # Graph config
        ticks = 4500
        x_increments = 0.01
        x = [round(i * x_increments, 5) for i in range(ticks)]
        round_coeff = len(str(x_increments).split(".")[1])
    
        t_dmg = []

        if not self.burst_weapon:
            fire_delay = round(60/self.fire_rate, round_coeff)
        else:
            #this rate of fire calculation may need some looking at :P, but basically it takes a rate of fire and then
            #just cuts it in half, half to shoot in a burst, the other to pause between shots..
            #for delay first shot, might just have it be equal to the normal fire delay? who knows. <--- this is what i did
            #5 minutes later rox here: i made DFS burst weapons have to complete a full charge sequence despite '120 RPM' not actually meaning 120 rpm... it just means 500ms charge time (since 500ms = 2 shots/second = 120rpm? idfk)
            fire_delay = round((60/self.fire_rate)/2, round_coeff)
            burst_delay = round(((60/self.fire_rate)/2)/self.burst_bullets, round_coeff)

        fusion_delay = round(60/self.fire_rate, round_coeff)
        fire_timer = fusion_delay if self.fusion_weapon else 0

        # Init defaults
        # Any given value in ti may be passed to or returned by a perk class
        ti = {
            # Current mag
            'ammo_magazine': self.mag_cap,
            # All available ammo
            'ammo_total': self.ammo_total,
            # Heavy, special, kinetic
            'ammo_type': self.ammo_type,
            # Ammo expended
            'ammo_fired': 0,
            'burst_shot': 0,
            # Mag size
            'mag_cap': self.mag_cap,
            # Reload time
            'reload_time': self.reload_time,
            # Damage output
            'dmg_output': self.damage_per_shot,
            # Running totals
            'time_elapsed': 0,
            'total_dmg': 0,
            # Some perks require round coeff
            'round_coeff': round_coeff,
        }
        
        # Start main sim loop
        for tick in range(ticks):
            # No more e+17 pls!!!
            ti['dmg_output'] = self.damage_per_shot

            # Perks
            # NOTE Im sure I can do this in a nasty list comp but I really dont want to
            if self.has_perks:
                # On each perk
                for perk in perks:
                    # If enabled
                    if perk.enabled:
                        # Run perk output
                        perk_output = perk.output(**ti)
                        # Replace old tick_info values for any new ones sent from perk
                        for key, value in perk_output.items():
                            ti[key] = value

            # Standard Weapon
            if not self.burst_weapon:
                # Checks to make sure there is still ammo left
                if ti['ammo_total'] == 0:
                    ti['total_dmg'] = ti['total_dmg']
                # Checks to see if weapon needs a reload
                elif ti['ammo_magazine'] == 0:
                    fire_timer += ti['reload_time']
                    fire_timer -= fire_delay if self.fusion_weapon == True else 0
                    fire_timer = round(fire_timer, round_coeff)
                    ti['ammo_fired'] = 0
                    ti['ammo_magazine'] = ti['mag_cap']
                # Checks to fire
                elif ti['time_elapsed'] >= fire_timer:
                    ti['total_dmg'] += ti['dmg_output']
                    fire_timer += fire_delay
                    fire_timer = round(fire_timer, round_coeff)
                    ti['ammo_fired'] += 1
                    ti['ammo_magazine'] -= 1
                    ti['ammo_total'] -= 1

                # Increments time value and appends total damage to a list to calculate over the index points later                        
                ti['time_elapsed'] = round(ti['time_elapsed'] + x_increments, 5)
                t_dmg.append(ti['total_dmg'])
                # Logging
                if do_cmd_prints:
                    if stale_dmg != t_dmg[tick]:
                        if tick != 0:
                            print(f'Weapon: {self.name} | Damage at {tick/100} secs: {t_dmg[tick]} | DPS: [{round(t_dmg[tick]/(tick/100), 1)}] | Per Shot: <{ti["dmg_output"]}> ')
                            stale_dmg = t_dmg[tick]

            # Burst type weapon
            elif self.burst_weapon:
                # Checks to make sure there is still ammo left
                if ti['ammo_total'] == 0:
                    ti['total_dmg'] = ti['total_dmg']
                # Checks to see if weapon needs a reload
                elif ti['ammo_magazine'] == 0:
                    fire_timer += ti['reload_time']
                    fire_timer -= fire_delay if self.fusion_weapon else 0
                    fire_timer = round(fire_timer, round_coeff)
                    # Rox: I want to test how things function without this 'ammo_fired' reset, as it may prove to be more beneficial to track specific needs within specific perks
                    #ammo_fired = 0
                    ti['ammo_magazine'] = ti['mag_cap']

                elif ti['time_elapsed'] >= fire_timer:
                    # Checks to ensure that weapon is still within burst timing/bullet ammount
                    if ti['burst_shot'] >= 0 and ti['burst_shot'] < self.burst_bullets:
                        fire_timer += burst_delay
                        fire_timer = round(fire_timer, round_coeff)
                        ti['total_dmg'] += ti['dmg_output']
                        ti['burst_shot'] += 1
                        ti['ammo_fired'] += 1
                        ti['ammo_magazine'] -= 1
                        ti['ammo_total'] -= 1
                    # Once weapon passes this, it gets the rest of the standard fire delay
                    elif ti['burst_shot'] >= self.burst_bullets:
                        ti['burst_shot'] = 0
                        fire_timer += (fusion_delay - burst_delay) if self.fusion_weapon else fire_delay
                        fire_timer = round(fire_timer, round_coeff)
            
                ti['time_elapsed'] = round(ti['time_elapsed'] + x_increments, 5)
                t_dmg.append(ti['total_dmg'])
                # Logging
                if do_cmd_prints:
                    if stale_dmg != t_dmg[tick]:
                        if tick != 0:
                            print(f'Weapon: {self.name} | Damage at {tick/100} secs: {t_dmg[tick]} | DPS: [{round(t_dmg[tick]/(tick/100), 1)}] | Per Shot: < {ti["dmg_output"]} > ')
                            stale_dmg = t_dmg[tick]

        dps = [(t_dmg[i] / x[i]) for i in range(ticks) if not i == 0]
        # tick bug !!!
        dps.insert(0, 0)
        # Cache graph data
        self.cached_graph_data = (x, dps)
        # Logging
        if do_cmd_prints:
            realtime_elapsed = round(realtime_elapsed - time.time(), 2) * -1000
            print(f'Calculation for weapon: {self.name} took {realtime_elapsed} ms')

        return x, dps
    
def set_do_dmg_prints(value:bool):
    global do_cmd_prints 
    do_cmd_prints = value