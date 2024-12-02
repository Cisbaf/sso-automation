import pandas as pd, re, unidecode
from src.bigquery.controller import get_connection, insert_data, get_last_update, get_last_insert
from datetime import date, timedelta

def clean_column_name(name):
    name = unidecode.unidecode(name)  # Remove acentos
    name = re.sub(r'\s+', '_', name)  # Substitui espaços por underlines
    name = re.sub(r'[^\w\s]', '', name)  # Remove caracteres especiais
    return name

def format_date(date: date):
    return date.strftime("%d/%m/%Y")

def treat_data(path_archive: str):
    # # Load the Excel file
    df = pd.read_excel(path_archive, keep_default_na=False, skipfooter=1, engine="openpyxl")

    # Clean column names
    df.columns = [clean_column_name(col) for col in df.columns]

    # Ensure IDADE and TOTAL are cast to integers, handle invalid values by coercing them to NaN
    df['IDADE'] = pd.to_numeric(df['IDADE'], errors='coerce')
    df['TOTAL'] = pd.to_numeric(df['TOTAL'], errors='coerce')
    # Converter a coluna 'data' para o formato datetime
    df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')

    # Se precisar converter para o formato UTC, você pode usar o seguinte
    df['DATA'] = df['DATA'].dt.tz_localize('UTC')

    last_date = df['DATA'].max()

    return df, last_date


def check_interval(client, diference: int):
    last_date = get_last_update(client)
    hoje = date.today()
    diferenca = abs((hoje - last_date).days)
    if diferenca >= diference:
        return True
    return False

def get_dates(client):
    last_insert = get_last_insert(client)
    first_date = last_insert + timedelta(days=1)
    second_date = last_insert + timedelta(days=3)
    return first_date, second_date
