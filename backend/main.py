from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import boto3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
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
    # for uploaded_file in files:
    try:
        s3_client.upload_fileobj(files.file, S3_BUCKET_NAME, files.filename)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return {"message": "File(s) uploaded successfully"}

@app.get("/")
def hello():
    return {"message": "Backend is running"}
