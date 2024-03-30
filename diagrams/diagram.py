!pip install diagrams
from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.container import Docker
from diagrams.onprem.client import User
from diagrams.saas.analytics import Snowflake
from diagrams.aws.storage import S3
 
graph_attr = {
    "fontsize": "30",
    "bgcolor": "white",
    "nodesep": "1.60",  # adjust the space between nodes
    "ranksep": "0.75",  # adjust the space between ranks (levels)
    "width": "0.75",    # set the width attribute (in inches)
    "height": "0.75",   # set the height attribute (in inches)
    "fixedsize": "true" # force fixed size of nodes
}
 
with Diagram("Architectural Diagram", show=False) as data_pipeline:
    user = User("end-user")
    with Cluster("Streamlit App"):
        streamlit_app = Docker("Streamlit App")
    fast_api_service = Custom("FastAPI Service\n(Data Transformation)", "FastAPITrigger.png")
    
    with Cluster("S3"):
        s3_buckets = S3("S3_buckets") 
    snowflake_db = Snowflake("Snowflake") 
    airflow = Airflow("Airflow")
    
    with Cluster("Airflow Pipeline"):
        extraction = Custom("Data Extraction (Grobid/PyPDF)", "Extraction.png")  
        validation = Custom("Data Validation", "Validation.png")  
        loading = Custom("Data Loading", "Loading.png")    
    
    # Dependencies and Connections

 
    # Data Flow
    user >> streamlit_app
    streamlit_app >> fast_api_service
    fast_api_service >> s3_buckets
    fast_api_service >> airflow
    airflow >> s3_buckets
    airflow >> extraction
    airflow >> validation
    airflow >> loading
    loading >> snowflake_db
    fast_api_service >> snowflake_db
    snowflake_db >> fast_api_service
    fast_api_service >> streamlit_app

 
data_pipeline