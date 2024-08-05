import requests
from dags.etl.testebd import data, headers
url = 'https://app.alunos.me/api/ahoy_viewer_ti'

response = requests.post(url, headers=headers,json=data)
print(response.json())
