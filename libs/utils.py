import pandas as pd
import numpy as np
import plotly.express as px
import plotly.subplots as ps
import folium
from haversine import haversine

pd.set_option("display.max_columns", None)
pd.set_option('future.no_silent_downcasting', True)

def check_outliers(df, bounds=1.5):
    """
    Receives a DataFrame and return another Dataframe with only outliers.
    Take as base the assumption that the data is normally distributed.
    
    :param df: DataFrame to be analyzed.
    :param bounds: Multiplier for IQR to determine outliers, smaller number means greater sensitivity.
    :return: DataFrame with outliers.
    """
    outliers_list = []
    # Loop through each numeric column in the DataFrame
    for column in df.select_dtypes(include=[np.number]).columns:
        # Calculate the 1 quartil (Q1)
        q1 = df[column].quantile(0.25)
        # Calculate the 3 quartil (Q3)
        q3 = df[column].quantile(0.75)
        # Calculate the Interquartile Range (IQR)
        iqr = q3 - q1
        # Define the upper and lower bounds for outliers
        lower_bound = q1 - bounds * iqr
        upper_bound = q3 + bounds * iqr
        # Identify the outliers and add them to the list
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        outliers_list.append(outliers)
    # Concatenate all outliers identified
    df_outliers = pd.concat(outliers_list).drop_duplicates().reset_index(drop=True)
    return df_outliers

def plot_histogram(df):
    """
    Plot a histogram for each numerical value in the given DataFrame.
    
    :param df: DataFrame to be analyzed.
    :return:Plotly figure object with histograms for each numerical column in the DataFrame.
    """
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    nrows = int(np.ceil(np.sqrt(len(numeric_columns))))
    ncols = int(np.ceil(len(numeric_columns) / nrows))
    fig = ps.make_subplots(rows=nrows, cols=ncols, subplot_titles=numeric_columns)
    for i, column in enumerate(numeric_columns):
        row_idx = (i // ncols) + 1
        col_idx = (i % ncols) + 1
        fig.add_trace(px.histogram(df, x=column).data[0], row=row_idx, col=col_idx)
    fig.update_layout(title={"text": "Numeric Columns", "x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
    return fig

def plot_correlation(df):
    """
    Plot a correlation matrix for the given DataFrame.
    
    :param df: DataFrame to be analysed.
    :return: Plotly figure object with the correlation matrix plot.
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

