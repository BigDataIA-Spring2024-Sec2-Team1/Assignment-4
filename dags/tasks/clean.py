import pandas as pd
from tasks.util.pydantic_models.pydantic_classes import MetaDataPDFClass
import os

def get_clean_csv(**kwargs):
    try:
        ti = kwargs['ti']
        print("context", ti)
        input_path = ti.xcom_pull(key="TEMP_OUTPUT_TXT", task_ids="grobid_processing")
        print("reding file", input_path)
        # Read the CSV file
        df = pd.read_json(input_path)
        
        # Convert each row to a CleanCSV object
        clean_rows = []
        for _, row in df.iterrows():
            try:
                clean_row = MetaDataPDFClass(**row)
                clean_rows.append(clean_row.dict())
            except ValidationError as e:
                print(f"Skipping invalid row: {e}")
        
        file_path=ti.xcom_pull(key="file_path", task_ids="init_setup")
        data = file_path.split("/")[-1].split("-")
        print(data)

        
        folder_path = ti.xcom_pull(key="temp_folder_path", task_ids="init_setup")
        writePath = os.path.join(folder_path, f"Grobid_RR_{data[0]}_{data[1]}_combined.csv")
        # Write the clean rows to a new CSV file
        clean_df = pd.DataFrame(clean_rows)
        clean_df.to_csv(writePath, index=True)
        ti.xcom_push(key="output_file_path", value=writePath)
        print("Clean CSV file created successfully.")
        return True
    except FileNotFoundError:
        print("Input CSV file not found.")
        return False
    except Exception as e:
        print(f"Error processing CSV: {e}")
        return False
