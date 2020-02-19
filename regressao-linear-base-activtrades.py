import time
inicio = time.time()
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import math

# Importando dataset
dataset = pd.read_csv('dados/EURUSD_Daily_01.01.2005_17.02.2020.csv', sep='\t')

# Removendo colunas que não agregam nenhuma infromação
dataset = dataset.drop(columns=['<TICKVOL>','<VOL>', '<SPREAD>'], axis=1)

#Renomeando colunas para facilitar a manipulação do dataset
renomear = {
        '<DATE>':'date',
        '<OPEN>':'open',
        '<HIGH>':'high',
        '<LOW>':'low',
        '<CLOSE>':'close'        
        }
dataset = dataset.rename(columns = renomear)

# Criando a coluna de pips
for index, row in dataset.iterrows():
    if index + 1 >= len(dataset):
        dataset.loc[index, 'pips'] = 0
    else:
        dataset.loc[index, 'pips'] = (dataset.loc[index+1,'close']-dataset.loc[index+1, 'open'])*10000
    if index % 997:
        print('Criando a coluna pips, {} de {} linhas'.format(index, len(dataset)))

# Criando a coluna de alvo
for index, row in dataset.iterrows():
    if row['pips'] > 0:
        dataset.loc[index, 'alvo'] = 1
    else:
        dataset.loc[index, 'alvo'] = 0
    if index % 997:
        print('Criando a coluna alvo, {} de {} linhas'.format(index, len(dataset)))

# Criando a coluna de volatilidade de 10 períodos    
dataset['vol_10'] = dataset['close'].rolling(window=11).std()

# Preenchendo os valores faltantes com média da volatilidade de 10 períodos
dataset = dataset.fillna({'vol_10':dataset['vol_10'].mean()})

# Capturando o tamanho do dataset (linhas)
size_dataset = len(dataset)

# Separando a base de teste e base de treinamento
x_train = dataset[['vol_10']][:1868]
x_test = dataset[['vol_10']][1868:]

y_train = dataset['alvo'][:1868]
y_test = dataset['alvo'][1868:]

# Inicializando o modelo de regressão linear, com o intercepto = 0
modelo = LinearRegression(fit_intercept=False)

# Treinando o modelo
modelo.fit(x_train, y_train)
y_predict = modelo.predict(x_test)

# Criando a coluna de regressão linear
dataset['regressao'] = dataset['vol_10']*modelo.coef_

# Criando o agrupamento de valores da regressão
cortes = dataset['regressao'][:1868].value_counts(bins=20,sort=False)

# Fazendo a separação categorica de acordo com o agrupamento da regressão
dataset['faixa'] = pd.cut(dataset.regressao[:1868], cortes.index
       , include_lowest=True)

# Criando a tabela dinâmica entre regressão e pips
tabela = pd.pivot_table(dataset,index=['faixa'], values=['pips'], 
                        aggfunc=[np.sum])

# Criando a coluna com a regra de trade
for index, row in dataset.iterrows():
    if  row['regressao'] <= 0.301:
        dataset.loc[index, 'trade'] = dataset.loc[index,'pips']
    elif 0.301 < row['regressao']:
        dataset.loc[index, 'trade'] = -dataset.loc[index,'pips']
    else:
        dataset.loc[index, 'trade'] = 0
    if index % 997:
        print('Criando a coluna trade, {} de {} linhas'.format(index, 
              len(dataset)))

# Criando a coluna de pips acumulado
for index, row in dataset.iterrows():
    if index == 0:
        dataset.loc[index, 'acumulado'] = dataset.loc[index, 'trade']
    else:
        dataset.loc[index,'acumulado'] = dataset.loc[index,'trade'] + dataset.loc[index-1,'acumulado']
    if index % 997:
        print('Crindo a coluna acumulado, {} de {} linhas'.format(index, 
              len(dataset)))

# Criando gráfico dos pontos acumulado
fig, ax = plt.subplots()
ax.plot(dataset['date'][:1868], dataset.acumulado[:1868], label = 'Treinamento')
ax.plot(dataset['date'][1868:], dataset['acumulado'][1868:], label='Teste')
ax = plt.title('EURUSD')
ax = plt.xlabel('Dias')
ax = plt.ylabel('Resultado acumulado')
ax = plt.legend()
plt.savefig('teste.pdf', dpi=150)
plt.show()

# Regressão Linear fitada por seleção continua
print('y = {} vol_10'.format(modelo.coef_.round(2)))

fim = time.time()
tempo_execucao = (math.ceil(fim-inicio))/60
print(f'Tempo de execução do programa foi de aproximadamente {tempo_execucao} minutos')
