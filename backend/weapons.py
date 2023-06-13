import copy
import time
from origin_traits import ORIGIN_TRAITS_LIST
from perks import PERKS_LIST
from buffs import BUFFS_LIST, WEAPON_BOOSTS_LIST, DEBUFFS_LIST

# Weapon Superclass
class BaseWeapon:
    def __init__(self, name:str, enhance1:bool=False, enhance2:bool=False, perk_indices:list=[], buff_indices:dict={}, origin_trait:int=0):
        self.name = name

        self.perk_indices = perk_indices
        self.enhance1 = enhance1
        self.enhance2 = enhance2
        self.has_perks = True if self.perk_indices else False

        self.buff_indices = buff_indices
        self.has_buffs = True if self.buff_indices else False

        self.origin_trait = origin_trait
        self.has_orgin_trait = True if self.origin_trait else False
        
        self.cached_graph_data = None

    def gen_all_literals(self):
        if self.has_perks:
            self.perk_literals = self.gen_perk_literals()

        if self.has_buffs:
            self.buff_literals = self.gen_buff_literals()

        if self.has_orgin_trait:
            self.origin_literal = self.gen_origin_literals()

    def gen_perk_literals(self):
        fs = self.get_full_settings()
        enhance = [self.enhance1, self.enhance2]
        return [PERKS_LIST[perk_index][2](isenhanced=[enhance[idx]], **fs) for idx, perk_index in enumerate(self.perk_indices)]
    
    def gen_buff_literals(self):
        arr = []
        for k, v in self.buff_indices.items():
            match k:
                case 'deb':
                    arr.append(DEBUFFS_LIST[v[0]][2](isconstant=v[1]))
                case 'buff':
                    arr.append(BUFFS_LIST[v[0]][2](isconstant=v[1]))
                case 'wdmg':
                    arr.append(WEAPON_BOOSTS_LIST[v[0]][2](isconstant=v[1]))
        return arr
    
    def gen_origin_literals(self):
        return ORIGIN_TRAITS_LIST[self.origin_trait][2]()

    def get_pruned_settings(self):
        settings = self.get_full_settings()
        for key, value in settings.copy().items():
            if value == False or 0 or not bool(value):
                del settings[key]
        return settings
    
    def DamageCalculate(self):
        # Here we would modify to remove all of the burst weapon code
        # because we would redefine damagecalculate to tailor it to
        # burst weapons
        pass

# Sandbox-type weapons (current structure)
class SandboxWeapon(BaseWeapon):
    WEAPON_FLAG = 'SANDBOX'
    def __init__(self) -> None:
        super().__init__()
        # Old Weapon class init code here, should just be direct copy

    def get_full_settings(self):
        return {
            'name': self.name,
            'fire_rate': self.fire_rate,
            'reload_time': self.reload_time,
            'damage_per_shot': self.damage_per_shot,
            'mag_cap': self.mag_cap,
            'ammo_total': self.ammo_total,
            'ammo_type': self.ammo_type,
            'fusion_weapon': self.fusion_weapon,
            'burst_weapon': self.burst_weapon,
            'burst_bullets': self.burst_bullets,
            'perk_indices': self.perk_indices,
            'enhance1': self.enhance1,
            'enhance2': self.enhance2,
            'buff_indices': self.buff_indices,
            'origin_trait': self.origin_trait,
            'WEAPON_FLAG': self.WEAPON_FLAG
        }

    def DamageCalculate(self):
        pass

