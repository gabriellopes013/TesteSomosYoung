from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from etl.extract import get_data
from etl.transform import transform
from etl.load import load

default_args = {
    'owner': 'Gabriel Almeida',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'etl_dag',
    default_args=default_args,
    description='ETL DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 7, 1),
    catchup=False,
) as dag:

    extract_api = SimpleHttpOperator(
        task_id='extract_api',
        http_conn_id='api_connection',
        endpoint='/api/ahoy_viewer_ti',  # substitua pelo endpoint da sua API
        method='POST',
        headers={"Content-Type": "application/json"},
        data=get_data(),
        response_filter=lambda response: response.json(),
        log_response=True,
    )


    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform,
        provide_context=True,
    )

    load_data = PythonOperator(
        task_id='load_data',
        python_callable=load,
        provide_context=True,
    )
# transform_task = PythonOperator(
#     task_id='transform',
#     python_callable=transform,
#     provide_context=True,
#     dag=dag,
# )

# load_task = PythonOperator(
#     task_id='load',
#     python_callable=load,
#     provide_context=True,
#     dag=dag,
# )
extract_api >>  transform_data >> load_data
# extract_task >> transform_task >> load_task
