import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook

def load_dim_user_type(**context):
    task_instance = context['ti']
    df = task_instance.xcom_pull(task_ids='transform_data')
    unique_user_types = df[['user_type']].drop_duplicates()
    
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    conn = pg_hook.get_sqlalchemy_engine()
    
    for _, row in unique_user_types.iterrows():
        conn.execute(f"""
            INSERT INTO public.dimusertype (user_type)
            VALUES ('{row['user_type']}')
            ON CONFLICT (user_type) DO NOTHING;
        """)
    

    print("Dados inseridos na tabela DimUserType com sucesso.")

def load_dim_company(**context):
    task_instance = context['ti']
    df = task_instance.xcom_pull(task_ids='transform_data')
    unique_company = df[['company']].drop_duplicates()
    
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    conn = pg_hook.get_sqlalchemy_engine()
    
    for _, row in unique_company.iterrows():
        conn.execute(f"""
            INSERT INTO public.dimcompany (company)
            VALUES ('{row['company']}')
            ON CONFLICT (company) DO NOTHING;
        """)
    

    print("Dados inseridos na tabela DimCompany com sucesso.")

def load_dim_campaign(**context):
    task_instance = context['ti']
    df = task_instance.xcom_pull(task_ids='transform_data')
    unique_campaign = df[['id_campaign','campaign']].drop_duplicates()
    
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    conn = pg_hook.get_sqlalchemy_engine()
    
    for _, row in unique_campaign.iterrows():
        conn.execute(f"""
            INSERT INTO public.dimcampaign (id_campaign,campaign)
            VALUES ('{row['id_campaign']}','{row['campaign']}')
            ON CONFLICT (id_campaign) DO NOTHING;
        """)
    

    print("Dados inseridos na tabela DimCampaign com sucesso.")

def load_fatoemailmarketing(**kwargs):
    task_instance = kwargs['ti']

    df = task_instance.xcom_pull(task_ids='transform_data')

    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(f"SELECT id_campaign FROM DimCampaign WHERE campaign = '{row['campaign']}'")
        id_campaign = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT id_company FROM DimCompany WHERE company = '{row['company']}'")
        id_company = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT id_user_type FROM DimUserType WHERE user_type = '{row['user_type']}'")
        id_user_type = cursor.fetchone()[0]

        cursor.execute(f"""
            INSERT INTO fatoemailmarketing (
                id,id_campaign, id_company, id_user_type, "to", mailer, subject, sent_at, opened_at, clicked_at, token
            ) VALUES ('{row['id']}','{id_campaign}', '{id_company}', '{id_user_type}', '{row['to']}', '{row['mailer']}', '{row['subject']}', '{row['sent_at']}', '{row['opened_at']}', '{row['clicked_at']}', '{row['token']}')
        """.replace("'None'",'Null'))

    conn.commit()
    cursor.close()
    conn.close()

