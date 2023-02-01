def TripleTap(totalDamage):
    print(totalDamage)

def FTTC(totalDamage):
    print(totalDamage)

    #i have no idea how the fuck this works so im just gonna start writing things from my
    #notebook into this python and surely it will get figured out
    #surely

#magazine modifers
TripleTap:
    if shots_fired % 3 = 0:
        shots_left_mag += 1
        shots_left_reserve += 1
    #this would need to be checked after every shot to prevent reloads from happening too early

FTTC: #Fourth Times The Charm
    if shots_fired % 4 = 0:
        shots_left_mag += 2
        shots_left_reserve += 2
    #TT but if it was 4 and 2

#damage modifiers
VorpalWeapon: #check before damage calculations as it is always active, passive bonus
    if VorpalActive = 0:
        if VorpalWeapon = 1: #primary ammo
            damage_per_shot = damage_per_shot * 1.2
            VorpalActive = 1
        elif VorpalWeapon = 2: #special ammo
            damage_per_shot = damage_per_shot * 1.15
            VorpalActive = 1
        elif VorpalWeapon 3: #heavy ammo
            damage_per_shot = damage_per_shot * 1.1
            VorpalActive = 1
    else
        0 = 0

FocusedFury: #checks for whether it is active, then for whether it should activate, then the activation requirements before setting itself active, followed by a check on how to turn it back
    if FFActive = 0:
        if FocusedFury = 1:
            if shots_fired = magCap/2:
               damage_per_shot = damage_per_shot * 1.2
               FFActive = 1
            else
                damage_per_shot = damage_per_shot
        else
            0 = 0
    else
        if time_elapsed % 10 = 0: #this time check logic needs to be looked at, probably use another variable to track when the timer would be up for the buff
            damage_per_shot = damage_per_shot * (5/6)
            FFActive = 0
        else
            0 = 0
