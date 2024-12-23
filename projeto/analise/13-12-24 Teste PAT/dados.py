# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 16:08:02 2024

@author: lucas
"""

#%% Importar bibliotecas

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% Importar Dataframe

dados_brutos = pd.read_csv('texto.csv')

dados_brutos.describe()
dados_brutos.info()

#%% Renomear variáveis

nomes_colunas = {'ano': 'year', 'mes': 'month', 'dia': 'day', 'hora': 'hour', 'minuto': 'minute', 'segundo': 'second', 'temperatura': 'temp', 'umidade': 'umid'}
dados_tratados = dados_brutos.rename(columns=nomes_colunas)

#%% Correção da Temperatura

dados_tratados = dados_tratados.assign(temp = lambda x: x.temp / 5)

#%% Formatação de Data

# correção de ano
dados_tratados = dados_tratados.assign(year=dados_tratados['year'] + 2000)

dados_tratados = dados_tratados.assign(date = pd.to_datetime(dados_tratados[['year', 'month', 'day', 'hour', 'minute', 'second']]))

dados_tratados[['year', 'month', 'day', 'hour', 'minute', 'second']]

#%% Dados Tratados

dados_uteis = dados_tratados.drop(columns = ['year', 'month', 'day', 'hour', 'minute', 'second'])

dados_uteis.info()
dados_uteis.describe()

#%% Gráficos

plt.figure(figsize=(15,9), dpi=600)
# sns.lineplot(data=dados_uteis, x='date', y='umid')
# sns.lineplot(data=dados_uteis, x='date', y='temp')
sns.lineplot(data=dados_uteis, x='date', y='gX')
sns.lineplot(data=dados_uteis, x='date', y='gY')
sns.lineplot(data=dados_uteis, x='date', y='gZ')
plt.show()
