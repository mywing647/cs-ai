from demoparser2 import DemoParser

#parser = DemoParser("demo/pro/demo_pro_9.dem")

def detect_kill(player_name,parser):
    import numpy as np
    import pandas as pd
    ticks_df = parser.parse_ticks(["shots_fired"])
    events = dict(parser.parse_events(["player_death"]))
    player_df = ticks_df[ticks_df["name"] == player_name]

    player_df["previous"]=player_df["shots_fired"].shift(1)
    shotfire_events = player_df[(player_df["shots_fired"]>0)&(player_df["previous"]==0)]
    shotfire_list=shotfire_events["tick"].tolist()
    shot_array = np.sort(np.array(shotfire_list))

    death_df = events["player_death"]
    kill_events = death_df[
        death_df["attacker_name"] == player_name
    ]

    shot_list=[]
    kill_event_list = []
    for _, death in kill_events.iterrows():
        kill_tick = death["tick"]
        idx = np.searchsorted(shot_array, kill_tick) - 1

        if idx >= 0:
            fire_tick = shot_array[idx]
            if kill_tick - fire_tick <= 500:
                kill_event_list.append(death)
                shot_list.append(fire_tick)

    kill_event=pd.DataFrame(kill_event_list)
            
    return shot_list,kill_event

#shot_list,kill_event = detect_kill(player_name)
# print(shot_list)
# print(kill_list)

def statistic_calculation(feature,feature_name):
    import numpy as np
    import pandas as pd

    mean = np.mean(feature)   
    min = np.min(feature)     
    max = np.max(feature)  
    median= np.median(feature)
    standard=np.std(feature)
    feature_df = pd.DataFrame([{f"{feature_name}_mean": mean,
                                f"{feature_name}_min": min,
                                f"{feature_name}_max": max,
                                f"{feature_name}_median": median,
                                f"{feature_name}_standard": standard
                                 }])
    return feature_df

def detect_aim(player_name,shot_list,parser):
    import numpy as np

    ticks_df = parser.parse_ticks(["pitch","yaw"])
    player_df = ticks_df[ticks_df["name"] == player_name].copy()
    player_df = player_df.set_index("tick")

    player_df["yaw_change"] = player_df["yaw"].diff()
    player_df["pitch_change"] = player_df["pitch"].diff()
    player_df["aim_speed"]=(player_df["yaw_change"]**2 +player_df["pitch_change"]**2) ** 0.5
    aim_speed = player_df["aim_speed"]

    aim_start_list=[]
    for tick in shot_list:
        found=False
        for j in range(tick-1, tick-500,-1):
            if aim_speed.get(j, 0)>=0.1 and aim_speed.get(j+1, 0) >=0.1 and aim_speed.get(j+2, 0) >=0.1 and aim_speed.get(j-1, 0)<0.1:
                aim_start_list.append(j)
                found=True
                break
        if not found:
            aim_start_list.append(None)
            
    return aim_start_list
   
#aim_start_list = detect_aim(player_name,shot_list)
# print(aim_start_list)

def crosshead_eror(player_name,aim_start_list,kill_events,parser):
    import math
    import numpy as np
    import pandas as pd

    ticks_df = parser.parse_ticks(["X","Y","Z","pitch","yaw","ducked"])
    my_df = ticks_df[ticks_df["name"] == player_name]

    if kill_events.empty:
        return []

    if "user_name" in kill_events.columns:
        victim_col = "user_name"
    else:
        return [None] * len(aim_start_list)

    crosshead_list=[]
    for tick,victim_name in zip(aim_start_list,kill_events[victim_col]):
        my_row=my_df[my_df["tick"]==tick]
        if my_row.empty:
            crosshead_list.append(None)
            continue
        my_x = my_row["X"].iloc[0]
        my_y = my_row["Y"].iloc[0]
        my_z = my_row["Z"].iloc[0]
        yaw=my_row["yaw"].iloc[0]
        pitch= my_row["pitch"].iloc[0]

        yaw_rad=math.radians(yaw)
        pitch_rad=math.radians(pitch)

        crosshead_x = math.cos(pitch_rad) * math.cos(yaw_rad)
        crosshead_y = math.cos(pitch_rad) * math.sin(yaw_rad)
        crosshead_z = -math.sin(pitch_rad)

        victim_row=ticks_df[(ticks_df["tick"]==tick)&(ticks_df["name"]==victim_name)]
        if victim_row.empty:
            crosshead_list.append(None)
            continue
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

    return crosshead_list

#crosshead_list=crosshead_eror(player_name,aim_start_list,kill_event)
#print(crosshead_list)





