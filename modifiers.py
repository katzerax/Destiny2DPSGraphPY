import math
import random
#this will not include all perks and traits, as some can be accounted for more consistently using the pre-input variables
#(this includes some such as Field Prep, which modifies weapons' reserves on an inventory stat basis, as well as maxing weapon archetype reload speed)


#magazine + reload perks/traits
def TripleTap(shots_fired,shots_left_mag,shots_left_reserve,tt_delay,i_hate_this): #every three shots fired (and presumably hit), it gives one bullet into the mag for free (technically giving more reserves)
    if shots_fired != 0:
        if tt_delay == 0:
            if shots_fired % 3 == 0: #this would need to be checked after every shot to prevent reloads from happening too early
                shots_left_mag += 1
                shots_left_reserve += 1 #HAHAHAHAHA THIS SCALES INFINITELY AND FOR WHAT
                i_hate_this = shots_fired
                tt_delay = 1
                print("shots fired, magazine, reserve, and if delay is on", shots_fired, shots_left_mag, shots_left_reserve, tt_delay) #13000 SHOTS IN THE MAG?????????
        else:
            if i_hate_this != shots_fired:
                tt_delay = 0
                print("shots fired and compare value", shots_fired, i_hate_this) #i fixed it and this so fucking SUCKS!!!!!!!!!
    return shots_left_mag, shots_left_reserve, tt_delay, i_hate_this 

def FTTC(shots_fired,shots_left_mag,shots_left_reserve): #Fourth Times The Charm, Triple Tap but if it was FOUR and TWO bullets
    if shots_fired % 4 == 0:
        shots_left_mag += 2
        shots_left_reserve += 2
    return shots_left_mag, shots_left_reserve

def VeistStinger(shots_fired,shots_left_mag): #will need to get rough RNG estimate + dealing with timer lockout + new nerf
    print("OOPS")

def ClownCartridge():
    print("OOPS")

def Overflow(): #lol like stack
    print("OOPS")

def RapidHit():
    print("OOPS")

#damage perks
def VorpalWeapon(VorpalActive,shot_dmg_output): #check before damage calculations as it is always active, passive bonus
    if VorpalActive == 0:
        if VorpalWeapon == 1: #primary ammo
            shot_dmg_output = shot_dmg_output * 1.2
            VorpalActive = 1
        elif VorpalWeapon == 2: #special ammo
            shot_dmg_output = shot_dmg_output * 1.15
            VorpalActive = 1
        elif VorpalWeapon == 3: #heavy ammo
            shot_dmg_output = shot_dmg_output * 1.1
            VorpalActive = 1
    return shot_dmg_output

def FocusedFury(FFActive,shots_fired,magazine_capacity,damage_per_shot,time_elapsed,shot_dmg_output): #checks for whether it is active, then for whether it should activate, then the activation requirements before setting itself active, followed by a check on how to turn it back
    if FFActive == 0:
        if shots_fired == math.ceil(magazine_capacity/2): #activates when shots reach half the magazine
            shot_dmg_output = shot_dmg_output * 1.2
            FFActive = 1
    else:
        if time_elapsed % 10 == 0: #this time check logic needs to be looked at, probably use another variable to track when the timer would be up for the buff
            shot_dmg_output = damage_per_shot
            FFActive = 0
    return shot_dmg_output

def HighImpactReserves(shots_left_mag,magazine_capacity,damage_per_shot,shot_dmg_output): #scales damage from bonus 12.5% to a bonus 25% by the last bullet, starting at half mag
    if shots_left_mag < magazine_capacity/2:
        c = shots_left_mag / (magazine_capacity/2)
        #shot_dmg_output = damage_per_shot - commenting this out as there is a better way to universally reset this damage, but want to keep it around
        hir_scalar_dmg = c(shot_dmg_output * 1.125) + (1-c)(shot_dmg_output * 1.25) #as magazine gets emptier, it retains more of the 25% bonus than the 12.5%, although i think the final % may be higher as it will only reach 25% at 0 shots left.
        shot_dmg_output = hir_scalar_dmg #giving the bonus, could make it so the scalar only multiplies by 0.125, 0.25, and then just += the extra dmg to make this more usable with other bonuses
    return shot_dmg_output

def HIREnhanced(shots_left_mag,magazine_capacity,damage_per_shot,shot_dmg_output): #first of many enhanced perks because this game fucking sucks
    if shots_left_mag < magazine_capacity/(4/3):
        c = shots_left_mag / magazine_capacity/(4/3)
        #shot_dmg_output = damage_per_shot
        hir_scalar_dmg = c(shot_dmg_output * 1.125) + (1-c)(shot_dmg_output * 1.25)
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
