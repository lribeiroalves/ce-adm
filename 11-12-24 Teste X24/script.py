# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:44:19 2024

@author: lucas
"""

#%% Bibliotecas

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%% Preparação dos dados para importação

novas_linhas = []

# extrair todas as linhas do arquivo
with open('logCESala_asc.txt', 'r') as f:
    while True:
        linha = f.readline()
        if not linha:
            break
        
        # tratar a linha
        linha = linha.strip().split(' ')
        
        # identificar e ignorar pacotes corrompidos
        if len(linha) > 13:
            continue
        
        # tratar pacotes cortados
        if len(linha) < 13:
            prox_linha = f.readline()
            if not prox_linha:
                break
            prox_linha = prox_linha.strip().split(' ')
            linha = linha + prox_linha
                
        # construir nova lista com os pacotes tratados
        if len(linha) == 13 and linha[-1] == '44':
            novas_linhas.append(linha)


#%% Verificação das novas linhas

erros_linhas = []
for l in novas_linhas:
    if len(l) != 13:
        erros_linhas.append(l)
        
#%% Construção do arquivo csv

with open('dados.csv', 'w') as f:
    f.write('day,month,year,hour,minute,second,umid,temp,gX,gY,gZ,rssi\n')
    for l in novas_linhas:
        c = 0
        for i in l:
            f.write(i)
            c = c + 1
            if c < 12:
                f.write(',')
            else:
                f.write('\n')
                break
            
#%% Importação dos Dados

dados_brutos = pd.read_csv('dados.csv')
dados_brutos.info()

#%% Calculo da temperatura

dados_tratados = dados_brutos.assign(temp=dados_brutos['temp'] / 5)

#%% Calculo do RSSI

dados_tratados = dados_tratados.assign(rssi = lambda x: -1 * (256 - x.rssi))

#%% filtro de valores incorretos

dados_tratados = dados_tratados[dados_tratados['day'] <= 31]
dados_tratados = dados_tratados[dados_tratados['month'] <= 12]
dados_tratados = dados_tratados[dados_tratados['year'] == 2024]
dados_tratados = dados_tratados[dados_tratados['hour'] <= 24]
dados_tratados = dados_tratados[dados_tratados['minute'] <= 59]
dados_tratados = dados_tratados[dados_tratados['second'] <= 59]
dados_tratados = dados_tratados[dados_tratados['gX'] > 0]
dados_tratados = dados_tratados[dados_tratados['gY'] > 0]
dados_tratados = dados_tratados[dados_tratados['gZ'] > 0]

#%% Criação de coluna de Data

# Correção do ano
dados_tratados = dados_tratados.assign(year = dados_tratados.year + 2000)

# Coluna de Data
dados_tratados = dados_tratados.assign(date = pd.to_datetime(dados_tratados[['year', 'month', 'day', 'hour', 'minute', 'second']]))

dados_tratados[['year', 'month', 'day', 'hour', 'minute', 'second']].describe()

#%% Selecionar dados uteis

dados_uteis = dados_tratados[['date', 'temp', 'umid', 'gX', 'gY', 'gZ', 'rssi']]

dados_uteis[['gX', 'gY', 'gZ']].describe()

#%% Exibir resultados

plt.figure(figsize=(15,9), dpi=3000)
# sns.lineplot(data=dados_uteis, x='date', y='umid')
# sns.lineplot(data=dados_uteis, x='date', y='temp')
sns.lineplot(data=dados_uteis, x='date', y='gX')
sns.lineplot(data=dados_uteis, x='date', y='gY')
sns.lineplot(data=dados_uteis, x='date', y='gZ')
plt.show()
