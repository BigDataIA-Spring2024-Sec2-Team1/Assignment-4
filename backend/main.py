from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import boto3
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://frontend:8501"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

AWS_ACCESS_KEY_ID = 'AKIATNRXE6JBYW4S4PQP'
AWS_SECRET_ACCESS_KEY = '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'
S3_BUCKET_NAME = 'bigdata-assignment-04'
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

@app.post("/upload")
async def upload_file(files: UploadFile = File(...)):
    try:
        print("Uploading file to s3", files.filename)
        s3_client.upload_fileobj(files.file, S3_BUCKET_NAME, files.filename)
        print("file uploaded successfully")
        triggerAirFlowPipeline(f'https://{S3_BUCKET_NAME}.s3.amazonaws.com/{files.filename}')
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    return {"message": "File(s) uploaded successfully"}

@app.get("/")
def hello():
    return {"message": "Backend is running"}

def triggerAirFlowPipeline(s3_url):
    airflow_base_url = 'http://host.docker.internal:8024'
    airflow_url = f"{airflow_base_url}/api/v1/dags/cfa_workflow/dagRuns"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Authorization": "Basic YWlyZmxvdzphaXJmbG93",
    }
    data = {"conf": {"s3_uploaded_file": s3_url}}
    response = requests.post(airflow_url, headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 201:
        response_json = response.json()
        return (
            "DAG triggered successfully",
            response_json["dag_run_id"],
        )
    else:
        return f"Failed to trigger DAG: {response.text}", None, None 
