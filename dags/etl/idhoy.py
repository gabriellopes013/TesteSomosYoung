from airflow.models import Variable

def idahoy():
    current_idahoy = int(Variable.get("idahoy"))
    new_idahoy = current_idahoy + 10
    Variable.set("idahoy", new_idahoy)
    