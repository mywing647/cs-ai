import event_detection
from demoparser2 import DemoParser
import pandas as pd

parser = DemoParser("demo/pro/demo_pro_1.dem")
ticks_df = parser.parse_ticks(["X", "Y","spotted","approximate_spotted_by","pitch","yaw", "shots_fired"])#pitch up_down, yaw left_right

name_list= ticks_df["name"].unique().tolist()
player_df = ticks_df[ticks_df["name"] == "NiKo"]
player_name="niko"

def build_event_table(player_name):

    aim = event_detection.detect_aim(player_name)
    kill_list,shot_list,kill_events = event_detection.detect_kill(player_name)
    event_df = pd.DataFrame({"aim_start_tick": aim,"fire_tick": shot_list,"kill_tick":kill_list})

    return event_df
    

build_event_table(player_df)
