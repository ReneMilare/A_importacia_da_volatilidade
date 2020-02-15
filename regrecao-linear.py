import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Importando dataser
dataset = pd.read_excel('EURUSD_Daily.xlsx')

# Criando a coluna de pips
dataset['pips'] = (dataset['Close'] - dataset['Open'])*10000

# Criando a coluna de alvo
for index, row in dataset.iterrows():
    if row['pips'] > 0:
        dataset.loc[index, 'alvo'] = 1
    else:
        dataset.loc[index, 'alvo'] = 0
    if index % 997:
        print('Criando a coluna alvo, {} de {} linhas'.format(index, len(dataset)))

# Criando a coluna de volatilidade de 10 períodos    
dataset['vol_10'] = dataset['Close'].rolling(window=11).std()

# Criando um data frame com a descrição dos dados
describe = dataset.describe()

# Preenchendo os valores faltantes com média da volatilidade de 10 períodos
dataset = dataset.fillna({'vol_10':describe['vol_10']['mean']})

# Capturando o tamanho do dataset (linhas)
size_dataset = len(dataset)

# Separando a base de teste e base de treinamento
x_train = dataset[['vol_10']][0:854]
x_test = dataset[['vol_10']][len(x_train):size_dataset]

y_train = dataset['alvo'][0:854]
y_test = dataset['alvo'][len(y_train):size_dataset]

# Inicializando o modelo de regressão linear, com o intercepto = 0
modelo = LinearRegression(fit_intercept=False)

# Treinando o modelo
modelo.fit(x_train, y_train)

# Criando a coluna de regressão linear
dataset['regressao'] = dataset['vol_10']*modelo.coef_

# Criando o agrupamento de valores da regressão
q = dataset['regressao'][0:854].value_counts(bins=20,sort=False)

# Fazendo a separação categorica de acordo com o agrupamento da regressão
dataset['faixa'] = pd.cut(dataset.regressao, q.index , include_lowest=True)

# Criando a tabela dinâmica entre regressão e pips
df = pd.pivot_table(dataset,index=['faixa'], values=['pips'], aggfunc=[np.sum])

# Criando a coluna com a regra de trade
for index, row in dataset.iterrows():
    if  row['regressao'] <= 0.394:
        dataset.loc[index, 'trade'] = dataset.loc[index,'pips']
    elif 0.394 < row['regressao']:
        dataset.loc[index, 'trade'] = -dataset.loc[index,'pips']
    else:
        dataset.loc[index, 'trade'] = 0
    if index % 997:
        print('Criando a coluna trade, {} de {} linhas'.format(index, len(dataset)))

# Criando a coluna de pips acumulado
for index, row in dataset.iterrows():
    if index == 0:
        dataset.loc[index, 'acumulado'] = dataset.loc[index, 'trade']
    else:
        dataset.loc[index, 'acumulado'] = dataset.loc[index, 'trade'] + dataset.loc[index-1, 'acumulado']
    if index % 997:
        print('Crindo a coluna acumulado, {} de {} linhas'.format(index, len(dataset)))

# Criando gráfico dos pontos acumulado
fig, ax = plt.subplots()
ax.plot(dataset['Time (CAT)'][0:854], dataset.acumulado[0:854], label = 'Treinamento')
ax.plot(dataset['Time (CAT)'][854:len(dataset)], dataset['acumulado'][854:len(dataset)], label='Teste')
ax = plt.title('EURUSD')
ax = plt.xlabel('Dias')
ax = plt.ylabel('Resultado acumulado')
ax = plt.legend()
plt.show()


print('y = {} . x'.format(modelo.coef_.round(2)))
