from .utils import pd, np, haversine
import plotly.express as px
import plotly.subplots as ps
import folium
from folium.plugins import HeatMap

def get_metrics_company(df: pd.DataFrame):
    """
    This function processes the DataFrame to compute several company key metrics:
    - Number of unique restaurants.
    - Mean number of orders per restaurant.
    - Number of unique delivery services.
    - Mean number of deliveries per delivery service.
    - Total number of deliveries.
    - Maximum number of deliveries in a single week.
    - Minimum number of deliveries in a single week.
    - Mean number of deliveries per week.
    - Standard deviation of the number of deliveries per week.
    - Mean difference in the number of deliveries between consecutive weeks.

    :param df: DataFrame containing the dataset with "ID", "Restaurant_location", "Delivery_person_ID", and "Day_Ordered" columns.
    :return: Dictionary containing the calculated metrics.
    """
    metrics = {}
    df_aux = df[["ID", "Restaurant_location"]].groupby("Restaurant_location").count().reset_index()
    metrics["restaurants"] = df_aux["Restaurant_location"].nunique()
    metrics["mean_orders_per_restaurant"] = df_aux["ID"].mean()
    df_aux = df[["Delivery_service_ID", "ID"]].groupby("Delivery_service_ID").count().reset_index()
    metrics["delivery_services"] = df_aux["Delivery_service_ID"].nunique()
    metrics["mean_deliveries_per_service"] = df_aux["ID"].mean()
    df_aux = df
    df["Day_Ordered"] = pd.to_datetime(df["Time_Ordered"]).dt.date
    df_aux["Week_Ordered"] = pd.to_datetime(df_aux["Day_Ordered"]).dt.strftime("%W").astype(int)
    df_aux = df_aux[["Week_Ordered", "ID"]].pivot_table(index="Week_Ordered", aggfunc="count").reset_index()
    all_weeks = pd.DataFrame({"Week_Ordered": range(df_aux["Week_Ordered"].min(), df_aux["Week_Ordered"].max() + 1)})
    df_aux = pd.merge(all_weeks, df_aux, on="Week_Ordered", how="left").fillna(0)
    metrics["total_deliveries"] = df_aux["ID"].sum()
    metrics["week_max_deliveries"] = df_aux["ID"].max()
    metrics["week_min_deliveries"] = df_aux["ID"].min()
    metrics["week_mean_deliveries"] = df_aux["ID"].mean()
    metrics["week_std_dev_deliveries"] = df_aux["ID"].std()
    metrics["week_mean_diff_deliveries"] = df_aux["ID"].diff().mean()
    return metrics

def get_metrics_deliveries(df: pd.DataFrame):
    """
    This function processes the DataFrame to compute several delivery-related metrics:
    - Minimum delivery person rating.
    - Maximum delivery person rating.
    - Mean delivery person rating.
    - Standard deviation of delivery person ratings.
    - Mean delivery distance.

    :param df: DataFrame containing the dataset with "Delivery_person_Ratings" column.
    :return: Dictionary containing the calculated metrics.
    """
    metrics = {}
    metrics["ratings_min"] = df["Delivery_person_Ratings"].min()
    metrics["ratings_max"] = df["Delivery_person_Ratings"].max()
    metrics["ratings_mean"] = df["Delivery_person_Ratings"].mean()
    metrics["ratings_std_dev"] = df["Delivery_person_Ratings"].std()
    metrics["mean_delivery_distance"] = df.apply(lambda x: haversine(x["Restaurant_location"], x["Delivery_location"]), axis=1).mean()
    return metrics

def get_metrics_restaurants(df: pd.DataFrame):
    """
    This function processes the DataFrame to compute several restaurant-related metrics:
    - Maximum pick-up time in minutes.
    - Minimum pick-up time in minutes.
    - Mean pick-up time in minutes.
    - Standard deviation of pick-up times in minutes.

    :param df: DataFrame containing the dataset with "Pick_time(min)" column.
    :return: Dictionary containing the calculated metrics.
    """
    metrics = {}
    metrics["Pick_time_max"] = df["Pick_time(min)"].max()
    metrics["Pick_time_min"] = df["Pick_time(min)"].min()
    metrics["Pick_time_mean"] = df["Pick_time(min)"].mean()
    metrics["Pick_time_std_dev"] = df["Pick_time(min)"].std()
    return metrics

