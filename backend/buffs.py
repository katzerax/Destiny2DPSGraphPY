import stat
import math
import random

BUFFS_LIST = {
    0: ("Null", "No selection"),
    1: ("Well of Radiance", "Super that gives healing and damage bonus in an area.")
}

#Superclass
class Buff():
    def __init__(self):
        self.enabled = True

class WellofRadiance(Buff):
    def __init__(self):
        pass
        #self.well_warlocks = well_warlocks
        #self.well_cast = 0
        #self.well_timer = 0

    def output(self, dmg_output, time_elapsed, **_):
        pass
        # Rox: this code should work assuming that the variables above are passed in properly. Just setting these files up for use.
        # if not self.well_warlocks:
        #     pass
        # elif self.well_warlocks >= 1 and not self.well_cast:
        #     self.well_warlocks -= 1
        #     self.well_cast = 1
        #     self.well_timer = time_elapsed
        # elif self.well_warlocks >= 0 and self.well_cast and (time_elapsed - self.well_timer) <= 25:
        #     dmg_output *= 1.25
        # elif self.well_cast and (time_elapsed - self.well_timer) > 25:
        #     self.well_cast = 0




def WardofDawn(self):
    pass


def Shadowshot(self):
    pass


def WolfPack(self):
    pass