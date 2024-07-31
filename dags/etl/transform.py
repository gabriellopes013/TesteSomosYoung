from airflow.models import Variable
import pandas as pd

def transform(**context):
    task_instance = context['ti']
    response = task_instance.xcom_pull(task_ids='extract_api')  
    df = pd.DataFrame(response)
    
    print("DataFrame:")
    print(df.head())
    
    # Atualiza a variável idahoy para o próximo lote
    current_idahoy = int(Variable.get("idahoy", default_var=1811657))
    new_idahoy = current_idahoy + 1000
    Variable.set("idahoy", new_idahoy)
    print(new_idahoy)
    
    return df