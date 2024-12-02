from celery import Celery
from celery.schedules import crontab
from config import date, path_all, path_temp, file_name
from src.dataanalise.analise import DataAnalysis
from download import relatorio, relatorio2, relatorio3, relatorio4, relatorio5, relatorio6, relatorio7
from download import relatorio8, relatorio9, GerenciadorRelatorios
from src.bigquery.helper import check_interval, get_connection, get_dates, format_date, treat_data, insert_data
import os

app = Celery('tasks', broker='redis://localhost:6379/0')

app.conf.result_backend = 'redis://localhost:6379/0'

app.conf.timezone = 'UTC'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(day_of_month='*/1', hour=8, minute=0),
        automate.s(),
    )

@app.task
def automate():
    credentials, client = get_connection()
    check = check_interval(client, 2)
    if not check:
        return
    f, s = get_dates(client)
    date.clear()
    date.append(str(format_date(f)))
    date.append(str(format_date(s)))
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
