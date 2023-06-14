import math
import random

# Superclass
class OriginTrait:
    enabled = True

class VeistStinger(OriginTrait):
    """Random chance to provide ammo back to the magazine from the reserves."""
    def __init__(self):
        self.time_cache = -4

    def output(self, ammo_fired, time_elapsed, ammo_magazine, ammo_total, mag_cap, **_):
        if ammo_fired:
            # 4 second cooldown
            if time_elapsed >= self.time_cache + 4:
                # m: your old way of doing 10% was not actually correct :P
                veist_proc = random.randrange(1,11)
                if veist_proc == 10 and ammo_magazine < mag_cap:
                    self.time_cache = time_elapsed
                    ammo_granted = math.floor(mag_cap * 0.25)
                    # Veist now pulls from reserves and not thin air
                    if ammo_granted > ammo_total:
                        ammo_granted = ammo_total
                    ammo_magazine += ammo_granted
                    ammo_total -= ammo_granted

        return {'ammo_magazine': ammo_magazine, 'ammo_total': ammo_total}
    
ORIGIN_TRAITS_LIST = {
    0: ('Null', 'No selection', None),
    1: ('Veist Stinger', VeistStinger.__doc__, VeistStinger),
}

# def RunnethOver(self):
#     pass

    # Potentials
    # - nanotech tracers
    # - alacrity
    # - celerity
    # - bitterspite
    # - hot swap