from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator


dag = DAG('testebanco', description='testebanco',
          schedule_interval=None, start_date=datetime(2023,3,5),
          catchup=False)

teste = PostgresOperator(task_id='teste',
                         postgres_conn_id='postgres_conn',
                         sql='SELECT NOW()',
                         dag=dag)

teste