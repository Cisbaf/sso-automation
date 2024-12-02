from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime, date, timedelta
from src.bigquery.controller import get_last_insert

def teste():
    credentials = service_account.Credentials.from_service_account_file(
        'client.json',
        scopes=['https://www.googleapis.com/auth/bigquery']
    )
    client = bigquery.Client(credentials=credentials, project='integracaosheets-426313')
    query = f"""
        SELECT Dt_Atualizacao FROM `integracaosheets-426313.Portal_SAMU.Data Atualização`
    """
    query_job = client.query(query)
    for row in query_job.result():
        date = row[0]
        hoje = date.today()
        diferenca = abs((hoje - date).days)
        if diferenca >= 1:
            last_insert = get_last_insert(client)
            first_date = last_insert + timedelta(days=1)
            second_date = last_insert + timedelta(days=3)
            print('last', last_insert)
            print('first', first_date)
            print('last', second_date)
        # tres_dias_depois = date + timedelta(days=3)
        
        # print(date)
        # print(tres_dias_depois)


if __name__ == '__main__':
    teste()
    