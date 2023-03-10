import math
import random
#this will not include all perks and traits, as some can be accounted for more consistently using the pre-input variables
#(this includes some such as Field Prep, which modifies weapons' reserves on an inventory stat basis, as well as maxing weapon archetype reload speed)


#magazine + reload perks/traits
def TripleTap(shots_fired,shots_left_mag,shots_left_reserve,tt_delay,tt_delay_check): #every three shots fired (and presumably hit), it gives one bullet into the mag for free (technically giving more reserves)
    if shots_fired != 0:
        if tt_delay == 0:
            if shots_fired % 3 == 0: #this would need to be checked after every shot to prevent reloads from happening too early
                shots_left_mag += 1
                shots_left_reserve += 1
                tt_delay_check = shots_fired
                tt_delay = 1
        else:
            if tt_delay_check != shots_fired:
                tt_delay = 0 #this fix ensures that the shot count changes before doing the main check again
    return shots_left_mag, shots_left_reserve, tt_delay, tt_delay_check 

def FTTC(shots_fired,shots_left_mag,shots_left_reserve,fttc_delay,fttc_delay_check): #Fourth Times The Charm, Triple Tap but if it was FOUR and TWO bullets
    if shots_fired != 0:
        if fttc_delay ==0:
            if shots_fired % 4 == 0:
                shots_left_mag += 2
                shots_left_reserve += 2
                fttc_delay_check = shots_fired
                fttc_delay = 1
        else:
            if fttc_delay_check != shots_fired:
                fttc_delay = 0
    return shots_left_mag, shots_left_reserve, fttc_delay, fttc_delay_check

def VeistStinger(shots_fired, shots_left_mag,magazine_capacity, veist_overflow_cross, veist_check): #will need to get rough RNG estimate + dealing with timer lockout + new nerf
    if shots_fired != veist_check: #more or less working as intended, just need to make sure
        VeistProc = round(random.randrange(1,100), 5) 
        veist_check = shots_fired #that the capacity exceed check can get figured out at some point
        if shots_left_mag == 0: #so if there is no ammo left, it doesnt attempt to check
            VeistProc = 1
        if VeistProc >= 90: #10% chance right now, but may need to scale based on magazine size
            veist_bonus = math.floor(magazine_capacity * 0.25)
            shots_left_mag += veist_bonus
            if veist_overflow_cross != 1: #pointless check for now, until i implement better VS + OF and CC whatevers
                if shots_left_mag > magazine_capacity:
                    shots_left_mag = magazine_capacity
    return shots_left_mag, veist_check


def ClownCartridge(magazine_capacity, shots_left_mag, clown_check, reload_count):
    if clown_check != reload_count:
        clown_check = reload_count
        ClownCoeff = round(random.randrange(1,100))
        if ClownCoeff <= 25:
            shots_left_mag = math.ceil(magazine_capacity * 1.1)
        elif ClownCoeff <= 50:
            shots_left_mag = math.ceil(magazine_capacity *1.2)
        elif ClownCoeff <= 75:
            shots_left_mag = math.ceil(magazine_capacity *1.3)
        elif ClownCoeff >= 76:
            shots_left_mag = math.ceil(magazine_capacity * 1.45)
    return clown_check, shots_left_mag

def Overflow(shots_left_mag,of_check,delay_first_shot,veist_overflow_cross,magazine_capacity): #lol like stack
    if of_check == 0:
        if delay_first_shot:
            shots_left_mag = math.ceil(shots_left_mag * 2)
            of_check = 1
        else:
            shots_left_mag = math.ceil((shots_left_mag + 1) * 2) - 1
            of_check = 1
    #if of_check == 1:
        #if shots_left_mag <= magazine_capacity:
            #veist_overflow_cross = 1 #i hate exceptions... this is not working bc if veist procs too often anyways it does not matter
    return shots_left_mag, of_check, veist_overflow_cross #there is a way to fix this using shots_fired, or similar variable to track when OF should end.

