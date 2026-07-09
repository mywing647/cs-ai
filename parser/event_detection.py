from demoparser2 import DemoParser

parser = DemoParser("demo/pro/demo_pro_9.dem")
ticks_df = parser.parse_ticks(["X", "Y","spotted","approximate_spotted_by","pitch","yaw", "shots_fired","death_time"])
name_list= ticks_df["name"].unique().tolist()

def detect_kill(player_name):
    import numpy as np

    ticks_df = parser.parse_ticks(["shots_fired"])
    events = dict(parser.parse_events(["player_death"]))
    player_df = ticks_df[ticks_df["name"] == player_name]

    player_df["previous"]=player_df["shots_fired"].shift(1)
    shotfire_events = player_df[(player_df["shots_fired"]>0)&(player_df["previous"]==0)]
    shotfire_list=shotfire_events["tick"].tolist()
    shot_array = np.array(shotfire_list)

    death_df = events["player_death"]
    kill_events = death_df[
        death_df["attacker_name"] == player_name
    ]

    kill_list = []
    shot_list=[]
    shot_array = np.array(shotfire_list)

    for kill_tick in kill_events["tick"]:
        idx = np.searchsorted(shot_array, kill_tick) - 1

        if idx >= 0:
            fire_tick = shot_array[idx]

            if kill_tick - fire_tick <= 500:
                kill_list.append(kill_tick)
                shot_list.append(fire_tick)
            
    return kill_list,shot_list,kill_events

player_name = "NiKo"

kill_list,shot_list,kill_events = detect_kill(player_name)
# print(shot_list)
# print(kill_list)

def detect_aim(player_name,shot_list):
    import numpy as np

    ticks_df = parser.parse_ticks(["pitch","yaw"])
    player_df = ticks_df[ticks_df["name"] == player_name]

    player_df["yaw_change"] = player_df["yaw"].diff()
    player_df["pitch_change"] = player_df["pitch"].diff()
    player_df["aim_speed"]=(player_df["yaw_change"]**2 +player_df["pitch_change"]**2) ** 0.5
    aim_speed = player_df["aim_speed"].to_numpy()

    aim_start_list=[]
    for tick in shot_list:
        for j in range(tick-1, tick-500,-1):
            if aim_speed[j]>=0.1 and aim_speed[j+1] >=0.1 and aim_speed[j+2] >=0.1 and aim_speed[j-1]<0.1:
                aim_start_list.append(j)
                break
            
    return aim_start_list
   
aim_start_list = detect_aim(player_name,shot_list)
print(aim_start_list)

def crosshead_eror(player_name,aim_start_list,kill_events):
    import math
    import numpy as np

    ticks_df = parser.parse_ticks(["X","Y","Z","pitch","yaw","ducked"])
    my_df = ticks_df[ticks_df["name"] == player_name]

    victim_name = kill_events["user_name"]

    crosshead_list=[]
    for tick in aim_start_list:
        my_row=my_df[my_df["tick"]==tick]
        my_x = my_row["X"].values[0]
        my_y = my_row["Y"].values[0]
        my_z = my_row["Z"].values[0]
        yaw=my_row["yaw"].values[0]
        pitch= my_row["pitch"].values[0]

        yaw_rad=math.radians(yaw)
        pitch_rad=math.radians(pitch)

        crosshead_x = math.cos(pitch_rad) * math.cos(yaw_rad)
        crosshead_y = math.cos(pitch_rad) * math.sin(yaw_rad)
        crosshead_z = -math.sin(pitch_rad)

        victim_name = kill_events["user_name"].iloc[0]
        victim_row=ticks_df[(ticks_df["tick"]==tick)&(ticks_df["name"]==victim_name)]
        victim_x=victim_row["X"].iloc[0]
        victim_y=victim_row["Y"].iloc[0]
        victim_z=victim_row["Z"].iloc[0]+72

        to_head_x =victim_x-my_x
        to_head_y =victim_y-my_y
        is_ducked = my_row["ducked"].iloc[0]

        if is_ducked:
            to_head_z =victim_z-(my_z+46)
        else:
            to_head_z =victim_z-(my_z+64)

        head_dist = math.sqrt(to_head_x**2 + to_head_y**2 + to_head_z**2)
        if head_dist == 0:
            crosshead_list.append(0)
            continue

        to_head_x /= head_dist
        to_head_y /= head_dist
        to_head_z /= head_dist

        dot = (crosshead_x * to_head_x + crosshead_y * to_head_y + crosshead_z * to_head_z)
        dot = max(-1, min(1, dot))
        angle = math.degrees(math.acos(dot))
        crosshead_list.append(angle)

    valid_errors = [e for e in crosshead_list if e < 30]

    if len(valid_errors) > 0:
        mean_error = np.mean(valid_errors)   
        min_error = np.min(valid_errors)     
        final_error = valid_errors[-1]  
    return mean_error,min_error,final_error

mean_error,min_error,final_error=crosshead_eror(player_name,aim_start_list,kill_events)
print(mean_error,min_error,final_error)





