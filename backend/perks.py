import stat
import math
import random

# Superclass
class Perk():
    def __init__(self, isenhanced:bool=False):
        self.enhanced = isenhanced
        self.enabled = True

# 1 - Triple Tap
class TripleTap(Perk):
    """Landing 3 precision hits refunds 1 ammo back to the magazine."""
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)
        self.tt_addcheck = 0
        self.tt_ammocheck = 0

    def output(self, ammo_magazine, ammo_total, ammo_fired, **_):
        if ammo_fired:
            if self.tt_addcheck == 0:
                if ammo_fired % 3 == 0:
                    ammo_magazine += 1
                    ammo_total += 1
                    self.tt_addcheck = 1
                    self.tt_ammocheck = ammo_fired
            else:
                if self.tt_ammocheck != ammo_fired:
                    self.tt_addcheck = 0

        return {'ammo_magazine': ammo_magazine, 'ammo_total': ammo_total}

# 2 - Fourth Times the Charm
class FourthTimesTheCharm(Perk):
    """Landing 4 precision hits refunds 2 ammo back to the magazine."""
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)
        self.fttc_addcheck = 0
        self.fttc_ammocheck = 0

    def output(self, ammo_magazine, ammo_total, ammo_fired, **_):
        if ammo_fired:
            if self.fttc_addcheck == 0:
                if ammo_fired % 4 == 0:
                    ammo_magazine += 2
                    ammo_total += 2
                    self.fttc_addcheck = 1
                    self.fttc_ammocheck = ammo_fired
            else:
                if self.fttc_ammocheck != ammo_fired:
                    self.fttc_addcheck = 0

        return {'ammo_magazine': ammo_magazine, 'ammo_total': ammo_total}
    
# 3 - Focused Fury
class FocusedFury(Perk):
    """Gain 20% increased damage for 12 seconds upon landing 50% of magazine as precision hits"""
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)
        self.ff_timecheck = 0
        self.ff_ammo = 0
        self.ff_active = 0

        if not isenhanced:
            self.ff_timer = 10
        elif isenhanced:
            self.ff_timer = 11
    
    def output(self, ammo_fired, mag_cap, dmg_output, time_elapsed, **_):

        if not self.ff_active:
            if (ammo_fired - self.ff_ammo) >= math.ceil(mag_cap/2):
                dmg_output *= 1.2
                self.ff_timecheck = time_elapsed
                self.ff_active = 1

        elif self.ff_active:
            if (time_elapsed - self.ff_timecheck) < self.ff_timer:
                dmg_output *= 1.2
            elif (time_elapsed - self.ff_timecheck) >= self.ff_timer:
                self.ff_active = 0
                self.ff_ammo = ammo_fired

        return {'dmg_output': dmg_output}

# 4 - Clown Cartridge
class ClownCartridge(Perk):
    """Randomly grants 10-50% increased mag capacity on reload."""
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)
        self.clown_coeff = 0

    def output(self, mag_cap, ammo_magazine, ammo_fired, total_dmg, **_):
        if not ammo_fired and total_dmg: # < --- could remove in order to 'prepare' clown cart for dps, if runs itself seven million times, just add an initial check
            self.clown_coeff = round(random.randrange(1,100))
            if self.clown_coeff <= 25:
                ammo_magazine = math.ceil(mag_cap * 1.1)
            elif self.clown_coeff <= 50:
                ammo_magazine = math.ceil(mag_cap * 1.2)
            elif self.clown_coeff <= 75:
                ammo_magazine = math.ceil(mag_cap * 1.3)
            elif self.clown_coeff >= 76:
                ammo_magazine = math.ceil(mag_cap * 1.45)

        return {'ammo_magazine': ammo_magazine}

# 5 - Overflow
class Overflow(Perk):
    """Upon picking up special or heavy ammo magazine gets overflowed to 200% of its regular capacity from reserves."""
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)
    
    def output(self, mag_cap, ammo_magazine, **_):

        if not self.overflow_check and not self.isenhanced:
            ammo_magazine = math.floor(mag_cap * 2)
            self.enabled = False

        elif not self.overflow_check and self.isenhanced:
            ammo_magazine = math.floor(mag_cap * 2.3)
            self.enabled = False

        return {'ammo_magazine': ammo_magazine}

