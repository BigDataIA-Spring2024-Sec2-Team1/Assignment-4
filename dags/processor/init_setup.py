import random
import os
from pathlib import Path
import boto3
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables from .env file
load_dotenv()

# Access environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def _generate_random_string() -> str:
    return ''.join(random.choice('0123456789abcdef') for i in range(16))

def _get_path_from_url(url):
    parsed_url = urlparse(url)
    return parsed_url.path.lstrip('/')

def download_and_initial_setup(**kwargs):
    # pdf_url = "https://bigdata-assignment-04.s3.amazonaws.com/2024-l1-topics-combined-2.pdf"
    pdf_url = kwargs["dag_run"].conf["s3_uploaded_file"]
    print('Selected pdf:' + pdf_url)
    ti = kwargs['ti']
    local_folder_name = _generate_random_string()
    local_folder_path = os.path.join("/tmp/webapp", local_folder_name)
    local_file_path = os.path.join(local_folder_path, os.path.basename(pdf_url))
    Path(local_folder_path).mkdir(parents=True, exist_ok=True)

    pdf_path = _get_path_from_url(pdf_url)
    print(f'pdf path {pdf_path}')
    print(f'pdf local file path {local_file_path}')
    s3_client.download_file(S3_BUCKET_NAME, pdf_path, local_file_path)

    ti.xcom_push(key="temp_folder_name", value=local_folder_name)
    ti.xcom_push(key="temp_folder_path", value=local_folder_path)
    ti.xcom_push(key="s3_pdf_link", value=pdf_url)
    ti.xcom_push(key="file_path", value=local_file_path)
