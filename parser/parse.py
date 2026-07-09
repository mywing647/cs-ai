#from demoparser2 import DemoParser
#demo_path = "demo/pro/demo_pro_1.dem"
#parser=DemoParser(demo_path)
#kills=parser.parse_event("player_death")
#print(kills["attacker_name"].value_counts())

from demoparser2 import DemoParser
parser = DemoParser("demo/pro/demo_pro_1.dem")
death_df = parser.parse_event("player_death", player=["X", "Y"], other=["total_rounds_played"])
ticks_df = parser.parse_ticks(["X", "Y","spotted","approximate_spotted_by"])#pitch up_down, yaw left_right
#niko = ticks_df[ticks_df["name"] == "NiKo"]
name_list= ticks_df["name"].unique().tolist()

print(ticks_df.head(30))