def get_mean_ratings_by_service(df: pd.DataFrame):
    """
    This function processes the DataFrame to calculate the mean rating for each delivery person.
    It groups the data by delivery person ID, computes the mean rating for each person,
    sorts the results by rating in descending order, and renames the column to "Mean_rating".
    The index is then reset and incremented by 1 for better readability.

    :param df: DataFrame containing the dataset with "Delivery_person_ID" and "Delivery_person_Ratings" columns.
    :return: DataFrame with the mean rating for each delivery person, sorted by rating in descending order.
    """
    df = df[["Delivery_service_ID", "Delivery_person_Ratings"]].groupby("Delivery_service_ID").mean().round(2).sort_values(by="Delivery_person_Ratings", ascending=False).rename(columns={"Delivery_person_Ratings": "Mean_rating"}).reset_index()
    df.index = df.index +1
    return df

def get_means_ratings_by_traffic(df: pd.DataFrame):
    """
    This function processes the DataFrame to calculate the mean and standard deviation of delivery person ratings
    for each traffic density category. It groups the data by traffic density, computes the mean and standard deviation
    of ratings for each category, and then resets the index for better readability.

    :param df: DataFrame containing the dataset with "Delivery_person_Ratings" and "Road_traffic_density" columns.
    :return: DataFrame with the mean and standard deviation of delivery person ratings for each traffic density category.
    """
    df = df[["Delivery_person_Ratings", "Road_traffic_density"]].groupby("Road_traffic_density").agg({"Delivery_person_Ratings": ["mean", "std"]})
    df.columns = ["Mean_Rating", "Std_Rating"]
    df.reset_index(inplace=True)
    df.index = df.index +1
    return df

def get_mean_ratings_by_weather(df: pd.DataFrame):
    """
    This function processes the DataFrame to calculate the mean and standard deviation of delivery person ratings
    for each weather condition category. It groups the data by weather condition, computes the mean and standard deviation
    of ratings for each category, and then resets the index for better readability.

    :param df: DataFrame containing the dataset with "Delivery_person_Ratings" and "Weatherconditions" columns.
    :return: DataFrame with the mean and standard deviation of delivery person ratings for each weather condition category.
    """
    df = df[["Delivery_person_Ratings", "Weatherconditions"]].groupby("Weatherconditions").agg({"Delivery_person_Ratings": ["mean", "std"]})
    df.columns = ["Mean_Rating", "Std_Rating"]
    df.reset_index(inplace=True)
    df.index = df.index +1
    return df

def get_top_10_fastest_deliveries(df: pd.DataFrame, reverse: bool=False):
    """
    This function processes the DataFrame to calculate the mean velocity for each delivery person,
    sorts the results by velocity in either ascending or descending order based on the 'reverse' parameter,
    and returns the top 10 fastest delivery persons. 
    This means that if the reverse parameter is set to "True", the function will return the top 10 slowest delivery persons.

    :param df: DataFrame containing the dataset with "Delivery_person_ID" and "Velocity(km/h)" columns.
    :param reverse: Boolean flag to determine the sorting order. If True, sorts in ascending order; if False, sorts in descending order.
    :return: DataFrame with the top 10 delivery persons sorted by their mean velocity.
    """
    df = df[["Delivery_service_ID", "Velocity(km/h)"]].groupby("Delivery_service_ID").mean().sort_values("Velocity(km/h)", ascending=reverse).reset_index()
    df = df.head(10).reset_index(drop=True)
    df.index = df.index +1
    return df

def get_mean_pick_time_by_city(df: pd.DataFrame):
    """
    This function processes the DataFrame to calculate the mean and standard deviation of pick-up times
    for each city. It groups the data by city, computes the mean and standard deviation of pick-up times
    for each city, and then resets the index for better readability.

    :param df: DataFrame containing the dataset with "Pick_time(min)" and "City" columns.
    :return: DataFrame with the mean and standard deviation of pick-up times for each city.
    """
    df = df[["Pick_time(min)", "City"]].groupby("City").agg(["mean", "std"]).reset_index()
    df.columns = ["City", "Mean_time", "Std_time"]
    return df

