"""
    Apache Airflow DAG(Directed Acyclic Graph)
    - defines tasks and order of execution
"""


from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago

from scripts import fetch_api_data, scrape_web_data, transform_data_with_dbt

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='etl_pipeline',
    default_args=default_args
    description='An ETL pipeline using DBT and Airflow',
    schedule_interval='@daily',
    start_date=days_ago(1),
) as dag:
    fetch_api_task = PythonOperator(
        task_id='fetch_api_data',
        python_callable=fetch_api_data,
    )

    scrape_web_task = PythonOperator(
        task_id='scrape_web_data',
        python_callable=scrape_web_data,
    )

    transform_data_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data_with_dbt,
    )

    load_data_task = PostgresOperator(
        task_id='load_data',
        postgres_conn_id='postgres_default',
        sql='SQL_FILE.sql',
    )

    fetch_api_task >> scrape_web_task >> transform_data_task >> load_data_task