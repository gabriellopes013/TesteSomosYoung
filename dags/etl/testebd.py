import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook

def testandobd():
    # Obtém a conexão usando PostgresHook
    pg_hook = PostgresHook(postgres_conn_id='postgres_conn')

    try:
        # Usa o método get_conn do PostgresHook para obter a conexão
        engine = pg_hook.get_sqlalchemy_engine()

        # Testa a conexão
        with engine.connect() as connection:
            print("Conexão bem-sucedida!")
            # Testa a execução de uma consulta simples
            df = pd.read_sql('SELECT NOW()', connection)
            print(df)
    except Exception as e:
        print(f"Erro ao conectar: {e}")
    
    return print(df)