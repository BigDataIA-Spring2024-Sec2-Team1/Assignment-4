from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from processor.grobid_parse import parsePDF
from processor.init_setup import download_s3
from tasks.clean import get_clean_csv
from processor.upload_to_snowflake import push_data_to_snowflake
with DAG(
    dag_id='cfa_workflow',
    default_args={'start_date': days_ago(1),
    'execution_timeout': timedelta(minutes=30)},
    schedule_interval='0 23 * * *',
    catchup=False
) as dag:
    
    initial_setup_task = PythonOperator(
        task_id="init_setup",
        python_callable=download_s3,
        dag=dag
    )

    trigger_grobid = PythonOperator(
        task_id="grobid_processing",
        python_callable=parsePDF,
        dag=dag
    )
    
    data_validation = PythonOperator(
        task_id="data_validation",
        python_callable=get_clean_csv,
        dag=dag
    )
     
    upload_to_snowflake = PythonOperator(
        task_id="upload_to_snowflake",
        python_callable=push_data_to_snowflake,
        dag=dag
    )

    initial_setup_task >> trigger_grobid >> data_validation >> upload_to_snowflake
