from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from processor.grobid_parse import parsePDF
from processor.init_setup import download_and_initial_setup

with DAG(
    dag_id='cfa_pipe',
    default_args={'start_date': days_ago(1),
    'execution_timeout': timedelta(minutes=30)},
    schedule_interval='0 23 * * *',
    catchup=False
) as dag:
    
    initial_setup_task = PythonOperator(
        task_id="init_setup",
        python_callable=download_and_initial_setup,
        dag=dag
    )

    trigger_grobid = PythonOperator(
        task_id="grobid_processing",
        python_callable=parsePDF,
        dag=dag
    )

    initial_setup_task >> trigger_grobid
