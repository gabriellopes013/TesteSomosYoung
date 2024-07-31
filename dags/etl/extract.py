from airflow.hooks.base import BaseHook
from airflow.models import Variable
import json

def get_data():
    # Pega a conexão HTTP e lê o token do campo password
    conn = BaseHook.get_connection('api_connection')
    token = conn.password
    
    idahoy = Variable.get("idahoy", default_var=1811657)
    
    return json.dumps({
        "token": token,
        "idahoy": idahoy
    })