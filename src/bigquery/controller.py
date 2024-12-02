
from google.cloud import bigquery
from google.oauth2 import service_account
from pandas_gbq import to_gbq
from datetime import datetime, timezone


def get_connection():
    credentials = service_account.Credentials.from_service_account_file(
        'client.json',
        scopes=['https://www.googleapis.com/auth/bigquery']
    )
    client = bigquery.Client(credentials=credentials, project='integracaosheets-426313')
    return credentials, client

def insert_data(client, credentials, df, last):
    to_gbq(df,
        destination_table='integracaosheets-426313.Portal_SAMU.Base 2024',
        project_id='integracaosheets-426313',
        if_exists='append',
        credentials=credentials
    )

    # Atualizar a tabela Data Atualização
    client = bigquery.Client(credentials=credentials, project='integracaosheets-426313')
    
    dt_atualizacao = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    query = f"""
    UPDATE `integracaosheets-426313.Portal_SAMU.Data Atualização`
    SET Dt_Atualizacao = DATE('{dt_atualizacao}'), 
        Dt_Registro = DATE('{last}')
    WHERE TRUE -- Atualiza sempre a única linha existente
    """

    # Executar a query
    query_job = client.query(query)
    query_job.result() 


def get_last_update(client):
    query = f"""
        SELECT Dt_Atualizacao FROM `integracaosheets-426313.Portal_SAMU.Data Atualização`
    """
    query_job = client.query(query)
    for row in query_job.result():
        date = row[0]
        return date
    
def get_last_insert(client):
    query = f"""
        SELECT Dt_Registro FROM `integracaosheets-426313.Portal_SAMU.Data Atualização`
    """
    query_job = client.query(query)
    for row in query_job.result():
        date = row[0]
        return date
    