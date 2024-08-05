from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
from etl.extract import get_data
from etl.transform import transform
from etl.testebd import testandobd
from etl.idhoy import idahoy
from etl.dim_load import load_dim_user_type, load_dim_company, load_dim_campaign, load_fatoemailmarketing

default_args = {
    'owner': 'Gabriel Almeida',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    'etl_dag',
    default_args=default_args,
    description='ETL DAG',
    schedule_interval=timedelta(minutes=10),
    start_date=datetime(2023, 7, 1),
    catchup=False,
) as dag:

    extract_api = SimpleHttpOperator(
        task_id='extract_api',
        http_conn_id='api_connection',
        endpoint='/api/ahoy_viewer_ti',
        method='POST',
        headers={"Content-Type": "application/json"},
        data=get_data(),
        response_filter=lambda response: response.json()[:10],
        log_response=True,
        
    )


    transform_data = PythonOperator(
        task_id='transform_data',
        python_callable=transform,
        provide_context=True,
    )

    testandobanco = PythonOperator(
            task_id='testandobanco',
            python_callable=testandobd,
            provide_context=True,
        )
    
    create_dim_campaign = PostgresOperator(
        task_id='create_dim_campaign',
        postgres_conn_id='postgres_conn',
        sql="""
            CREATE TABLE IF NOT EXISTS DimCampaign (
                id_campaign INT PRIMARY KEY,
                campaign VARCHAR(255) UNIQUE NOT NULL
            );
        """
    )

    create_dim_company = PostgresOperator(
        task_id='create_dim_company',
        postgres_conn_id='postgres_conn',
        sql="""
            CREATE TABLE IF NOT EXISTS DimCompany (
                id_company SERIAL PRIMARY KEY,
                company VARCHAR(255) UNIQUE NOT NULL
            );
        """
    )

    create_dim_user_type = PostgresOperator(
        task_id='create_dim_user_type',
        postgres_conn_id='postgres_conn',
        sql="""
            CREATE TABLE IF NOT EXISTS DimUserType (
                id_user_type SERIAL PRIMARY KEY,
                user_type VARCHAR(255) UNIQUE NOT NULL
);
        """
    )

    create_fato_email_marketing = PostgresOperator(
        task_id='create_fato_email_marketing',
        postgres_conn_id='postgres_conn',
        sql="""
            CREATE TABLE IF NOT EXISTS FatoEmailMarketing (
                id INT PRIMARY KEY,
                id_campaign INT,
                id_company INT,
                id_user_type INT,
                "to" VARCHAR(255),
                mailer VARCHAR(255),
                subject VARCHAR(255),
                sent_at TIMESTAMP,
                opened_at TIMESTAMP,
                clicked_at TIMESTAMP,
                token VARCHAR(255),
                FOREIGN KEY (id_campaign) REFERENCES DimCampaign(id_campaign),
                FOREIGN KEY (id_company) REFERENCES DimCompany(id_company),
                FOREIGN KEY (id_user_type) REFERENCES DimUserType(id_user_type)
            );
        """
    )
    dim_user_type_load = PythonOperator(
                task_id='carga_dimensao_user_type',
                python_callable=load_dim_user_type,
                provide_context=True,
            )
    
    dim_company_load = PythonOperator(
                task_id='carga_dimensao_company',
                python_callable=load_dim_company,
                provide_context=True,
            )
    
    dim_campaign_load = PythonOperator(
                task_id='carga_dimensao_campaign',
                python_callable=load_dim_campaign,
                provide_context=True,
            )
    
    load_fato = PythonOperator(
                task_id='carga_fatoemailmarketing',
                python_callable=load_fatoemailmarketing,
                provide_context=True,
            )
    modify_id = PythonOperator(
                task_id='modify_idahoy',
                python_callable=idahoy,
                provide_context=True,
            )
 
(extract_api >>  transform_data >> testandobanco >>
 [create_dim_campaign, create_dim_company, create_dim_user_type] >> create_fato_email_marketing 
 >> [dim_user_type_load, dim_company_load, dim_campaign_load] >> load_fato >> modify_id)
