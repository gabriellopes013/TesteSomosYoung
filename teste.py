from sqlalchemy import create_engine
import pandas as pd

# Dados de conexão
user = 'teste'
password = 'teste'
host = 'localhost'
port = '5437'
database = 'data'

# Cria a string de conexão
connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

# Cria o engine de conexão
engine = create_engine(connection_string)

# Testa a conexão
try:
    with engine.connect() as connection:
        print("Conexão bem-sucedida!")
        # Testa a execução de uma consulta simples
        df = pd.read_sql('SELECT NOW()', connection)
        print(df)
except Exception as e:
    print(f"Erro ao conectar: {e}")