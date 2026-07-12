from feature_extraction import feature_extraction
import os
import pandas as pd
import traceback

def build_final_dataset():
    from feature_extraction import feature_extraction
    base_dir = r"E:\projects\cs-ai\demo"
    pro_dir = os.path.join(base_dir, "pro")
    amateur_dir = os.path.join(base_dir, "amateur")

    data_dir = r"E:\projects\cs-ai\data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    output_csv = os.path.join(data_dir, "data.csv")
    log_file = os.path.join(data_dir, "processed_demos.txt")
        
    processed_files = set()
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            processed_files = set(line.strip() for line in f)

    all_demos_data = []
    new_processed_names = []
    if os.path.exists(pro_dir):
        for file_name in os.listdir(pro_dir):
            if file_name.endswith(".dem"):
                if file_name in processed_files:
                    print(f"skip files that were already processed: {file_name}")
                    continue
                
                file_path = os.path.join(pro_dir, file_name)
                
                try:
                    df = feature_extraction(file_path, 0)
                    if not df.empty:
                        all_demos_data.append(df)
                        print(f"complete processing demo:{file_name}")
                    new_processed_names.append(file_name)
                    
                except Exception as e:
                    traceback.print_exc()

    if os.path.exists(amateur_dir):
        for file_name in os.listdir(amateur_dir):
            if file_name.endswith(".dem"):
                if file_name in processed_files:
                    print(f"skip files that were already processed: {file_name}")
                    continue

                file_path = os.path.join(amateur_dir, file_name)              
                try:
                    df = feature_extraction(file_path,1)
                    if not df.empty:
                        all_demos_data.append(df)
                        print(f"complete processing demo:{file_name}")
                    new_processed_names.append(file_name)
                    
                except Exception as e:
                    traceback.print_exc()
        
    if all_demos_data:
        final_dataset = pd.concat(all_demos_data, axis=0, ignore_index=True)

        if os.path.exists(output_csv):
            final_dataset.to_csv(output_csv, mode='a', header=False, index=False, encoding='utf-8-sig')
            print(f"adding new data successfully")
        else:
            final_dataset.to_csv(output_csv, index=False, encoding='utf-8-sig')
            print(f"create new data file successfully")
            
        with open(log_file, "a", encoding="utf-8") as f:
            for name in new_processed_names:
                f.write(name + "\n")
    else:
        print("no new demos waiting for processing")
            

if __name__ == "__main__":
    build_final_dataset()