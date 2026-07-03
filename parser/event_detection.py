from demoparser2 import DemoParser
parser = DemoParser("demo/pro/demo_pro_1.dem")
ticks_df = parser.parse_ticks(["X", "Y","spotted","approximate_spotted_by","pitch","yaw"])#pitch up_down, yaw left_right

name_list= ticks_df["name"].unique().tolist()

niko = ticks_df[ticks_df["name"] == "NiKo"]
niko["previous"] = niko["spotted"].shift(1)
spotted_events = niko[(niko["spotted"] == True) & (niko["previous"] == False)]
print(spotted_events[["tick"]])

niko["yaw_change"] = niko["yaw"].diff()
niko["pitch_change"] = niko["pitch"].diff()
niko["aim_speed"]=(niko["yaw_change"]**2 +niko["pitch_change"]**2) ** 0.5
