# importa as bibliotecas
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv') # carrega o banco de dados
df['date'] = pd.to_datetime(df['date']) # coloca o tipo de dado da tabela 'date' para datatime
df.set_index(df['date']) # define a coluna 'date' como index

# Clean data
# filtra o dataset para tirar os valores extremos (maiores e menores que 2.5% do dataset)
df = df[(df['value'] > df['value'].quantile(0.025)) # pega os valores maiores que o limite inferior (2.5%)
        & (df['value'] < df['value'].quantile(0.975))] # pega os valores menores que o limite superior (97.5%) 


def draw_line_plot():
    # Draw line plot

    fig = plt.figure(figsize=(20,6)) # cria a figura e armazena ela na variável

    plt.plot(df.index, df['value'], color='red')  # cria o gráfico na figura com os valores do dataset e coloca a cor como vermelho
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019") # adiciona o título do gráfico
    plt.xlabel("Date") # adiciona o rótulo do eixo x
    plt.ylabel("Page Views") # adiciona o rótulo do eixo y

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png') # salva a imagem
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy() # faz uma cópia do dataset

    df_bar = df_bar.reset_index() # coluna 'date' deixa de ser índice e volta a ser coluna normal
    df_bar['year'] = df_bar['date'].dt.year # cria uma coluna de ano
    df_bar['month'] = df_bar['date'].dt.month # cria uma coluna de mês

    # Draw bar plot

    # pivot_table reorganiza o dataframe em uma tabela dinâmica 
    group = df_bar.pivot_table(
        index="year",    # define o eixo das linhas (cada linha representando um ano)
        columns="month", # define o eixo das colunas (cada coluna representando um mês)
        values="value",  # valores que vão preencher a tabela
        aggfunc="mean"   # calcula a média de 'value' para cada grupo de ano e mês -> função de agregação
    )

    fig = group.plot(
        kind="bar", # tipo de gráfico
        figsize=(12, 6), # tamanho da figura
        legend=True # exibe a legenda (True)
    )

    plt.xlabel("Years") # adiciona o rótulo do eixo x
    plt.ylabel("Average Page Views") # adiciona o rótulo do eixo y
    plt.legend(title="Months", labels=[ # legenda do gráfico
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ])

    # Save image and return fig (don't change this part)
    fig = fig.get_figure()
    fig.savefig('bar_plot.png') # salva a figura
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy() # faz uma cópia do dataset
    df_box = df_box.reset_index() # coluna 'date' deixa de ser índice e volta a ser coluna normal
    df_box['year'] = df_box['date'].dt.year # cria uma coluna de ano
    df_box['month'] = df_box['date'].dt.month # cria uma coluna de mês
    
    ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    df_box['month'] = pd.Categorical(
        df_box['month'],       # valores reais da coluna
        categories=ordered_months, # ordem correta
        ordered=True
    )

    df_box['month'] = df_box['date'].dt.strftime('%b') # converte os meses de números para o nome abreviado

    # com pd.Categorical é possível definir a ordem de uma lita/categorias
    df_box['month'] = pd.Categorical(
        df_box['month'], # valores da coluna
        categories=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        ordered=True # garante a ordem cronológica dos meses
    )

    # Draw box plots (using Seaborn)

    fig, axes = plt.subplots(1, 2, figsize=(15, 6)) # cria figura com dois conjuntos de eixos

    # cria o primeiro gráfico, na posição 0
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)") # título do gráfico
    axes[0].set_xlabel("Year") # rótulo do eixo x
    axes[0].set_ylabel("Page Views") # rótulo do eixo y

    # cria o segundo gráfico, na posição 1
    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)") # título do gráfico
    axes[1].set_xlabel("Month") # rótulo do eixo x
    axes[1].set_ylabel("Page Views") # rótulo do eixo y

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
