# Análise Temporal COVID-19 Brasil
[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=flat-square&logo=Jupyter)](https://jupyter.org/try) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg?style=flat-square)](https://github.com/PedroHCAlmeida/analise_temporal_COVID_Brasil/edit/main/LICENSE)

![Alt](img/unnamed.jpg)

# Introdução 📜

Olá, meu nome é Pedro Henrique, e esse é meu repositório referente ao projeto final do módulo 3 do [Bootcamp De Data Science Aplicada](https://www.alura.com.br/bootcamp/data-science-aplicada/matriculas-abertas) promovido pela [Alura](https://www.alura.com.br/) sobre análise de séries temporais.O objetivo desse projeto foi analisar os dados de COVID-19 no Brasil ao longo do tempo, olhando para os dados coletados por dia da notificação e a partir disso encontrar padrões temporais que influenciam o comportamento desses dados.

# COVID-19

O ano de 2020 começou de uma maneira completamente inesperada, o mundo foi atingido por uma das maiores crises sanitárias da história contemporânea, fato esse que trouxe desafios e adversidades em todo o mundo, e no Brasil não foi diferente, a população viu, rapidamente, o perigo do vírus uma vez que as taxas de morte sobem cada vez mais.Esse projeto teve como motivação os problemas causados pela COVID-19 a fim de encontrar respostas do comportamento temporal da doença. 

# Estrutura do projeto
O repostório foi organizado em 3 pastas, são elas:

## [Dados brutos](https://github.com/PedroHCAlmeida/analise_temporal_COVID_Brasil/tree/main/dados_brutos):
Nesta pasta se encontra o arquivo .csv dos dados brutos extraídos do [Brasil.IO](https://brasil.io/home/) relacionados aos dados de casos e óbitos da COVID-19 no Brasil coletados a partir das secretarias estaduais de saúde. Esses dados estão organizados em 18 colunas, são elas:

* city : cidade
* city_ibge_code : código da cidade
* date : data das observações
* epidemiological_week : semana epidemiológica
* estimated_population : população estimada
* estimated_population_2019 : população estimada de 2019
* is_last : indica se os dados de relacionados ao last_avaiable são realmente os últimos
* is_repeated : se os valores são repeditos
* last_available_confirmed : última atualização do número total de casos confirmados
* last_available_confirmed_per_100k_inhabitants : última atualização do número total de casos confirmados por 100 mil habitantes
* last_available_date : data da última atualização
* last_available_death_rate : última atualização da taxa de mortes
* last_available_deaths : última atualização do número total de mortes confirmados
* order_for_place : número que identifica a ordem do registro para este local.
* place_type : tipo de local, estado ou cidade
* state : sigla do estado correspondente
* new_confirmed : casos novos notificados no dia
* new_deaths : óbitos novos notificados no dia

## [Dados limpos](https://github.com/PedroHCAlmeida/analise_temporal_COVID_Brasil/tree/main/dados_limpos):
Nesta pasta está o arquivo .csv com os dados na forma que serão utilizados na análise. Esses dados foram filtrados e tratados no notebook [Limpeza_dados_covid](https://github.com/PedroHCAlmeida/analise_temporal_COVID_Brasil/blob/main/notebooks/Limpeza_dados_covid.ipynb), esse arquivo está organizado em 7 colunas, são elas:

* date : data relacionada ao número de casos e óbitos
* casos_novos : número de casos notificados no dia
* obitos_novos : número de óbitos notificados no dia
* MM7_casos : média móvel de 7 dias dos casos novos
* MM7_obitos : média móvel de 7 dias dos casos novos
* mes/ano : mes e ano correspondentes
* letalidade_mes : número de óbitos totais do mês divididos pelo número de casos notificados no mês

## [Notebooks](https://github.com/PedroHCAlmeida/analise_temporal_COVID_Brasil/tree/main/notebooks):
Nesta pasta se encontram os notebooks desenvolvidos no jupyter e os arquivos .py destinados às funções e classes:

#### [Limpeza_dados_covid](https://github.com/PedroHCAlmeida/analise_temporal_COVID_Brasil/blob/main/notebooks/Limpeza_dados_covid.ipynb):
Esse notebook foi destinado à limpeza dos dados brutos a fim de agrupar os dados do Brasil inteiro e organizar por dia, além disso foram renomeadas as colunas e  algumas outras foram criadas:

* MM7_casos : média móvel de 7 dias dos casos novos
* MM7_obitos : média móvel de 7 dias dos casos novos
* mes/ano : mes e ano correspondentes
* letalidade_mes : número de óbitos totais do mês divididos pelo número de casos notificados no mês

#### [Análise Final]():
Nesse notebook teve como objetivo a análise dos dados de casos e óbitos por COVID-19 no Brasil inteiro e tentar encontrar padrões nesses dados ao longo do tempo.

#### [model.py]():
Nesse arquivo python está o código do modelo utilizado no notebook da análise final. 

#### [plot.py]():
Nesse arquivo python está o código das funções que tem como objetivo a geração de visualizar os dados.

#### [requirements.txt](https://github.com/PedroHCAlmeida/analise_temporal_COVID_Brasil/blob/main/notebooks/requirements.txt):
Nesse arquivo .txt estão as versões de todas as bibliotecas que foram utilizadas no projeto.

## [img](https://github.com/PedroHCAlmeida/analise_temporal_COVID_Brasil/tree/main/img):
Pasta destinada às imagens utilizadas no projeto.

# Tecnologias utilizadas 💻
Esse projeto foi realizado utilizando a linguagem Python versão 3.7.6 através do jupyter lab versão 1.2.6, as bibliotecas usadas foram:
* Pandas versão 1.2.4 : biblioteca rápida e poderosa usada para manipulação de dados
* Matplotlib versão 3.1.3 : biblioteca usada para visualização de dados
* Seaborn versão 0.11.1 : biblioteca baseada no Matplotlib para visualização de gráficos estatísticos mais complexos
* Numpy versão 1.20.2 : biblioteca utilizada para computação matemática
* fbprophet 0.7.1 : biblioteca focada na previsão de séries temporais
* Para mais informações de todas as versões utilizadas para replicação do projeto acesse o [requirements.txt](https://github.com/PedroHCAlmeida/analise_temporal_COVID_Brasil/blob/main/notebooks/requirements.txt)

# Hipóteses

* A média móvel de 7 dias de casos por dia em 2021 ultrapassou o pico de casos em 2020
* A média móvel de 7 dias de óbitos por dia em 2021 ultrapassou o pico de óbitos em 2020
* Existe uma sazonalidade semanal na notificação de casos novos
* Existe uma correlação entre o número de óbitos no dia e o número de casos em dias anteriores

# Modelo
O modelo teve como objetivo prever os números de casos novos por dia de COVID-19 no Brasil, a biblioteca fbprophet foi utilizada especificamente para previsão de séries temporais.

# Conclusões

A partir das análises dos dados foi possível concluir:

* Em 2021, a média móvel de óbitos conseguiu superar o pico de mortes de 2020 em diversos momentos
* Em 2021, a média móvel de casos novos também conseguiu superar o pico de casos novos de 2020
* Existe uma sazonalidade semanal na notificação dos casos, em que no Domingo e na Segunda esses números costumam cair
* Existe uma correlação entre os óbitos e os casos nos dias anteriores, principalmente nos mesmos dias da semana uma semana antes

# Contato ☎️

[<img src="https://img.shields.io/badge/pedrocorrea-0A66C2?style=flat-square&logo=linkedin&logoColor=white" />](https://www.linkedin.com/in/pedro-henrique-corrêa-de-almeida/)<br>
[<img src="https://img.shields.io/badge/GitHub-PedroHCAlmeida-DCDCDC?style=flat-square" />](https://github.com/PedroHCAlmeida)<br>