# Frame-type weapons (new structure)
class FramedWeapon(BaseWeapon):
    WEAPON_FLAG = 'FRAMED'
    def __init__(self, archetype:str, reload_stat:int, damage_per_shot:int, 
                 mag_cap:int, ammo_total:int, element:int, **settings):
        super().__init__(**settings)

        self.archetype = archetype
        self.element = element
        self.damage_per_shot = damage_per_shot
        self.mag_cap = mag_cap
        self.ammo_total = ammo_total
        self.reload_time = self.get_reload_speed(reload_stat, self.reload_upper, self.reload_middle, self.reload_lower)
        self.reload_stat = reload_stat

        self.gen_all_literals()
    
    def get_reload_speed(self, reload_stat, upper_scalar, mid_scalar, bot_scalar):
        return round((upper_scalar * (reload_stat ** 2) + mid_scalar * reload_stat + bot_scalar)/30, 2)
    
    def get_full_settings(self):
        return {
            'name': self.name,

            'weapon_type': self.weapon_type,
            'archetype': self.archetype,
            'element': self.element,

            'fire_rate': self.fire_rate,
            
            'reload_time': self.reload_time,
            'reload_stat': self.reload_stat,
            'reload_cap': self.reload_cap,

            'damage_per_shot': self.damage_per_shot,

            'mag_cap': self.mag_cap,
            'ammo_total': self.ammo_total,
            'ammo_type': self.ammo_type,
            
            'perk_indices': self.perk_indices,
            'enhance1': self.enhance1,
            'enhance2': self.enhance2,

            'buff_indices': self.buff_indices,

            'origin_trait': self.origin_trait,

            'WEAPON_FLAG': self.WEAPON_FLAG
        }

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

        perks = copy.deepcopy(self.perk_literals) if self.has_perks else None
        buffs = copy.deepcopy(self.buff_literals) if self.has_buffs else None
        origin_trait = copy.deepcopy(self.origin_literal) if self.has_orgin_trait else None

        # Graph config
        ticks = 4500
        x_increments = 0.01
        x = [round(i * x_increments, 5) for i in range(ticks)]
        round_coeff = len(str(x_increments).split(".")[1])
        t_dmg = []

        fire_delay = round( 60 / self.fire_rate, round_coeff )
        fire_timer = fire_delay if self.fusion_weapon else 0

        # Init defaults
        # Any given value in ti may be passed to or returned by a perk/buff/ot class
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
            # Reset damage
            ti['dmg_output'] = self.damage_per_shot

            # Perks
            if self.has_perks:
                # On each perk
                for perk in perks:
                    # If enabled
                    if perk.enabled:
                        # Run output
                        perk_output = perk.output(**ti)
                        # Replace old tick_info values for any new ones
                        for k, v in perk_output.items():
                            ti[k] = v

            # Buffs
            if self.has_buffs:
                for buff in buffs:
                    if buff.enabled:
                        buff_output = buff.output(**ti)
                        for k, v in buff_output.items():
                            ti[k] = v

            # Origin trait
            if self.has_orgin_trait:
                if origin_trait.enabled:
                    origin_output = origin_trait.output(**ti)
                    for k, v in origin_output.items():
                        ti[k] = v

            # Checks to make sure there is still ammo left
            if ti['ammo_total'] == 0:
                ti['total_dmg'] = ti['total_dmg']
            # Checks to see if weapon needs a reload
            elif ti['ammo_magazine'] == 0:
                fire_timer += ti['reload_time']
                fire_timer -= fire_delay if self.fusion_weapon else 0
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

        dps = [round(t_dmg[i] / x[i], round_coeff) for i in range(ticks) if not i == 0]
        dps.insert(0, 0)
        # Cache graph data
        self.cached_graph_data = (x, dps)
        # Logging
        if do_cmd_prints:
            realtime_elapsed = round(realtime_elapsed - time.time(), 2) * -1000
            print(f'Calculation for weapon: {self.name} took {realtime_elapsed} ms')

        return x, dps

#####################
## Kinetic Weapons ##
#####################

