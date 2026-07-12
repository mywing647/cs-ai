#path="demo/pro/demo_pro_9.dem"
#ispro=1

def feature_extraction(path,is_pro):
    from demoparser2 import DemoParser
    import framework
    import pandas as pd

    parser = DemoParser(path)
    ticks_df = parser.parse_ticks(["X", "Y","spotted","approximate_spotted_by","pitch","yaw", "shots_fired"])
    name_list= ticks_df["name"].unique().tolist()
    
    player_stat=[]
    for player_name in name_list:
        player_stat_df=framework.build_event_table(player_name,parser)
        if player_stat_df.empty:
                continue
        player_stat_df["player_name"] = player_name

        player_stat_df["is_pro"] = is_pro
        player_stat.append(player_stat_df)
    if player_stat:
        final_dataset = pd.concat(player_stat, axis=0, ignore_index=True)
    else:
        final_dataset = pd.DataFrame()
        
    return final_dataset
        


#print(feature_extraction(path,ispro))