def get_mean_pick_time_by_order(df: pd.DataFrame):
    """
    This function processes the DataFrame to calculate the mean and standard deviation of pick-up times
    for each type of order. It groups the data by order type, computes the mean and standard deviation of
    pick-up times for each type, and then resets the index for better readability.

    :param df: DataFrame containing the dataset with "Pick_time(min)" and "Type_of_order" columns.
    :return: DataFrame with the mean and standard deviation of pick-up times for each type of order.
    """
    df = df[["Pick_time(min)", "Type_of_order"]].groupby(["Type_of_order"]).agg(["mean", "std"]).reset_index()
    df.columns = ["Type_of_order", "Mean_time", "Std_time"]
    return df

def get_mean_pick_time_by_traffic(df: pd.DataFrame):
    """
    This function processes the DataFrame to calculate the mean and standard deviation of pick-up times
    for each traffic density category. It groups the data by traffic density, computes the mean and standard deviation
    of pick-up times for each category, and then resets the index for better readability.

    :param df: DataFrame containing the dataset with "Pick_time(min)" and "Road_traffic_density" columns.
    :return: DataFrame with the mean and standard deviation of pick-up times for each traffic density category.
    """
    df = df[["Pick_time(min)", "Road_traffic_density"]].groupby(["Road_traffic_density"]).agg(["mean", "std"]).reset_index()
    df.columns = ["Road_traffic_density", "Mean_time", "Std_time"]
    return df

def plot_histogram(df: pd.DataFrame):
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

def plot_correlation(df: pd.DataFrame):
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
                font=dict(color="black")
            )
    fig.update_layout(coloraxis_showscale=True, coloraxis_cmin=-1, coloraxis_cmax=1,
                    title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
                    xaxis={"title_font": {"size": 18}, "showgrid": True},
                    yaxis={"title_font": {"size": 18}, "showgrid": True})
    return fig

def plot_orders_per_day(df: pd.DataFrame):
    """
    This function processes the cleaned DataFrame to extract the date of each order,
    counts the number of orders per day, and then plots these counts using a bar chart.
    
    :param df_clear: DataFrame containing the cleaned dataset with a "Time_Ordered" column.
    :return: Plotly figure object with the bar chart showing the number of orders per day.
    """
    df["Day_Ordered"] = pd.to_datetime(df["Time_Ordered"]).dt.date
    df = df[["ID", "Day_Ordered"]].groupby("Day_Ordered").count().reset_index()
    df = df[["Day_Ordered", "ID"]].pivot_table(index="Day_Ordered", aggfunc="sum").reset_index()
    fig = px.bar(df, x="Day_Ordered", y="ID", title="Daily orders", labels={"Day_Ordered": "Date", "ID": "Quantity"})
    fig.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
        xaxis={"title_font": {"size": 18}, "showgrid": True},
        yaxis={"title_font": {"size": 18}, "showgrid": True})
    return fig

def plot_orders_per_week(df: pd.DataFrame):
    """
    This function processes the DataFrame to extract the week number for each order,
    counts the number of orders per week, and then plots these counts using a line chart.

    :param df: DataFrame containing the dataset with a "Day_Ordered" column.
    :return: A tuple containing:
        - Plotly figure object with the line chart showing the number of orders per week.
    """
    df["Day_Ordered"] = pd.to_datetime(df["Time_Ordered"]).dt.date
    df["Week_Ordered"] = pd.to_datetime(df["Day_Ordered"]).dt.strftime("%W").astype(int)
    df = df[["Week_Ordered", "ID"]].pivot_table(index="Week_Ordered", aggfunc="count").reset_index()
    all_weeks = pd.DataFrame({"Week_Ordered": range(df["Week_Ordered"].min(), df["Week_Ordered"].max() + 1)})
    df = pd.merge(all_weeks, df, on="Week_Ordered", how="left").fillna(0)
    fig = px.line(df, x="Week_Ordered", y="ID", title="Weekly orders", labels={"Week_Ordered": "Week of the year", "ID": "Quantity"}, markers=True)
    fig.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
        xaxis={"title_font": {"size": 18}, "showgrid": True},
        yaxis={"title_font": {"size": 18}, "showgrid": True})
    return fig

def plot_orders_by_traffic(df: pd.DataFrame):
    """
    This function processes the DataFrame to count the number of orders for each traffic density category,
    calculates the percentage of orders for each category, and then plots these percentages using a pie chart.

    :param df: DataFrame containing the dataset with an "ID" column and a "Road_traffic_density" column.
    :return: Plotly figure object with the pie chart showing the distribution of orders by traffic density.
    """
    df = df[["ID", "Road_traffic_density"]].groupby("Road_traffic_density").count().reset_index()
    df["percent"] = df["ID"] / df["ID"].sum()
    fig = px.pie(df, values="percent", names="Road_traffic_density", title="Orders distribution by traffic density")
    fig.update_layout(width=700, height=600,
        title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
        legend={"font": {"size": 18}})
    return fig

