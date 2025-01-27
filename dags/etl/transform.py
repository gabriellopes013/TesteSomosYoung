from airflow.models import Variable
import pandas as pd

def transform(**context):
    task_instance = context['ti']
    response = task_instance.xcom_pull(task_ids='extract_api')
    print(response)  
    df = pd.DataFrame(response)
    
    print("DataFrame:")
    print(df)
    print(df.count())
    return df