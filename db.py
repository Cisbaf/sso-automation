import pandas as pd, re, unidecode, os
from src.database.controller import RelatorioController, RelatoriosTeste
from config import path_all
import numpy as np


def clean_column_name(name):
    name = unidecode.unidecode(name)  # Remove acentos
    name = re.sub(r'\s+', '_', name)  # Substitui espaços por underlines
    name = re.sub(r'[^\w\s]', '', name)  # Remove caracteres especiais
    return name


def insert_from_excell(path):
    df = pd.read_excel(path, keep_default_na=False)
    df = df.fillna('#N/A')
    df.columns = [clean_column_name(col.lower()) for col in df.columns] # removendo espaço
    rows = df.shape[0]
    relatories = []
    err = False
    for i in range(rows - 1):
        row = df.iloc[i]
        row_dict = row.to_dict()
        RelatorioController.create_relatorio(RelatoriosTeste.fill(row_dict))
        try:
            relatories.append(RelatoriosTeste.fill(row_dict))
        except Exception as e:
            print(f'erro na linha {i} : {str(e)}')
            print(row_dict)
            err = True
        mult = i * 100
        por = int(mult / rows)
        os.system('clear')
        print(f'Verificando dados excell - Progresso ({i}/{rows}) {por}%')
    os.system('clear') 
    print(f'Verificação concluída, erros?: {err}')
    if not err:
        print('Inserindo dados no banco')
        RelatorioController.create_relatories(relatories)
        print("Dados Inseridos!")

insert_from_excell(f'{path_all}/finaldf3.xlsx')