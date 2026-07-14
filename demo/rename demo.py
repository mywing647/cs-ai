import os

demo_path=["amateur","pro"]

for path in demo_path:
    max_index = 0
    files=os.listdir("demo/"+path)
    prefix = f"demo_{path}_"

    for file in files:
        if file.startswith(prefix) and file.endswith(".dem"):
            num = file[len(prefix):-4]
            if num.isdigit():
                max_index = max(max_index, int(num))
    for file in files:
        if file.endswith(".dem") and not file.startswith(prefix):
            max_index += 1
            new_filename = f"{prefix}{max_index}.dem"
            new_name = "demo/" + path + "/" + new_filename
            old_name="demo/"+path+"/"+file
            os.rename(old_name, new_name)

print("complete rename")