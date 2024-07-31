from sqlalchemy import create_engine
from airflow.hooks.base import BaseHook

def load(**context):

    task_instance = context['ti']
    df = task_instance.xcom_pull(task_ids='transform_data')
    # Obtém a conexão do Airflow
    conn = BaseHook.get_connection('postgres_conn')
    
    # Cria a string de conexão usando os detalhes da conexão do Airflow
    connection_string = f'postgresql+psycopg2://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}'
    
    # Cria o engine de conexão
    engine = create_engine(connection_string)
    
    # Nome da tabela onde os dados serão carregados
    table_name = 'testando'  # Substitua pelo nome da tabela onde deseja inserir os dados
    
    # Carrega o DataFrame na tabela PostgreSQL
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)  # Use 'replace', 'append', or 'fail'
        print("Dados carregados com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")

    print("####CHEGOU AQUI#####")
