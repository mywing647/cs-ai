from demoparser2 import DemoParser
demo_path = "demo/pro/demo_pro_1.dem"
parser=DemoParser(demo_path)
kills=parser.parse_event("player_death")
print(kills)
print(kills["attacker_name"].value_counts())