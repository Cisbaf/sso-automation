from config import date, path_all, path_temp, file_name
from src.dataanalise.analise import DataAnalysis
from download import relatorio, relatorio2, relatorio3, relatorio4, relatorio5, relatorio6, relatorio7
from download import relatorio8, relatorio9, GerenciadorRelatorios
from src.bigquery.helper import check_interval, get_connection, get_dates, format_date, treat_data, insert_data
import os

def automate():
    print("tentando executar?")
    credentials, client = get_connection()
    check = check_interval(client, 2)
    print("check?", check)
    if not check:
        return
    f, s = get_dates(client)
    date.clear()
    date.append(str(format_date(f)))
    date.append(str(format_date(s)))
    print("Datas", date)
    for archive in os.listdir(path_all):
        os.remove(f'{path_all}/{archive}')
    download_pt1 = GerenciadorRelatorios([
        relatorio, relatorio2, relatorio3, relatorio4
    ], path_temp)
    download_pt1.start()
    download_pt1.check()
    download_pt2 = GerenciadorRelatorios([
        relatorio5, relatorio6, relatorio7, relatorio8, relatorio9
    ], path_temp)
    download_pt2.start()
    download_pt2.check()
    if len(os.listdir(path_all)) != 9:
        raise Exception("Arquivos insuficientes!")
    analise = DataAnalysis(path_all)
    analise.load_dfs()
    total_columns = analise.joins_dfs2()
    if total_columns != 31:
        raise Exception("Quantidade de colunas insuficientes!")
    df, last_date = treat_data(f'{path_all}/{file_name}')
    insert_data(client, credentials, df, last_date)
