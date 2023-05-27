#Superclass
class Buff():
    def __init__(self, isconstant:bool=True):
        self.constant = isconstant
        self.enabled = True

    def output(self, dmg_output, time_elapsed, **_):
        if self.constant:
            return {'dmg_output': dmg_output * self.multiplier}
        else:
            if time_elapsed <= self.FULL_TIMER:
                return {'dmg_output': dmg_output * self.multiplier}
            else:
                self.enabled = False
                return {'dmg_output': dmg_output}

###########
## BUFFS ##
###########

# 1 - Well of Radiance
class WellofRadiance(Buff):
    """25% damage bonus while standing in the Well of Radiance"""
    multiplier = 1.25
    FULL_TIMER = 20
    def __init__(self, isconstant:bool, **_):
        super().__init__(isconstant)

# 2 - Ward of Dawn
class WardofDawn(Buff):
    """25% damage bonus after passing through the Ward of Dawn."""
    # I honestly have no idea how long bubble lasts LMFAO
    multiplier = 1.25
    FULL_TIMER = 30
    def __init__(self, isconstant:bool, **_):
        super().__init__(isconstant)

# 3 - Blessing of the Sky
class BlessingoftheSky(Buff):
    """35% damage bonus when applied via Lumina or Boots of the Assembler"""
    # Dont know if timer is diff from Lumina to BotA but it prob is
    multiplier = 1.35
    FULL_TIMER = 5
    def __init__(self, isconstant:bool, **_):
        super().__init__(isconstant)
            
# 4 - Banner Shield
class BannerShield(Buff):
    """40% damage bonus while shooting through the Banner Shield"""
    # NOTE this timer is dead wrong I just couldnt find the actual
    multiplier = 1.4
    FULL_TIMER = 20
    def __init__(self, isconstant:bool, **_):
        super().__init__(isconstant)


#############
## DEBUFFS ##
#############

# 1 - Shadowshot
class Shadowshot(Buff):
    """30% debuff to any enemy caught in the tether range"""
    # timer: I think? also mobius diesofcringe
    multiplier = 1.3
    FULL_TIMER = 12
    def __init__(self, isconstant:bool, **_):
        super().__init__(isconstant)
            
# 2 - Tractor Cannon
class TractorCannon(Buff):
    """30% debuff to any enemy hit by Tractor Cannon"""
    multiplier = 1.3
    FULL_TIMER = 11
    def __init__(self, isconstant:bool, **_):
        super().__init__(isconstant)

# 3 - Divinity
class Divinity(Buff):
    """15% debuff to any enemy constantly being damaged by Divinity"""
    # timer: actually what do we do for this lmfao
    multiplier = 1.15
    FULL_TIMER = 50
    def __init__(self, isconstant:bool, **_):
        super().__init__(isconstant)

###################
## WEAPON BOOSTS ##
###################

# 1 - Surge Mod
class SurgeMod(Buff):
    """22% damage bonus to any weapon of matching element"""
    # blah blah time dilation blah blah
    multiplier = 1.22
    FULL_TIMER = 15
    def __init__(self, isconstant:bool, **_):
        super().__init__(isconstant)


###############
## ETC BUFFS ##
###############

# 1 - Pack Hunter
class PackHunter(Buff):
    """Grants Wolfpack Rounds to any legendary rocket"""
    pass
            
# - Jolt? (also jolt got its scaling removed if you didnt see :P)

BUFFS_LIST = {
    0: ("Null", "No selection", ""),
    1: ("Well of Radiance", WellofRadiance.__doc__, WellofRadiance),
    2: ("Ward of Dawn", WardofDawn.__doc__, WardofDawn),
    3: ("Blessing of the Sky", BlessingoftheSky.__doc__, BlessingoftheSky),
    4: ("Banner Shield", BannerShield.__doc__, BannerShield)
}

DEBUFFS_LIST = {
    0: ("Null", "No selection", ""),
    1: ("Shadowshot", Shadowshot.__doc__, Shadowshot),
    2: ("Tractor Cannon", TractorCannon.__doc__, TractorCannon),
    3: ("Divinity", Divinity.__doc__, Divinity)
}

WEAPON_BOOSTS_LIST = {
    0: ("Null", "No selection", ""),
    1: ("Surge Mod", SurgeMod.__doc__, SurgeMod),
}

ETC_LIST = {
    0: ("Null", "No selection", ""),
    1: ("Pack Hunter", PackHunter.__doc__, PackHunter)
}