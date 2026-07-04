from demoparser2 import DemoParser
parser = DemoParser("demo/pro/demo_pro_1.dem")
ticks_df = parser.parse_ticks(["X", "Y","spotted","approximate_spotted_by","pitch","yaw", "shots_fired"])#pitch up_down, yaw left_right

name_list= ticks_df["name"].unique().tolist()
player_df = ticks_df[ticks_df["name"] == "NiKo"]

def detect_spotted(player_df):
    player_df["previous"] = player_df["spotted"].shift(1)
    spotted_events = player_df[(player_df["spotted"] == True) & (player_df["previous"] == False)]

    spotted_list=[]
    for i in range(len(spotted_events)):
        spotted_event=spotted_events["tick"].iloc[i]
        spotted_list.append(spotted_event)

    return spotted_list

spotted_list = detect_spotted(player_df)

def detect_aim(player_df,threshold):
    player_df["yaw_change"] = player_df["yaw"].diff()
    player_df["pitch_change"] = player_df["pitch"].diff()
    player_df["aim_speed"]=(player_df["yaw_change"]**2 +player_df["pitch_change"]**2) ** 0.5
    aim_start_event = player_df[(player_df["aim_speed"].shift(-1) >threshold) & (player_df["aim_speed"].shift(-2) >threshold)&(player_df["aim_speed"] >threshold)]

    #print(player_df["aim_speed"].describe())

    count=len(spotted_list)
    aim_start_list=[]
    for i in range(count-1):
        tick=spotted_list[i]
        next_tick=spotted_list[i+1]
        aim_start_after_spotted=aim_start_event[(aim_start_event["tick"] > tick) & (aim_start_event["tick"] < next_tick)]
        if not aim_start_after_spotted.empty:
            aim_start_after_spotted=aim_start_after_spotted.iloc[0]
            aim_start_list.append(aim_start_after_spotted["tick"])

    last_tick = spotted_list[-1]
    aim_start_after_last_spotted=aim_start_event[aim_start_event["tick"] > last_tick]
    if not aim_start_after_last_spotted.empty:
        aim_start_after_last_spotted=aim_start_after_last_spotted.iloc[0]
        aim_start_list.append(aim_start_after_last_spotted["tick"])

    return aim_start_list

aim_start_list = detect_aim(player_df)

def detect_shot(player_df):
    count=len(aim_start_list)
    player_df["previous_shot"] = player_df["shots_fired"].shift(1)
    shotfire_events = player_df[(player_df["shots_fired"]>player_df["previous_shot"])]

    shotfire_list=[]
    for i in range(count-1):
        tick=aim_start_list[i]
        next_tick=aim_start_list[i+1]

        if not shotfire_events.empty:
            shotfire_after_spotted=shotfire_events[(shotfire_events["tick"] > tick) & (shotfire_events["tick"] < next_tick)]
            #print(shotfire_after_spotted["tick"])
            if not shotfire_after_spotted.empty:
                shotfire_after_spotted=shotfire_after_spotted.iloc[0]
                shotfire_list.append(shotfire_after_spotted["tick"])

    last_tick = aim_start_list[-1]
    shotfire_after_last_aim_start=shotfire_events[shotfire_events["tick"] > last_tick]
    if not shotfire_after_last_aim_start.empty:
        shotfire_after_last_aim_start=shotfire_after_last_aim_start.iloc[0]
        shotfire_list.append(shotfire_after_last_aim_start["tick"])

    return shotfire_list

shotfire_list = detect_shot(player_df)

#print(spotted_list)
#print(aim_start_list)
#print(shotfire_list)
