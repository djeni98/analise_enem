#!/usr/bin/env python3

##### Arquivos necessários (entrada)
# dicionario.json
# categorias.json
# enem.csv

##### Arquivo de saída
# final.pkl.xz

#### Parâmetros
## Quantidade de linhas lidas em cada iteração
nrows = 10_000

## Rodar o programa em paralelo com 't' threads
t = 2
paralelo = True

def le_csv_partes(filename, cria_colunas=False, offset = 0, limit = None):
    import pandas as pd
    import json
    import re

    #### Pega informacoes sobre o dicionario e as categorias
    with open('dicionario.json', 'r') as f:
        d = json.load(f)

    with open('categorias.json', 'r') as f:
        c = json.load(f)
        categoria = {
            **c['participante'], **c['escola'], **c['especializado'], **c['especifico'],
            **c['recurso'], **c['local_prova'], **c['prova'], **c['redacao'], **c['socioeconomico']
        }

    #### Escolhe primeira leva de colunas, depois vai retirar outras colunas
    header = pd.read_csv(filename, sep=';', nrows=1, encoding='ISO-8859-1')
    meus_headers = (
        ~header.columns.str.startswith('CO') & ~header.columns.str.startswith('TX') &
        ~header.columns.str.match('Q01[3-9]|Q02[01]') & ~header.columns.str.startswith('NU_NOTA_COMP') &
        ~header.columns.str.startswith('NU_INSCRICAO') &
        ~header.columns.str.startswith('NU_ANO') &
        ~header.columns.str.endswith('_ESC') & ~header.columns.str.startswith('TP_PRESENCA')
    )
    mantem_header = list(header.columns.where(meus_headers).dropna())

    #### Colunas que serao juntadas em uma só
    especializado = list(d['especializado'].keys())
    especifico = list(d['especifico'].keys())
    recurso = list(d['recurso'].keys())

    #### Colunas que vão ser mantidas no final
    mantem_final = list(header.columns.where(
        meus_headers &
        ~header.columns.isin(especializado) & ~header.columns.isin(especifico) &
        ~header.columns.isin(recurso)
    ).dropna())

    recurso.remove('IN_SEM_RECURSO')

    #### Tipo das Categorias
    dict_categoria = { coluna: pd.CategoricalDtype(
            categories=[ int(item) if item.isdigit() else item for item in list(categoria[coluna]) ],
            ordered=bool(re.match('Q00[5-9]|Q0[12][0-9]', coluna))
        ) for coluna in categoria if coluna in mantem_final
    }

    lines = offset+1
    len_df = nrows
    final_dfs = []
    csv_iter = pd.read_csv(
        filename, sep=';',
        skiprows=lines,
        nrows=limit-offset if limit is not None else None,
        encoding='ISO-8859-1',
        header=None,
        names=list(header.columns),
        usecols=(mantem_header if cria_colunas else mantem_final),
        iterator=True
    )
    while True:
        try:
            df = csv_iter.get_chunk(nrows)
        except StopIteration:
            break

        ### Trocar int64 e float64 por 32bits
        df = df.astype({ c: 'int32' for c in df.select_dtypes(include=['int64']).columns })
        df = df.astype({ c: 'float32' for c in df.select_dtypes(include=['float64']).columns })

        mask_df_sem_notas_zero = (
            df[['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']]
                .notnull()
                .agg(lambda x: x.any(), axis='columns')
        )
        df = (
            df
            ## Troca o tipo das categorias
            .astype(dict_categoria)
            ## Remove linhas com todas as notas zero
            [mask_df_sem_notas_zero]
        )

        ### Colunas juntadas
        if cria_colunas:
            series_especializado = df[especializado].agg(lambda x: x.any(), axis='columns')
            series_especializado.name = 'IN_ESPECIALIZADO'
            series_especifico = df[especifico].agg(lambda x: x.any(), axis='columns')
            series_especifico.name = 'IN_ESPECIFICO'
            series_recurso = df[recurso].agg(lambda x: x.any(), axis='columns')
            series_recurso.name = 'IN_RECURSO'
            df = df[mantem_final].join(series_especializado).join(series_especifico).join(series_recurso)
        else:
            df = df[mantem_final]

        final_dfs.append(df)

    print('Ok')
    return pd.concat(final_dfs)

def wrapper(x):
    return le_csv_partes(*x)

if __name__ == '__main__':
    from datetime import datetime
    from pandas import Timedelta, concat
    from multiprocessing import Pool
    from itertools import zip_longest
    from pprint import pprint

    inicio = datetime.now()
    if paralelo:
        print(f'Rodando em Paralelo com {t} threads')
        with Pool(t) as p:
            x = 5_100_000 // t
            args = [ ('enem.csv', True, i, j) for i, j in zip_longest(range(0, x*t, x), range(x, x*t, x)) ]
            pprint(args)
            arr = p.map(wrapper, args)
            df = concat(arr)
    else:
        print('Rodando Sequencial')
        df = le_csv_partes('enem.csv', True, 0, None)

    print(Timedelta(datetime.now() - inicio).isoformat())
    print(len(df))

    inicio = datetime.now()
    print('Criando arquivo pickle')
    df.to_pickle('final.pkl.xz')
    print(Timedelta(datetime.now() - inicio).isoformat())
