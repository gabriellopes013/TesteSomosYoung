import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook

def testandobd():
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')

    try:
        engine = pg_hook.get_sqlalchemy_engine()

        with engine.connect() as connection:
            print("Conexão bem-sucedida!")
            df = pd.read_sql('SELECT NOW()', connection)
            print(df)
    except Exception as e:
        print(f"Erro ao conectar: {e}")
    
    return print(df)