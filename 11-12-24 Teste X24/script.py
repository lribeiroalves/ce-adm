# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 12:44:19 2024

@author: lucas
"""

#%% Bibliotecas



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