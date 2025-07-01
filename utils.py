import pandas as pd
import numpy as np
import plotly.express as px
import folium
from haversine import haversine

pd.set_option("display.max_columns", None)
pd.set_option('future.no_silent_downcasting', True)

def check_outliers(df):
    """
    Recebe um DataFrame e retorna um DataFrame com os outliers.
    Baseia-se no pressuposto de que os dados estão normalmente distribuídos.
    
    :param df: DataFrame a ser verificado
    """
    outliers_list = []
    # Itera sobre as colunas numéricas
    for column in df.select_dtypes(include=[np.number]).columns:
        # Calcula o 1 quartil (Q1)
        Q1 = df[column].quantile(0.25)
        # Calcula o 3 quartil (Q3)
        Q3 = df[column].quantile(0.75)
        # Calcula o Intervalo Interquartil (IQR)
        IQR = Q3 - Q1
        # Define os limites inferior e superior para outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        # Identifica os outliers da coluna atual e adiciona à lista
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        outliers_list.append(outliers)
    # Concatena todos os outliers identificados
    df_outliers = pd.concat(outliers_list).drop_duplicates().reset_index(drop=True)
    return df_outliers

def plot_correlation(df):
    """
    Plota uma heatmap de correlação para um DataFrame.
    
    :param df: DataFrame a ser analisado
    """
    correlation_matrix = df.select_dtypes(include=[np.number]).corr()
    fig = px.imshow(correlation_matrix,
                    title="Correlation Matrix",
                    labels={"x": "Features", "y": "Features"},
                    range_color=(-1, 1),
                    color_continuous_scale="RdBu")
    for i in range(len(correlation_matrix)):
        for j in range(len(correlation_matrix.columns)):
            fig.add_annotation(
                text=str(round(correlation_matrix.iat[i, j], 2)),
                x=i,
                y=j,
                showarrow=False,
                font=dict(color='black')
            )
    fig.update_layout(coloraxis_showscale=True, coloraxis_cmin=-1, coloraxis_cmax=1,
                    title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
                    xaxis={"title_font": {"size": 18}, "showgrid": True},
                    yaxis={"title_font": {"size": 18}, "showgrid": True})
    return fig

