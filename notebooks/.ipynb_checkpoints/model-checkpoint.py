from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot, plot_cross_validation_metric
from fbprophet.diagnostics import cross_validation, performance_metrics
from plot import plot_time_series, apresentacao
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mlt

class Modelo_prophet_semanal:
    '''
    Parâmetros Construtor:
    ---------------------
    dados : DataFrame com duas colunas de nome 'ds'(tipo datetime) e 'y'(tipo int ou float)
    teste_periodo : número inteiro representando o número de dias destinado para o teste
    **Kwargs_model : argumentos adicionais passados para a classe fbprophet.Prophet na hora de criar o modelo
    
    Atributos:
    ---------
    Definidos no construtor:
    -----------------------
        treino : dataset destinado aos dados de treino
        teste : dataset destinado aos dados de teste
        modelo : modelo do tipo fbprophet.Prophet
        previsao : previsao do modelo sobre dados de treino e teste
        
    Definido pela função c_valid():
    ------------------------------
        cross : DataFrame com os dados da validação cruzada
    
    Definido pela função metricas():
    -------------------------------
        metricas : Dataframe com as métricas da validação cruzada 
    
    Funções:
    -------
    __init__() : construtor da classe que define os dados de treino, teste e o modelo como atributos do objeto, adiciona os regressores, treina o modelo e faz a previsao para todos os dados
    c_valid() : realiza a validação cruzada do modelo através da função fbprophet.diagnostics.cross_validation
    metricas() : calcula as métricas da validação cruzada através da função fbprophet.diagnostics.performance_metrics
    plota() : função que plota a previsão com os dados de treino e teste
    plot_cross_validation() : chama a função plot_cross_validation_metric do fbprophet.plot
    '''
    
    def __init__(self, dados:pd.DataFrame, teste_periodo:int=0, holiday=False, pais:str='BR', regressors=[], **kwargs_model):
        '''
        Construtor da classe que define os dados de treino, teste e o modelo como atributos do objeto
        
        Parâmetros:
        ----------
        dados : DataFrame com os dados de treino e teste com as colunas de data('ds') e a coluna a ser prevista('y'), tipo : pd.DataFrame
        teste_periodo : quantidade de dias que será reservado para os dados de treino, tipo : int
        pais : pais correspondente aos dados para serem adicionados os feriados, tipo : str
        **kwargs_model : argumentos adicionais que serão passados para o modelo fbprophet.Prophet 
        '''
        self.treino = dados[:len(dados) - teste_periodo]
        self.teste = dados[len(dados) - teste_periodo:]
        self.modelo = Prophet(daily_seasonality=False, yearly_seasonality=False, **kwargs_model)
        
        if holiday == True:
            self.modelo.add_country_holidays(country_name=pais)
            
        for regressor in regressors:
            if regressor not in dados.columns:
                raise ValueError('A coluna passada como regressor não foi encontrada nos dados passados')
            self.modelo.add_regressor(regressor)
            
        self.modelo.fit(self.treino)
        
        dados_prever = dados.drop(columns='y')
        self.previsao = self.modelo.predict(dados_prever)
        
    def c_valid(self, **kwargs_cross_validation):
        '''
        Função responsável por realizar a validação cruzada
        
        Parâmetros:
        ----------
        **kwargs_cross_validation : argumentos adicionais para serem passados na função fbprophet.diagnostics.cross_validation
        '''
        self.cross = cross_validation(self.modelo, **kwargs_cross_validation)

    def metricas(self, metrics=['rmse', 'mae'], diff_rmse_mae=True, margins_mean=True, **kwargs_metricas):
        '''
        Função que calcula as métricas da validação cruzada através da função fbprophet.diagnostics.performance_metrics
        '''
        self.metricas = performance_metrics(self.cross, metrics=metrics, **kwargs_metricas)
        
        if margins_mean == True:
            self.metricas['media_metricas'] = self.metricas.mean(axis=1)
            mean_row = self.metricas.mean()
            mean_row = mean_row.to_frame().T
            mean_row['horizon'] = np.nan
            mean_row.index = ['media']
            self.metricas = self.metricas.append(mean_row)
            
        if diff_rmse_mae == True and 'rmse' in metrics and 'mae' in metrics:
            self.metricas['diff_rmse_mae'] = abs(self.metricas['rmse'] - self.metricas['mae'])
    
    def plota(self, title:str='', subtitle:str='', xlabel:str='', ylabel:str='', 
              teste:bool=True, ax=None, show:bool=False,
              month_freq:int=2, kwargs_modeloplot:dict={}, 
              kwargs_testeplot:dict={'marker':'.', 'color':'red', 'linestyle':'', 'markersize':8}):
        '''
        Função que plota os resultados do modelo e dos dados reais de treino e teste
        
        Parâmetros:
        ----------
        title : título do gráfico, tipo : str, padrão : ''
        subtitle : subtítulo do gráfico, tipo : str, padrão : ''
        xlabel : rótulo do eixo x, tipo : str, padrão : ''
        ylabel : rótulo do eixo y, tipo : str, padrão : ''
        teste : valor lógico para decidir se os dados de teste serão plotados no gráfico, tipo : bool, padrão : True
        show : valor lógico para mostrar ou não mostrar o gráfico, tipo : bool, padrão : False
        ax : eixo a ser plotado o gráfico, se nenhum for passado será criado automaticamnete, tipo : matplotlib.axes, padrão : None
        month_freq : inteiro correspondente ao intervalo entre os meses a serem plotados no eixo x, tipo : int, padrão : 2
        kwargs_modeloplot : dicionário com os argumentos para serem passados pra função fbprophet.Prophet.plot, tipo : dict, padrão : {}
        kwargs_testeplot : dicionário com os argumentos para serem passados pra função seaborn.lineplot, tipo : dict, padrão :{'marker':'.', 'color':'red', 'linestyle':'', 'markersize':8} 
        
        Retorno:
        -------
        Retorna o eixo onde o gráfico foi criado
        OBS : se o argumento show for passado igual a True não retorna nada 
        '''
        if ax is None:
            fig, ax = plt.subplots(figsize=(20,10))
        
        if len(self.previsao) == 0:
            raise ValueError()
        self.modelo.plot(self.previsao, ax=ax, **kwargs_modeloplot)
        
        plt.sca(ax)
        if len(self.teste) > 0:
            plot_time_series(self.teste, title=title, subtitle=subtitle, xlabel=xlabel, ylabel=ylabel, \
                             ax=ax, month_freq=month_freq, **kwargs_testeplot)
            plt.xticks(pd.date_range(min(self.treino['ds']), max(self.teste['ds']), freq=f'{month_freq}MS'),\
                       pd.date_range(min(self.treino['ds']), max(self.teste['ds']), freq=f'{month_freq}MS').strftime('%Y-%b'), color='#333333')
        else:
            plt.xticks(pd.date_range(min(self.treino['ds']), max(self.treino['ds']), freq=f'{month_freq}MS'),
                       pd.date_range(min(self.treino['ds']), max(self.treino['ds']), freq=f'{month_freq}MS').strftime('%Y-%b'), color='#333333')
            apresentacao(ax,title,subtitle,xlabel,ylabel)
            
        if show is True:
            plt.show()
            
        else:
            return ax
    
    def plot_cross_validation(self, janela:list=[0], metric:str='rmse'):
        
        if len(self.cross) == 0:
            raise ValueError('a validação cruzada não foi definida, chame a função c_valid primeiramente')
        if type(janela) != list:
            raise TypeError('o parâmetro janela deve ser uma lista')
        
        cutoff = self.cross['cutoff'].unique()[janela]
        df_cv_cut = self.cross[self.cross['cutoff'].isin(cutoff)]
        plot_cross_validation_metric(df_cv_cut, metric)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        