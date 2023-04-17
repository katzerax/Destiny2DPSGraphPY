def calculate_dps(fire_rate, reload_time, damage_per_shot, magazine_capacity, ammo_reserve, delay_first_shot, x, x_increments, data_points):
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