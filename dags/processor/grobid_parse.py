from langchain_community.document_loaders.parsers import GrobidParser
from langchain_community.document_loaders.generic import GenericLoader
import os
import json

def parsePDF(**kwargs):
    print("parsing pdf using langchain's grobid parser")
    try:
        ti = kwargs['ti']
        folder_path = ti.xcom_pull(key="temp_folder_path", task_ids="init_setup")
        file_path=ti.xcom_pull(key="file_path", task_ids="init_setup")
        print("folder_path_is", folder_path)
        
        print("full path", file_path)
        loader = GenericLoader.from_filesystem(
            file_path,
            parser= GrobidParser(segment_sentences=False, grobid_server="http://grobid:8070/api/processFulltextDocument")
        )
        docs = loader.load()
        data = file_path.split("/")[-1].split("-")
        print(data)

        writePath = os.path.join(folder_path, f"Grobid_RR_{data[0]}_{data[1]}_combined.json")
        print("storing to ", writePath)

        res = []
        with open(writePath, "w") as file:
            for i in range(len(docs)):
                res.append({"text": docs[i].metadata['text'], "section_title": docs[i].metadata['section_title'],"file_path": docs[i].metadata['file_path']})
            json.dump(res, file)
    
        ti.xcom_push(key="TEMP_OUTPUT_TXT", value=writePath)

        print(f"Extracted text from '{file_path}' and saved to: {writePath}")
    except Exception as e:
        print("in exception", e)
