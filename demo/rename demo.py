import os


demo_path=["amateur","pro"]

for path in demo_path:
    count=0
    files=os.listdir("demo/"+path)
    #count = len(files)

    for file in files:
        if file.endswith(".dem") and file[0:4]=="demo":
            count+=1
            new_name="demo/"+path+"/demo_"+path+"_"+str(count)+".dem"
            old_name="demo/"+path+"/"+file
            os.rename(old_name, new_name)
