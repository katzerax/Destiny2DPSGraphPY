def calculate_dps(fire_rate, reload_time, damage_per_shot, magazine_capacity, ammo_reserve, delay_first_shot, x, x_increments, data_points, perk1, perk2):
    t_dmg = []
    roundingcoeff = len(str(x_increments).split(".")[1])
    fire_delay = round(60/fire_rate, roundingcoeff)
    next_fire = fire_delay
    total_damage = 0 if delay_first_shot else damage_per_shot
    time_elapsed = 0
    shots_left_reserve = ammo_reserve if delay_first_shot else (ammo_reserve - 1)
    shots_left_mag = magazine_capacity if delay_first_shot else (magazine_capacity - 1)
    shots_fired = 0 if delay_first_shot else 1
    shot_dmg_output = damage_per_shot
    output_reload_time = round(reload_time, roundingcoeff)

    for i in range(data_points):
        shot_dmg_output = damage_per_shot
        fire_delay = round(60/fire_rate, roundingcoeff)
        output_reload_time = round(reload_time, roundingcoeff)

        if perk1: #triple tap for example purposes just to see
            if shots_fired != 0:
                if tt_delay == 0:
                    if shots_fired % 3 == 0:
                        shots_left_mag += 1
                        shots_left_reserve += 1
                        tt_delay_check = shots_fired
                        tt_delay = 1
                else:
                    if tt_delay_check != shots_fired:
                        tt_delay = 0

        if perk2: #fourth times the charm
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

        if shots_left_reserve == 0: # reserve check
            total_damage = total_damage
        elif shots_left_mag == 0: # reload
            next_fire += output_reload_time
            next_fire -= fire_delay if delay_first_shot == 0 else 0
            next_fire = round(next_fire, roundingcoeff)
            shots_fired = 0
            shots_left_mag = magazine_capacity
        elif time_elapsed == next_fire:
            total_damage += shot_dmg_output
            next_fire += fire_delay
            next_fire = round(next_fire, roundingcoeff)
            shots_fired += 1
            shots_left_mag -= 1
            shots_left_reserve -= 1
        time_elapsed += x_increments
        time_elapsed = round(time_elapsed, roundingcoeff)

        t_dmg.append(total_damage)
    dps = [0]
    for z in range(data_points):
        if z != 0:
            dps.append(t_dmg[z] / x[z])
    return dps