from demoparser2 import DemoParser
parser = DemoParser("demo/pro/demo_pro_1.dem")
asdsaevent_df = parser.parse_event("player_death", player=["X", "Y"], other=["total_rounds_played"])
ticks_df = parser.parse_ticks(["X", "Y", "pitch","yaw"])#pitch up_down, yaw left_right
niko = ticks_df[ticks_df["name"] == "NiKo"]
print(niko[["tick","X","Y","pitch","yaw"]].iloc[500:520])