import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
    
    
def apresentacao(ax, title:str='', subtitle:str='', xlabel:str='', ylabel:str='', fonte:str='https://brasil.io/dataset/covid19/caso_full/', 
                 spines_invisible:list=['top', 'right'], kwargs_grid:dict={'axis':'y', 'alpha':0.6}):
    '''
    Função que plota as informações adicionais dos gráficos, título, subtítulo, rótulos, labels, fontes
    
    Parâmetros:
    ----------
    ax : eixo a ser plotado o gráfico, se nenhum for passado será criado automaticamnete, tipo : matplotlib.axes
    title : título do gráfico, tipo : str, padrão : ''
    subtitle : subtítulo do gráfico, tipo : str, padrão : ''
    xlabel : rótulo do eixo x, tipo : str, padrão : ''
    ylabel : rótulo do eixo y, tipo : str, padrão : ''
    fonte : fonte dos dados para ser plotada no gráfico(embaixo), tipo : str, padrão : 'https://brasil.io/dataset/covid19/caso_full/'
    spines_invisible : nome dos eixos a serem ocultados, tipo : list, padrão : ['top', 'right']
    kwargs_grid : argumentos a serem passados pra função matplotlib.pyplot.grid, tipo : dict, padrão : {'axis':'y', 'alpha':0.6}
    '''
    
    plt.sca(ax)
    plt.title(title + '\n', fontsize=25, loc='left', color='black')
    plt.text(0,1.03, subtitle, color='gray', transform=ax.transAxes, fontsize=15)
    plt.xlabel(xlabel, color='#333333', fontsize=15)
    plt.ylabel(ylabel, color='#333333', fontsize=15)
    plt.yticks(fontsize=15, color='#333333')
    plt.text(0,-0.1, f'fonte:{fonte}', color='gray', transform=ax.transAxes, fontsize=15)
    
    for spine in spines_invisible:
        ax.spines[spine].set_visible(False)
    plt.grid(**kwargs_grid)
    
def plot_time_series(df:pd.DataFrame, title:str='', subtitle:str='', xlabel:str='', ylabel:str='', show:bool=False, ax=None, month_freq:int=2, formatter_x=None, formatter_y=None,                   
                     fonte:str='https://brasil.io/dataset/covid19/caso_full/',spines_invisible:list=['top', 'right'], ylim:list=None, 
                     xlim:list=None, kwargs_grid:dict={'axis':'y', 'alpha':0.6}, **kwargs_lineplot):
    '''
    Função que plota uma série temporal com os dados relacionados ao tempo no eixo x e os dados numéricos no eixo y
    
    Parâmetros:
    ----------
    df : DataFrame do pandas a serem passados os gráfico, precisa ter 2 colunas, uma com dados do tipo datetime e outra com dados numéricos, tipo : pandas.DataFrame, argumento obrigatótio
    title : título do gráfico, tipo : str, padrão : ''
    subtitle : subtítulo do gráfico, tipo : str, padrão : ''
    xlabel : rótulo do eixo x, tipo : str, padrão : ''
    ylabel : rótulo do eixo y, tipo : str, padrão : ''
    show : valor lógico para mostrar ou não mostrar o gráfico, tipo : bool, padrão : False
    ax : eixo a ser plotado o gráfico, se nenhum for passado será criado automaticamnete, tipo : matplotlib.axes, padrão : None
    month_freq : inteiro correspondente ao intervalo entre os meses a serem plotados no eixo x, tipo : int, padrão : 2 
    fonte : fonte dos dados para ser plotada no gráfico(embaixo), tipo : str, padrão : 'https://brasil.io/dataset/covid19/caso_full/'
    spines_invisible : nome dos eixos a serem ocultados, tipo : list, padrão : ['top', 'right']
    ylim : lista indicando os limites do eixo y, tipo : list, padrão = None
    xlim : lista indicando os limites do eixo x, tipo : list, padrão = None
    kwargs_grid : argumentos a serem passados pra função matplotlib.pyplot.grid, tipo : dict, padrão : {'axis':'y', 'alpha':0.6}
    **kwargs_lineplot : argumentos adicionais a serem passados para função seaborn.lineplot
    
    Retorno:
    -------
    Retorna o eixo onde o gráfico foi criado
    OBS : se o argumento show for passado igual a True não retorna nada 
    '''
    if len(df.columns) != 2:
        raise TypeError('o dataframe precisa conter 2 colunas')
    
    try:
        df = df.rename(columns = {df.select_dtypes(include=['datetime']).columns[0] : 'date'})
    except IndexError:
        raise TypeError('o eixo x precisa ser do tipo datetime')
    try:
        df = df.rename(columns = {df.select_dtypes(include=['int64', 'float64']).columns[0] : 'y'})
    except IndexError:
        raise TypeError('o eixo y precisa ser do tipo int ou float')
    
    if ax is None: 
        fig, ax = plt.subplots()
    
    sns.lineplot(x='date', y='y', data=df, **kwargs_lineplot)
        
    #Plotando os títulos, mudando o tamanho e cores das fontes
    
    apresentacao(ax, title, subtitle, xlabel, ylabel, fonte, 
                 spines_invisible, kwargs_grid)
    
    mapa={'Jan':'Jan', 'Feb':'Fev', 'Mar':'Mar', 'Apr':'Abr', 'May':'Maio', 'Jun':'Jun', 'Jul':'Jul', 'Aug':'Ago', 'Sep':'Set','Oct':'Out',
         'Nov':'Nov','Dec':'Dez'}
    func = lambda mes: mes[:-3] + mapa[mes[-3:]]
    plt.xticks(pd.date_range(min(df['date']), max(df['date']), freq=f'{month_freq}MS'),
               pd.date_range(min(df['date']), max(df['date']), freq=f'{month_freq}MS').strftime('%Y-%b').map(func), 
               color='#333333', fontsize=15)
    
    plt.text(0,-0.1, f'fonte:{fonte}', color='gray', transform=ax.transAxes, fontsize=15)
    
    if formatter_x != None:
        ax.xaxis.set_major_formatter(formatter_x)
    
    if formatter_y != None:
        ax.yaxis.set_major_formatter(formatter_y)
    
    if xlim is not None:
        plt.xlim(xlim[0], xlim[1])
    if ylim is not None:
        plt.ylim(ylim[0], ylim[1])
    
    if show:
        plt.show()
    
    return ax

def thousand_formatter(x, pos):
    '''
    Função responsável por formatar um eixo do 'matplotlib' dividindo os valores por Mil, 
    mostrando duas casas decimais depois da vírgula e colocando a palavra 'Mil' após os valores indicando a grandeza,
    precisa ser passada como parâmetro para a função FuncFormatter do matplotlib.ticker
    '''
   
    return "%.2f Mil" % (x/1E3)

def million_formatter(x, pos):
    '''
    Função responsável por formatar um eixo do 'matplotlib' dividindo os valores por Milhão, 
    mostrando duas casas decimais depois da vírgula e colocando a palavra 'Mi' após os valores indicando a grandeza,
    precisa ser passada como parâmetro para a função FuncFormatter do matplotlib.ticker
    '''
    return "%.2f Mi" % (x/1E6)
                 
def percent_formatter(x, pos):
    '''
    Função responsável por formatar um eixo do 'matplotlib' transformando os valores em porcentagem,
    precisa ser passada como parâmetro para a função FuncFormatter do matplotlib.ticker
    '''
    return '{:.0%}'.format(x)
    



