def RapidHit(output_reload_time,rh_stacks,shots_fired,roundingcoeff):
    rh_stacks = math.floor(shots_fired)
    if rh_stacks >= 5:
        rh_stacks = 5
    if rh_stacks == 1:
        output_reload_time = round(output_reload_time / (1.1), roundingcoeff)
    elif rh_stacks == 2:
        output_reload_time = round(output_reload_time / (1.2), roundingcoeff)
    elif rh_stacks == 3:
        output_reload_time = round(output_reload_time / (1.3), roundingcoeff)
    elif rh_stacks == 4:
        output_reload_time = round(output_reload_time / (1.4), roundingcoeff)
    elif rh_stacks == 5:
        output_reload_time = round(output_reload_time / (1.5), roundingcoeff)
    return output_reload_time

#damage perks
def VorpalWeapon(weapon_class,shot_dmg_output): #check before damage calculations as it is always active, passive bonus
    if weapon_class == 1: #primary ammo
        shot_dmg_output = shot_dmg_output * 1.2
    elif weapon_class == 2: #special ammo
        shot_dmg_output = shot_dmg_output * 1.15
    elif weapon_class == 3: #heavy ammo
        shot_dmg_output = shot_dmg_output * 1.1
    return shot_dmg_output

def FocusedFury(FFActive,shots_fired_ff,magazine_capacity,time_elapsed,shot_dmg_output,ff_time_check): #checks for whether it is active, then for whether it should activate, then the activation requirements before setting itself active, followed by a check on how to turn it back
    if FFActive == 0:
        if shots_fired_ff == math.ceil(magazine_capacity/2): #activates when shots reach half the magazine
            shot_dmg_output = shot_dmg_output * 1.2
            FFActive = 1
            ff_time_check = time_elapsed
    else:
        shot_dmg_output = shot_dmg_output * 1.2
        if (time_elapsed - ff_time_check) >= 10: 
            shot_dmg_output = shot_dmg_output * (1/1.2)
            shots_fired_ff = 0
            FFActive = 0
    return shot_dmg_output, FFActive, ff_time_check, shots_fired_ff

def HighImpactReserves(shots_left_mag,magazine_capacity,shot_dmg_output): #scales damage from bonus 12.5% to a bonus 25% by the last bullet, starting at half mag
    if shots_left_mag < magazine_capacity/2:
        c = shots_left_mag / (magazine_capacity/2)
        hir_scalar_dmg = (c * (shot_dmg_output * 1.125)) + ((1 - c) * (shot_dmg_output * 1.25)) #as magazine gets emptier, it retains more of the 25% bonus than the 12.5%, although i think the final % may be higher as it will only reach 25% at 0 shots left.
        hir_bonus_dmg = hir_scalar_dmg - shot_dmg_output
        shot_dmg_output += hir_bonus_dmg #giving the bonus, could make it so the scalar only multiplies by 0.125, 0.25, and then just += the extra dmg to make this more usable with other bonuses
    return shot_dmg_output

def HIREnhanced(shots_left_mag,magazine_capacity,shot_dmg_output): #first of many enhanced perks because this game fucking sucks
    if shots_left_mag < magazine_capacity/(4/3):
        c = shots_left_mag / magazine_capacity/(4/3)
        hir_scalar_dmg = (c * (shot_dmg_output * 1.125)) + ((1 - c) * (shot_dmg_output * 1.25))
        hir_bonus_dmg = hir_scalar_dmg - shot_dmg_output #important that it is shot dmg output as it scales based off buffed dmg as is, not starting dmg
        shot_dmg_output += hir_bonus_dmg #alt. calculation i mentioned in an above comment
    return shot_dmg_output

def FiringLine(shot_dmg_output): #flat bonus 20%, for all cases, permanently, so easy
    shot_dmg_output = shot_dmg_output * 1.2
    return shot_dmg_output

def ExplosiveLight(shot_dmg_output): #explosives only but whatever
    print("OOPS")

def CascadePoint(fire_delay,roundingcoeff,fire_rate,cascade_fr):
    cascade_fr = fire_rate * 1.5
    fire_delay = round(60/cascade_fr, roundingcoeff)
    return fire_delay

def ExplosivePayload(shot_dmg_output): #similar to firing line hehe
    shot_dmg_output = shot_dmg_output * 1.14
    return shot_dmg_output

def Frenzy():
    print("OOPS")

def GHornBonus(): #rockets only but whatever
    print("OOPS")

#player buffs - armor mods will go here
def WellofRadiance():
    print("REMOVE ME LOL")