# 6 - Rapid Hit
class RapidHit(Perk):
    """Gain 1 stack up to 5 for every precision hit. Scales at (5 | 30 | 35 | 42 | 60) reload speed for 2 seconds."""
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)
        self.rapid_hit_stacks = 0
        
    def output(self, ammo_fired, reload_time, round_coeff, **_):
        self.rapid_hit_stacks = math.floor(ammo_fired)
        match self.rapid_hit_stacks:
            case 0:
                return reload_time
            case 1:
                reload_time = round(reload_time * 0.99, round_coeff)
            case 2:
                reload_time = round(reload_time * 0.96, round_coeff)
            case 3:
                reload_time = round(reload_time * 0.95, round_coeff)
            case 4:
                reload_time = round(reload_time * 0.945, round_coeff)
            case 5 | _:
                reload_time = round(reload_time * 0.92, round_coeff)
        return {'reload_time': reload_time}

# 7 - Vorpal Weapon
class VorpalWeapon(Perk):
    """Flat damage increase of 10% to heavies, 15% to specials, and 20% to primaries."""
    def __init__(self, isenhanced:bool, ammo_type, **_):
        super().__init__(isenhanced)
        match ammo_type:
            case 1: # Primary Ammo
                self.scalar = 1.2
            case 2: # Special Ammo
                self.scalar = 1.15
            case 3: # Heavy Ammo
                self.scalar = 1.1

    def output(self, dmg_output, **_):
        dmg_output *= self.scalar
        return {'dmg_output': dmg_output}
    
# 8 - Target Lock
class TargetLock(Perk):
    """Landing hits within 0.2 seconds of each other grant a scaling damage buff up to 40%"""
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)
        if not isenhanced:
            self.bonus1 = 1.1673
            self.bonus2 = 1.4
        elif isenhanced:
            self.bonus1 = 1.1882
            self.bonus2 = 1.45
        
    def output(self, dmg_output, ammo_fired, mag_cap, **_):
        bonus_scalar = (ammo_fired / mag_cap) / 1.105
        if bonus_scalar >= (0.125 / 1.105) and bonus_scalar <= 1:
            dmg_output = ((1 - bonus_scalar) * (dmg_output * self.tl_bonus1)) + (bonus_scalar * (dmg_output * self.tl_bonus2))
        elif bonus_scalar > 1:
            dmg_output *= self.tl_bonus2
        return {'dmg_output': dmg_output}

# 9 - High Impact Reserves
class HighImpactReserves(Perk):
    """Linearly increases weapon damage from (12.1% - 25.6%) as magazine drops from 50% capacity to empty."""
    def __init__(self, isenhanced:bool, mag_cap, **_):
        super().__init__(isenhanced)
        if not isenhanced:
            self.hir_mag = (mag_cap/2)
        elif isenhanced:
            self.hir_mag = (mag_cap/(4/3))

    def output(self, ammo_magazine, dmg_output, **_):
        if ammo_magazine < self.hir_mag:
            scalar = ammo_magazine / self.hir_mag
            dmg_output = (scalar * (dmg_output * 1.125)) + ((1 - scalar) * (dmg_output * 1.255))
        return {'dmg_output': dmg_output}

# 10 - Firing Line
class FiringLine(Perk):
    """Gain 20% increased precision damage when within 15 meters of 2 or more allies."""
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)
        
    def output(self, dmg_output, **_):
        dmg_output *= 1.2
        return {'dmg_output': dmg_output}

# 11 - Explosive Light
class ExplosiveLight(Perk):
    """Nuts"""
    def __init__(self, isenhanced:bool, WEAPON_FLAG:str, weapon_type:str='', **_):
        super().__init__(isenhanced)
        self.shotcount = 6

        if WEAPON_FLAG == 'FRAMED':
            match weapon_type:
                case 'Grenade Launcher':
                    self.scalar = 1.42
                case 'Rocket Launcher' | _:
                    self.scalar = 1.25
        else:
            self.scalar = 1.25

    def output(self, dmg_output, **_):
        dmg_output *= self.scalar
        return {'dmg_output': dmg_output}

