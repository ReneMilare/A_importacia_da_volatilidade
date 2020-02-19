# A-importancia-da-volatilidade
<p>Projeto inspirado no vídeo do Leandro Guerra sobre a importância da volatilidade. Segue o link para o vídeo:
<link>https://www.youtube.com/watch?v=gZkH6m_P0-4&t=612s</link> </p>
<p>O dataset que resolvi usar é uma base que consegui na ActivTrades, que vai de: 
02/01/2005 até 17/02/2020 do ativo EURUSD, gráfico diário. </p>
<p>No vídeo o Leandro separa a base de treinamento de: 22/09/2009 até 31/12/2012, dando un tatal de 854 dias. 
Eu separei a base de treinamento de: 02/01/2005 até 31/12/2010, dando um total de 1867 dias.</p>
<li>A regressão do Leandro obteve a seguinte equação: <b>y = 39,002 x vol_10</b></li>
<li>Eu obtive a seguinte equação: <b>y = 35,22 x vol_10</b></li>
<li>O Leandro adotou como ponto de corte para o trade, o valor de <b>y = 0,342</b></li>
<li>Eu adotei <b>y = 0,301</b></li>
<p>Este valor de corte do y foi diferente pois resolvi dividir em mais partes as faixas de corte, 
como motra o trecho de código a seguir:<p/>
<p><b>cortes = dataset['regressao'][:1868].value_counts(bins=30,sort=False)</b></p>
<p>Note o parêmtro <b>bins</b> que recebe o valor de <b>30</b>, ou seja, foi divido em 30 partes a coluna chamada
regressão, já o Leandro dividiu em <b>20</b>, então foi tirado a soma de pontos que cada faixa continha. A figura a seguir mostra
uma parte dessa tabela, com a maior parte das somas dos pontos positivos destacada em amarelo:</p>

![soma_pips](https://user-images.githubusercontent.com/24875841/74861995-12f50200-532a-11ea-89b7-6e5593324fcd.PNG)

<p>Com a regra de trade foi montada:</p><p> <b>y <= 0,301 -> compra </p><p> y > 0,301 -> vende</b></p>
<p>O resultado acumulado ficou da seguinte forma:</p>

![acumulado](https://user-images.githubusercontent.com/24875841/74862433-e42b5b80-532a-11ea-863f-cf0b9e18fb09.PNG)

<p>Na pasta dados deixei o dataset que usei, e mais alguns do IBOV.</p>

<p>A planilha desenvolvida pelo Leandro pode ser encontrada pelo link: 
<link>https://www.outspokenmarket.com/blog/a-importancia-da-volatilidade</link></p>