def plot_orders_by_traffic_and_city_type(df: pd.DataFrame):
    """
    This function processes the DataFrame to count the number of orders for each combination of city type and traffic density,
    and then plots these counts using a stacked bar chart.

    :param df: DataFrame containing the dataset with "ID", "City", and "Road_traffic_density" columns.
    :return: Plotly figure object with the stacked bar chart showing the distribution of orders by city type and traffic density.
    """
    df = df[["ID", "City", "Road_traffic_density"]].groupby(["City", "Road_traffic_density"]).count().reset_index()
    fig = px.bar(df, x="City", y="ID", color="Road_traffic_density", title="Orders by city type grouped by traffic density", labels={"City": "City type", "ID": "Quantity", "Road_traffic_density": "Traffic"}, barmode="stack", log_y=True)
    fig.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
        xaxis={"title_font": {"size": 18}, "showgrid": True},
        yaxis={"title_font": {"size": 18}, "showgrid": True})
    return fig

def plot_weekly_orders_per_service(df: pd.DataFrame):
    """
    This function processes the DataFrame to calculate the total number of orders and the number of unique delivery services
    for each week. It then computes the average number of orders per delivery service for each week and plots these values
    using a line chart. The chart includes hover data showing the total number of orders and the number of actively delivery services for each week.

    :param df: DataFrame containing the dataset with "Week_Ordered" and "Delivery_service_ID" columns.
    :return: Plotly figure object with the line chart showing the average number of orders per delivery service per week.
    """
    df = df.groupby(["Week_Ordered", "Delivery_service_ID"]).size().reset_index(name="ID_Count")
    df = df.groupby("Week_Ordered").agg({"ID_Count": "sum", "Delivery_service_ID": "nunique"}).reset_index()
    df["Order_by_delivery"] = df["ID_Count"] / df["Delivery_service_ID"]
    all_weeks = pd.DataFrame({"Week_Ordered": range(df["Week_Ordered"].min(), df["Week_Ordered"].max() + 1)})
    df = pd.merge(all_weeks, df, on="Week_Ordered", how="left").fillna(0)
    fig = px.line(df, x="Week_Ordered", y="Order_by_delivery", title="Average weekly orders by delivery service", labels={"Week_Ordered": "Week of the year", "Order_by_delivery": "Average orders", "ID_Count": "Total orders", "Delivery_service_ID": "Actively delivery services"}, markers=True, hover_data=["ID_Count", "Delivery_service_ID"])
    fig.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
        xaxis={"title_font": {"size": 18}, "showgrid": True},
        yaxis={"title_font": {"size": 18}, "showgrid": True})
    return fig

def plot_central_delivery_locations(df: pd.DataFrame):
    """
    Generates a map with markers indicating the median delivery locations for each city and traffic density combination.
    This function processes the DataFrame to extract the median delivery location for each combination of city type and
    road traffic density. It then plots these locations on a Folium map, with markers displaying the coordinates,
    city type, and traffic density.

    :param df: DataFrame containing the dataset with "City", "Road_traffic_density", and "Delivery_location" columns.
    :return: Folium map object with markers showing the median delivery locations for each city and traffic density combination.
    """
    df = df[["City", "Road_traffic_density", "Delivery_location"]].copy()
    df[["Delivery_location_x", "Delivery_location_y"]] = pd.DataFrame(df["Delivery_location"].tolist(), index=df.index)
    df = df.drop(columns=["Delivery_location"])
    df = df.groupby(["City", "Road_traffic_density"]).median().reset_index()
    df["Delivery_location"] = list(zip(df["Delivery_location_x"], df["Delivery_location_y"]))
    df = df.drop(columns=["Delivery_location_x", "Delivery_location_y"])
    df = df[df["Delivery_location"].apply(lambda loc: loc[0] >= 1 and loc[1] >= 1)]
    fig = folium.Map(location=(20.904992, 79.417227), zoom_start=5)
    for index, location_info in df.iterrows():
        popup_html = f"""
        <div style="max-width: 150px">
            {location_info["Delivery_location"][0]}° N, {location_info["Delivery_location"][1]}° W<br>
            City type: {location_info['City']}<br>
            Traffic: {location_info['Road_traffic_density']}
        </div>
        """
        folium.Marker(location_info["Delivery_location"], popup=folium.Popup(popup_html, max_width=350)).add_to(fig)
    return fig