# 12 - Cascade Point
class CascadePoint(Perk):
    """Balls"""
    def __init__(self, isenhanced:bool, WEAPON_FLAG:str, weapon_type:str='', **_):
        super().__init__(isenhanced)
        self.timer = 2.5

        if WEAPON_FLAG == 'FRAMED':
            match weapon_type:
                case 'Machine Gun' | 'Submachine Gun':
                    self.scalar = 0.7
                case _:
                    self.scalar = 0.6
        else:
            self.scalar = 0.6

    def output(self, time_elapsed, fire_delay, **_):
        if time_elapsed <= self.timer:
            return {'fire_delay': fire_delay * self.scalar}
        else:
            self.enabled = False
            return {'fire_delay': fire_delay}

# 13 - Explosive Payload
class ExplosivePayload(Perk):
    # m: yamato is an idiot this scales off the precision multiplier of the gun lol
    """Flat 20% damage increase"""
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)

    def output(self, dmg_output, **_):
        dmg_output *= 1.2
        return {'dmg_output': dmg_output}

# 14 - Frenzy
class Frenzy(Perk):
    """20% damage increase while you have dealt or recieved damage in the last 5 seconds"""
    # m: we are just always going to assume being in combat but in fairness we could
    # absolutely code the 5 / 5.5 (enh) checks for toggling the perk, even if it would
    # never happen in actuality :P
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)

    def output(self, dmg_output, **_):
        dmg_output *= 1.2
        return {'dmg_output': dmg_output}

# 15 - Bait and Switch
class BaitNSwitch(Perk):
    """10 seconds of 35% increased damage upon dealing damage with all 3 weapons within 3 seconds."""
    def __init__(self, isenhanced:bool, **_):
        super().__init__(isenhanced)
        self.bns_proc = 0
        self.bns_timercheck = 0
        self.ammo_fired_bns = 0

        if not isenhanced:
            self.bns_timer = 10
        elif isenhanced:
            self.bns_timer = 11

    def output(self, ammo_fired, dmg_output, time_elapsed, **_):
        if self.bns_proc == 0:
            if (ammo_fired - self.ammo_fired_bns) >= 1:
                dmg_output *= 1.35
                self.bns_proc = 1
                self.bns_timercheck = time_elapsed

        elif self.bns_proc == 1:
            if (time_elapsed - self.bns_timercheck) <= self.bns_timer:
                dmg_output *= 1.35
            elif (time_elapsed - self.bns_timercheck) > self.bns_timer:
                self.bns_proc = 2
                self.ammo_fired_bns = ammo_fired

        elif self.bns_proc == 2:
            pass
        # NOTE I could easily add something else here to tie in how to re-proc, but to keep things real
        # For single weapon, it will only be proc'd once
        # Could add a bns_proc = 2 segment for handling lockouts if i ever figure out how that might work
        
        return {'dmg_output': dmg_output}

PERKS_LIST = {
    0: ('Null', 'No selection', None),
    1: ('Triple Tap', TripleTap.__doc__, TripleTap),
    2: ('Fourth Times the Charm', FourthTimesTheCharm.__doc__, FourthTimesTheCharm),
    3: ('Focused Fury', '', FocusedFury),
    4: ('Clown Cartridge', ClownCartridge.__doc__, ClownCartridge),
    5: ('Overflow', Overflow.__doc__, Overflow),
    6: ('Rapid Hit', RapidHit.__doc__, RapidHit),
    7: ('Vorpal Weapon', VorpalWeapon.__doc__, VorpalWeapon),
    8: ('Target Lock', TargetLock.__doc__, TargetLock),
    9: ('High Impact Reserves', HighImpactReserves.__doc__, HighImpactReserves),
    10: ('Firing Line', FiringLine.__doc__, FiringLine),
    11: ('Explosive Light', ExplosiveLight.__doc__, ExplosiveLight),
    12: ('Cascade Point', CascadePoint.__doc__, CascadePoint),
    13: ('Explosive Payload', ExplosivePayload.__doc__, ExplosivePayload),
    14: ('Frenzy', Frenzy.__doc__, Frenzy),
    15: ('Bait and Switch', BaitNSwitch.__doc__, BaitNSwitch),
}