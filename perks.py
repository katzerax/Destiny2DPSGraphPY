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

def VeistStinger(shots_fired,shots_left_mag): #will need to get rough RNG estimate + dealing with timer lockout + new nerf
    print("OOPS")

def ClownCartridge():
    print("OOPS")

def Overflow(shots_left_mag,of_check,delay_first_shot): #lol like stack
    if of_check == 0:
        if delay_first_shot:
            shots_left_mag = math.ceil(shots_left_mag * 2)
            of_check = 1
        else:
            shots_left_mag = math.ceil((shots_left_mag + 1) * 2) - 1
            of_check = 1
    return shots_left_mag, of_check

def RapidHit():
    print("OOPS")

#damage perks
def VorpalWeapon(weapon_class,shot_dmg_output): #check before damage calculations as it is always active, passive bonus
    if weapon_class == 1: #primary ammo
        shot_dmg_output = shot_dmg_output * 1.2
    elif weapon_class == 2: #special ammo
        shot_dmg_output = shot_dmg_output * 1.15
    elif weapon_class == 3: #heavy ammo
        shot_dmg_output = shot_dmg_output * 1.1
    return shot_dmg_output

def FocusedFury(FFActive,shots_fired_ff,magazine_capacity,damage_per_shot,time_elapsed,shot_dmg_output,ff_time_check): #checks for whether it is active, then for whether it should activate, then the activation requirements before setting itself active, followed by a check on how to turn it back
    if FFActive == 0:
        if shots_fired_ff == math.ceil(magazine_capacity/2): #activates when shots reach half the magazine
            shot_dmg_output = shot_dmg_output * 1.2
            FFActive = 1
            ff_time_check = time_elapsed
    else:
        shot_dmg_output = shot_dmg_output * 1.2
        if (time_elapsed - ff_time_check) >= 10: 
            shot_dmg_output = damage_per_shot
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

def ExplosiveLight(shot_dmg_output):
    print("OOPS")

def CascadePoint():
    print("OOPS")

def ExplosivePayload():
    print("OOPS")

def Frenzy():
    print("OOPS")

def GHornBonus(): #rockets only
    print("OOPS")

#player buffs - armor mods will go here
def WellofRadiance():
    print("REMOVE ME LOL")
