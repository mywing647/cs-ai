from demoparser2 import DemoParser
import pandas as pd

#parser = DemoParser("demo/pro/demo_pro_1.dem")
#player_name = "NiKo"

def build_event_table(player_name,parser):
    import event_detection
    from demoparser2 import DemoParser
    import pandas as pd

    shot_list,kill_event = event_detection.detect_kill(player_name,parser)
    aim_start_list = event_detection.detect_aim(player_name,shot_list,parser)
    crosshead_error=event_detection.crosshead_eror(player_name,aim_start_list,kill_event,parser)

    if kill_event.empty or "tick" not in kill_event.columns:
        return pd.DataFrame()

    event_df = pd.DataFrame({"aim_start_tick": aim_start_list,
                             "fire_tick": shot_list,
                             "kill_tick":kill_event["tick"].tolist(),
                             "crosshead_error":crosshead_error})
    
    event_df["reaction_time"] = event_df["fire_tick"] - event_df["aim_start_tick"]
    event_df["spray_time"] = event_df["kill_tick"] - event_df["fire_tick"]
    event_df = event_df[event_df["crosshead_error"] < 30]
    event_df = event_df[event_df["reaction_time"] > 0]
    if event_df.empty:
        return pd.DataFrame()

    crosshead_stats = event_detection.statistic_calculation(event_df["crosshead_error"], "crosshead")
    reaction_stats = event_detection.statistic_calculation(event_df["reaction_time"], "reaction")
    spray_stats = event_detection.statistic_calculation(event_df["spray_time"], "spray")
    
    statistic_df = pd.concat([crosshead_stats, reaction_stats, spray_stats], axis=1)    
    return statistic_df
    

# print(build_event_table(player_name))
