import os

demo_path=["amateur","pro"]

for path in demo_path:
    files=os.listdir("demo/"+path)
    count=0
    for file in files:
        if file.endswith(".dem"):
            count+=1
            new_name="demo/"+path+"/demo_"+path+"_"+str(count)+".dem"
            ###old_name="demo/"+path+"/"+file
            old_name=os.path.abspath(file)
            os.rename(old_name, new_name)
