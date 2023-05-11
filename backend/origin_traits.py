import stat
import math
import random

ORIGIN_TRAITS_LIST = {
    0: ("Null", "No selection"),
    1: ("Veist Stinger", "Random chance to provide ammo back to the magazine from the reserves.")
}


#Superclass
class OriginTrait():
    def __init__(self):
        self.enabled = True

class VeistStinger(OriginTrait):
    def __init__(self, **_):
        self.veist_check = 0

    def output(self, ammo_fired, ammo_magazine, mag_cap, **_):

        if ammo_fired != self.veist_check:
            veist_proc = round(random.randrange(1,100), 5)
            self.veist_check = ammo_fired
            if ammo_magazine == 0:
                veist_proc = 1
            if veist_proc >= 90:
                ammo_magazine += math.floor(mag_cap * 0.25)

        return {'ammo_magazine': ammo_magazine}


# def RunnethOver(self):
#     pass

    # Potentials
    # - nanotech tracers
    # - alacrity
    # - celerity
    # - bitterspite
    # - hot swap