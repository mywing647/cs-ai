from feature_extraction import feature_extraction
import traceback

file_path = r"E:\projects\cs-ai\demo\amateur\demo_amateur_1.dem"

try:
    df = feature_extraction(file_path, 1)
    print("no error")
    
except Exception as e:
    print("here is the error：\n")
    traceback.print_exc()

# from demoparser2 import DemoParser

# file_path = r"E:\projects\cs-ai\demo\pro\demo_pro_17.dem"
# parser = DemoParser(file_path)

# try:
#     events = parser.parse_events(["player_death"])
#     if "player_death" in events:
#         death_df = events["player_death"]
#         print(death_df.columns.tolist())
# except Exception as e:
#     print(f"error occur：{e}")