def plot_restaurant_locations(df: pd.DataFrame):
    """
    This function processes the DataFrame to filter out invalid restaurant locations (those with coordinates
    less than 1 in either latitude or longitude, mostly being [0, 0], known as "Null island"). It then groups the data by restaurant location and counts
    the number of deliveries from each location. The resulting map includes markers for each restaurant
    location, displaying the coordinates and the number of deliveries.

    :param df: DataFrame containing the dataset with "ID" and "Restaurant_location" columns.
    :return: Folium map object with markers showing the number of deliveries from each restaurant location.
    """
    df = df[df["Restaurant_location"].apply(lambda loc: loc[0] >= 1 and loc[1] >= 1)]
    df = df[["ID", "Restaurant_location"]].groupby("Restaurant_location").count().reset_index()
    fig = folium.Map(location=(20.904992, 79.417227), zoom_start=5)
    for index, location_info in df.iterrows():
        popup_html = f"""
        <div style="max-width: 150px">
            {location_info['Restaurant_location'][0]}° N, {location_info['Restaurant_location'][1]}° W<br>
            Number of deliveries: {location_info['ID']}
        </div>
        """
        folium.Marker(location_info["Restaurant_location"], popup=folium.Popup(popup_html, max_width=350)).add_to(fig)
    return fig

def plot_orders_heatmap(df: pd.DataFrame):
    """
    This function processes the DataFrame to filter out invalid delivery locations (those with coordinates
    less than 1 in either latitude or longitude, mostly being [0, 0], known as "Null island"). It then
    extracts the valid delivery locations and plots them on a Folium map using a heatmap. The heatmap
    visualizes the density of delivery locations.

    :param df: DataFrame containing the dataset with "Delivery_location" column.
    :return: Folium map object with a heatmap showing the density of delivery locations.
    """
    df = df[df["Delivery_location"].apply(lambda loc: loc[0] >= 1 and loc[1] >= 1)]["Delivery_location"].to_numpy()
    fig = folium.Map(location=(20.904992, 79.417227), zoom_start=5)
    HeatMap(data=df, radius=20).add_to(fig)
    return fig

def plot_deliveries_by_age(df: pd.DataFrame):
    """
    This function processes the DataFrame to count the number of deliveries for each delivery person age,
    and then plots these counts using a bar chart.

    :param df: DataFrame containing the dataset with "ID" and "Delivery_person_Age" columns.
    :return: Plotly figure object with the bar chart showing the number of deliveries by age.
    """
    df = df[["ID", "Delivery_person_Age"]].groupby("Delivery_person_Age").count().reset_index().sort_values(by="Delivery_person_Age")
    fig = px.bar(df, x="Delivery_person_Age", y="ID", title="Number of deliveries by delivery person age", labels={"Delivery_person_Age": "Age", "ID": "Quantity"})
    fig.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
        xaxis={"title_font": {"size": 18}, "showgrid": True},
        yaxis={"title_font": {"size": 18}, "showgrid": True})
    return fig

def plot_deliveries_by_vehicle_condition(df: pd.DataFrame):
    """
    This function processes the DataFrame to count the number of deliveries for each vehicle condition,
    and then plots these counts using a bar chart.

    :param df: DataFrame containing the dataset with "ID" and "Vehicle_condition" columns.
    :return: Plotly figure object with the bar chart showing the number of deliveries by vehicle condition.
    """
    df = df[["ID", "Vehicle_condition"]].groupby("Vehicle_condition").count().reset_index().sort_values(by="Vehicle_condition")
    x_values = df["Vehicle_condition"].unique()
    fig = px.bar(df, x="Vehicle_condition", y="ID", title="Number of deliveries by vehicle condition", labels={"Vehicle_condition": "Condition", "ID": "Quantity"})
    fig.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
        xaxis={"title_font": {"size": 18}, "showgrid": True, "tickmode": "array", "tickvals": x_values, "ticktext": ["muito ruim", "ruim", "bom", "muito bom"]},
        yaxis={"title_font": {"size": 18}, "showgrid": True, "type": "log"})
    return fig