# Pulse Rifle
class PulseRifle(FramedWeapon):
    """Pulse Rifle"""
    weapon_type = 'Pulse Rifle'
    burst_weapon = True
    ammo_type = 1

    reload_upper = 0.0034304
    reload_middle = -0.924866
    reload_lower = 96.6938
    reload_cap = 0.9

    def __init__(self, fire_rate:int, burst_bullets:int=3, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate
        self.burst_bullets = burst_bullets

    def DamageCalculate(self):
        # Edited to ONLY have burst weapon code instead of both
        # we wouldnt have to do this unless the calculation for a specific
        # weapon type should require special alterations
        pass

# Scout Rifle
class ScoutRifle(FramedWeapon):
    """Scout Rifle"""
    weapon_type = 'Scout Rifle'
    ammo_type = 1

    reload_upper = 0.00381167
    reload_middle = -0.999196
    reload_lower = 103.15
    reload_cap = 0.93

    def __init__(self, fire_rate:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate

# Hand Cannon
class HandCannon(FramedWeapon):
    """Hand Cannon"""
    weapon_type = 'Hand Cannon'
    ammo_type = 1

    reload_upper = 0.00477848
    reload_middle = -1.30872
    reload_lower = 138.482
    reload_cap = 1.47

    def __init__(self, fire_rate:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate

# Submachine Gun
class SubmachineGun(FramedWeapon):
    """Submachine Gun"""
    weapon_type = 'Submachine Gun'
    ammo_type = 1

    reload_upper = 0.00225423
    reload_middle = -0.6829
    reload_lower = 85.4344
    reload_cap = 0.97

    def __init__(self, fire_rate:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate

# Auto Rifle
class AutoRifle(FramedWeapon):
    """Auto Rifle"""
    weapon_type = 'Auto Rifle'
    ammo_type = 1

    reload_upper = 0.00316922
    reload_middle = -0.870122
    reload_lower = 92.5862
    reload_cap = 0.867

    def __init__(self, fire_rate:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate

# Sidearm
class Sidearm(FramedWeapon):
    """Sidearm"""
    weapon_type = 'Sidearm'
    ammo_type = 1

    reload_upper = 0.000882635
    reload_middle = -0.432829
    reload_lower = 68.6402
    reload_cap = 0.73

    def __init__(self, fire_rate:int, burst_weapon:bool=False, burst_bullets:int=0, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate
        self.burst_weapon = burst_weapon
        self.burst_bullets = burst_bullets

####################
## Energy Weapons ##
####################

# Shotgun
class Shotgun(FramedWeapon):
    """Shotgun"""
    weapon_type = 'Shotgun'
    ammo_type = 2

    reload_upper = 0.00237208
    reload_middle = -0.519846
    reload_lower = 42.4795
    reload_cap = 0.17

    def __init__(self, fire_rate:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate
        self.reload_time = round(self.reload_time * self.mag_cap, 2)

        # NOTE damagecalculate would have to be redefined here to include single shell
        # reloads, but I think I have an easy workaround to this that makes sense
        # because redefining the whole thing seems a bit redundant
        #
        # aprox 40 seconds later:
        # how tf do we decide whether to reload x shells vs the whole mag im gonna
        # give myself a headache *for now* we can multiply reload_time by mag_cap to force
        # it to reload it all at once with the correct timing

# Sniper Rifle
class SniperRifle(FramedWeapon):
    """Sniper Rifle"""
    weapon_type = 'Sniper Rifle'
    ammo_type = 2

    reload_upper = 0.00249814
    reload_middle = -0.821771
    reload_lower = 123.12
    reload_cap = 1.73

    def __init__(self, fire_rate:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate

# Fusion Rifle
class FusionRifle(FramedWeapon):
    """Fusion Rifle"""
    weapon_type = 'Fusion Rifle'
    ammo_type = 2

    reload_upper = 0.00227882
    reload_middle = -0.705757
    reload_lower = 91.6868
    reload_cap = 1.07

    def __init__(self, charge_time:int, **settings):
        super().__init__(**settings)

        self.charge_time = charge_time
        self.fire_rate = round((1000 / charge_time) * 60, 0)

# Breach Grenade Launcher
class BreachGL(FramedWeapon):
    """Breach Grenade Launcher"""
    weapon_type = 'Breach Grenade Launcher'
    ammo_type = 2

    reload_upper = 0.00268222
    reload_middle = -0.775084
    reload_lower = 104.714
    reload_cap = 1.5

    def __init__(self, fire_rate:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate

# Trace Rifle
class TraceRifle(FramedWeapon):
    """Trace Rifle"""
    weapon_type = 'Trace Rifle'
    ammo_type = 2

    # NOTE the spreadsheet was apparently made before legendary traces
    # were a thing so idk what to do about this. Im just giving it
    # auto rifle scalars for now
    reload_upper = 0.00316922
    reload_middle = -0.870122
    reload_lower = 92.5862
    reload_cap = 0.87

    def __init__(self, fire_rate:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate

###################
## Power Weapons ##
###################

# Rocket Launcher
class RocketLauncher(FramedWeapon):
    """Rocket Launcher"""
    weapon_type = 'Rocket Launcher'
    ammo_type = 3

    reload_upper = 0.00385034
    reload_middle = -0.917237
    reload_lower = 131.542
    reload_cap = 2.1

    def __init__(self, fire_rate:int, blast_radius:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate
        self.blast_radius = blast_radius

# Grenade Launcher
class GrenadeLauncher(FramedWeapon):
    """Grenade Launcher"""
    weapon_type = 'Grenade Launcher'
    ammo_type = 3

    reload_upper = 0.00279716
    reload_middle = -0.885767
    reload_lower = 132.442
    reload_cap = 1.97

    def __init__(self, fire_rate:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate

# Linear Fusion Rifle
class LinearFusionRifle(FramedWeapon):
    """Linear Fusion Rifle"""
    weapon_type = 'Linear Fusion Rifle'
    ammo_type = 3

    reload_upper = 0.00217949
    reload_middle = -0.709871
    reload_lower = 93.0427
    reload_cap = 1.13

    def __init__(self, charge_time:int, burst_weapon:bool=False, burst_bullets:int=0, **settings):
        super().__init__(**settings)

        self.charge_time = charge_time
        self.fire_rate = round((1000 / charge_time) * 60, 0)
        self.burst_weapon = burst_weapon
        self.burst_bullets = burst_bullets

        # NOTE if aggressive frame make damagecalculate the burst version?
        # or see if we can find a more intuitive way to do aggressive lfrs

# Machine Gun
class MachineGun(FramedWeapon):
    """Machine Gun"""
    weapon_type = 'Machine Gun'
    ammo_type = 3

    reload_upper = 0.00335315
    reload_middle = -1.08646
    reload_lower = 194.189
    reload_cap = 1.4

    def __init__(self, fire_rate:int, **settings):
        super().__init__(**settings)

        self.fire_rate = fire_rate

FRAMES_LIST = {
    'Kinetic': {
        'Pulse Rifle': ( {
            'Aggressive Burst': {
                'burst_bullets': 4,
                'fire_rate': 450
            },
            'Adaptive Frame': {
                'fire_rate': 390
            },
            'High-Impact Frame': {
                'fire_rate': 340
            },
            'Rapid-Fire Frame': {
                'fire_rate': 540
            },
            'Lightweight Frame': {
                'fire_rate': 450
            }
        }, PulseRifle ),
        'Scout Rifle': ( {
            'Aggressive Frame': {
                'fire_rate': 120
            },
            'High-Impact Frame': {
                'fire_rate': 150
            },
            'Rapid-Fire Frame': {
                'fire_rate': 260
            },
            'Lightweight Frame': {
                'fire_rate': 200
            },
            'Precision Frame': {
                'fire_rate': 180
            }
        }, ScoutRifle ),
        'Hand Cannon': ( {
            'Aggressive Frame': {
                'fire_rate': 120
            },
            'Adaptive Frame': {
                'fire_rate': 140
            },
            'Precision Frame': {
                'fire_rate': 180
            }
        }, HandCannon ),
        'Submachine Gun': ( {
            'Aggressive Frame': {
                'fire_rate': 750
            },
            'Lightweight Frame': {
                'fire_rate': 900
            },
            'Precision Frame': {
                'fire_rate': 600
            }
        }, SubmachineGun ),
        'Auto Rifle': ( {
            'Adaptive Frame': {
                'fire_rate': 600
            },
            'High-Impact Frame': {
                'fire_rate': 360
            },
            'Rapid-Fire Frame': {
                'fire_rate': 720
            },
            'Precision Frame': {
                'fire_rate': 450
            }
        }, AutoRifle ),
        'Sidearm': ( {
            'Aggressive Burst': {
                'burst_weapon': True,
                'burst_bullets': 2,
                'fire_rate': 325
            },
            'Adaptive Burst': {
                'burst_weapon': True,
                'burst_bullets': 3,
                'fire_rate': 491
            },
            'Adaptive Frame': {
                'fire_rate': 300
            },
            'Lightweight Frame': {
                'fire_rate': 360
            },
            'Precision Frame': {
                'fire_rate': 260
            },
        }, Sidearm ),
        # bow
    },
    'Energy': {
        'Shotgun': ( {
            'Aggressive Frame': {
                'fire_rate': 55
            },
            'Precision Frame': {
                'fire_rate': 65
            },
            'Lightweight Frame': {
                'fire_rate': 80
            },
            'Pinpoint Slug Frame': {
                'fire_rate': 65
            },
        }, Shotgun ),
        'Sniper Rifle': ( {
            'Aggressive Frame': {
                'fire_rate': 72
            },
            'Adaptive Frame': {
                'fire_rate': 90
            },
            'Rapid-Fire Frame': {
                'fire_rate': 140
            }
        }, SniperRifle ),
        'Fusion Rifle': ( {
            'el_exclude': [0],
            'High-Impact Frame': {
                'charge_time': 960
            },
            'Rapid-Fire Frame': {
                'charge_time': 500
            },
            'Precision Frame': {
                'charge_time': 780
            }
        }, FusionRifle ),
        'Breach Grenade Launcher': ( {
            'Lightweight Frame': {
                'fire_rate': 90
            },
            'Wave Frame': {
                'fire_rate': 72
            },
            'Double Fire': {
                'fire_rate': 100
            }
        }, BreachGL ),
        'Trace Rifle': ( {
            'el_exclude': [0],
            'Adaptive Frame': {
                'fire_rate': 1000
            }
        }, TraceRifle )
        # glaive
    },
    'Power': {
        'Rocket Launcher': ( {
            'el_exclude': [0],
            'Aggressive Frame': {
                'fire_rate': 25
            },
            'Adaptive Frame': {
                'fire_rate': 20
            },
            'High-Impact Frame': {
                'fire_rate': 15
            },
            'Precision Frame': {
                'fire_rate': 15
            }
        }, RocketLauncher ),
        'Grenade Launcher': ( {
            'el_exclude': [0],
            'Adaptive Frame': {
                'fire_rate': 120
            },
            'Rapid-Fire Frame': {
                'fire_rate': 150
            }
        }, GrenadeLauncher ),
        'Linear Fusion Rifle': ( {
            'el_exclude': [0],
            'Aggressive Frame': {
                'burst_weapon': True,
                'burst_bullets': 3,
                'charge_time': 533
            },
            'Precision Frame': {
                'charge_time': 533
            }
        }, LinearFusionRifle ),
        'Machine Gun': ( {
            'el_exclude': [0],
            'Adaptive Frame': {
                'fire_rate': 450
            },
            'High-Impact Frame': {
                'fire_rate': 360
            },
            'Rapid-Fire Frame': {
                'fire_rate': 900
            }
        }, MachineGun ),
        # sword
    }
}

ELEMENTS_LIST = [
    'Kinetic',
    'Strand',
    'Stasis',
    'Arc',
    'Solar',
    'Void'
]

def set_do_dmg_prints(value:bool):
    global do_cmd_prints 
    do_cmd_prints = value