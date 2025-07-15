import pandas as pd
import numpy as np
from haversine import haversine

pd.set_option("display.max_columns", None)
pd.set_option("future.no_silent_downcasting", True)

def clear_data(df):
    """
    Cleans and preprocesses the input DataFrame by performing the following steps:
    1. Strips leading and trailing whitespace from all string columns.
    2. Converts the "Delivery_person_Age", "Delivery_person_Ratings" and "multiple_deliveries" columns to numeric types, coercing errors to NaN and setting the data type to "Int64".
    3. Renames the "Time_Orderd" column to "Time_Ordered".
    4. Replaces occurrences of "Metropolitian" with "Metropolitan" in the "City" column.
    5. Converts the "Order_Date" column to datetime format and then to string format.
    6. Converts the "Time_Ordered", "Time_Order_picked", and "Time_taken(min)" columns to appropriate datetime or time formats.
    7. Extracts numeric values from the "Time_taken(min)" column and converts them to "Int64".
    8. Removes the prefix "conditions " from the "Weatherconditions" column.
    9. Replaces "NaN" with "Unknown" in specified columns ("Weatherconditions", "Road_traffic_density", "City", "Festival").
    10. Ensures that "Delivery_person_Ratings" values do not exceed 5.0.
    11. Drops rows with more than two NaN values.
    12. Convert negative values to positive in the columns ("Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude").
    13. Creates "Restaurant_location" and "Delivery_location" columns by zipping latitude and longitude values.
    14. Combines "Order_Date" and "Time_Ordered" to create a single datetime column for "Time_Ordered".
    15. Combines "Order_Date" and "Time_Order_picked" to create a single datetime column for "Time_Order_picked".
    16. Calculates "Time_Order_delivered" by adding "Time_taken(min)" to "Time_Order_picked" and swap "Order_Date" with it.
    17. Fills NaN values in "Delivery_person_Age" with the median age.
    18. Calculates the mean "Delivery_person_Ratings" for each "Delivery_person_ID" and fill NaN values in "Delivery_person_Ratings" with the mean rating.
    19. Fills NaN values in "Time_Ordered" with the median "Time_to_pick".
    20. Calculates the "Distance(km)" between "Restaurant_location" and "Delivery_location" using the Haversine formula.
    21. Calculates the "Velocity(km/h)" based on "Distance(km)" and "Time_taken(min)".
    22. Calculates "Prepare_time(min)" based on "Time_Ordered" and "Time_Order_picked".
    23. Renames the "Delivery_Person_ID" column to "Delivery_service_ID".
    24. Drop "multiple_deliveries" column.
    25. Reorders the columns to a specified order.
    26. Saves the cleaned DataFrame to a pickle file.

    :param df: DataFrame to be cleaned and preprocessed.
    :return: Cleaned and preprocessed DataFrame.
    """
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df["Delivery_person_Age"] = df["Delivery_person_Age"].apply(pd.to_numeric, errors="coerce").astype("Int64")
    df["Delivery_person_Ratings"] = df["Delivery_person_Ratings"].apply(pd.to_numeric, errors="coerce")
    df["multiple_deliveries"] = df["multiple_deliveries"].apply(pd.to_numeric, errors="coerce").astype("Int64")
    df.rename(columns={"Time_Orderd": "Time_Ordered"}, inplace=True)
    df["City"] = df["City"].str.replace("Metropolitian", "Metropolitan", regex=False)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y").astype("string")
    df["Time_Ordered"] = pd.to_datetime(df["Time_Ordered"], format="%H:%M:%S").dt.time.astype("string")
    df["Time_Order_picked"] = pd.to_datetime(df["Time_Order_picked"], format="%H:%M:%S").dt.time.astype("string")
    df["Time_taken(min)"] = df["Time_taken(min)"].str.extract(r'(\d+)').astype("Int64")
    df["Weatherconditions"] = df["Weatherconditions"].str.replace("conditions ", "", regex=False)
    cols = ["Weatherconditions", "Road_traffic_density", "City", "Festival"]
    for col in cols:
        df[col] = df[col].str.replace("NaN", "Unknown", regex=False)
    df.loc[df["Delivery_person_Ratings"] > 5.0, "Delivery_person_Ratings"] = 5.0
    df = df.dropna(thresh=len(df.columns) - 2).reset_index(drop=True)
    cols = ["Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude"]
    for col in cols:
        df[col] = abs(df[col])
    df["Restaurant_location"] = list(zip(df["Restaurant_latitude"], df["Restaurant_longitude"]))
    df["Delivery_location"] = list(zip(df["Delivery_location_latitude"], df["Delivery_location_longitude"]))
    df.drop(columns=["Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude"], inplace=True)
    df["Time_Ordered"] = pd.to_datetime(df["Order_Date"] + " " + df["Time_Ordered"], format="%Y-%m-%d %H:%M:%S")
    df["Time_Order_picked"] = pd.to_datetime(df["Order_Date"] + " " + df["Time_Order_picked"], format="%Y-%m-%d %H:%M:%S")
    df["Time_Order_picked"] = df.apply(lambda row: row["Time_Order_picked"] + pd.Timedelta(days=1) if row["Time_Ordered"] > row["Time_Order_picked"] else row["Time_Order_picked"], axis=1)
    df["Time_Order_delivered"] = df["Time_Order_picked"] + pd.to_timedelta(df["Time_taken(min)"], unit="m")
    df.drop(["Order_Date"], axis=1, inplace=True)
    df["Delivery_person_Age"] = df["Delivery_person_Age"].fillna(df["Delivery_person_Age"].median())
    df_aux = df[["Delivery_person_ID", "Delivery_person_Ratings"]].dropna()
    df_aux = df_aux.groupby(["Delivery_person_ID"]).mean().reset_index()
    df = df.merge(df_aux, on="Delivery_person_ID", how="left", suffixes=("", "_mean"))
    df["Delivery_person_Ratings"] = df["Delivery_person_Ratings"].fillna(df["Delivery_person_Ratings_mean"])
    df.drop(columns=["Delivery_person_Ratings_mean"], inplace=True)
    df_aux = df[["Time_Ordered", "Time_Order_picked", "Time_Order_delivered", "Type_of_order"]].dropna()
    df_aux["Time_to_pick"] = (df_aux["Time_Order_picked"] - df_aux["Time_Ordered"]).dt.total_seconds() / 60
    df_aux["Time_to_delivery"] = (df_aux["Time_Order_delivered"] - df_aux["Time_Order_picked"]).dt.total_seconds() / 60
    df_aux = df_aux.drop(columns=["Time_Ordered", "Time_Order_picked", "Time_Order_delivered"])
    df_times_grouped = df_aux.groupby(["Type_of_order"]).agg(["mean", "median"]).reset_index()
    df["Time_Ordered"] = df["Time_Ordered"].fillna(df["Time_Order_picked"] - pd.to_timedelta(df_times_grouped.loc[0, ("Time_to_pick", "median")], unit="m"))
    df["Distance(km)"] = df.apply(lambda x: haversine(x["Restaurant_location"], x["Delivery_location"]), axis=1)
    df["Velocity(km/h)"] = df["Distance(km)"] / (df["Time_taken(min)"] / 60)
    df["Pick_time(min)"] = ((df["Time_Order_picked"] - df["Time_Ordered"]).dt.total_seconds() / 60).astype(int)
    df.rename(columns={"Delivery_person_ID": "Delivery_service_ID"}, inplace=True)
    df.drop(columns=["multiple_deliveries"], inplace=True)
    df = df[["ID", "Delivery_service_ID", "Delivery_person_Age", "Delivery_person_Ratings", "Type_of_order", "Time_Ordered", "Time_Order_picked", "Pick_time(min)", "Time_Order_delivered", "Time_taken(min)", "Type_of_vehicle", "Vehicle_condition", "City", "Road_traffic_density", "Weatherconditions", "Festival", "Restaurant_location", "Delivery_location","Distance(km)", "Velocity(km/h)"]]
    df.to_pickle("./data/dataset_clear.pkl")
    return df

def load_dataset():
    """
    Loads the dataset from a CSV file. If the cleaned dataset is not found,
    it loads the raw dataset, cleans it using the `clear_data` function,
    and saves the cleaned dataset to a pickle file.
    Returns:
        pd.DataFrame: The loaded and possibly cleaned dataset.
    """
    try:
        df = pd.read_pickle("./data/dataset_clear.pkl")
    except FileNotFoundError:
        df = pd.read_csv("./data/dataset_raw.csv")
        df = clear_data(df)
    return df

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

def stringfy_time(time: int | float | list[int | float] | pd.DataFrame):
    """
    Converts time values from minutes to a string format of "hours:minutes".

    This function handles different types of input:
    - If the input is a single integer or float, it converts it to a string in the format "hours:minutes".
    - If the input is a list of integers or floats, it converts each element to the "hours:minutes" format.
    - If the input is a DataFrame, it converts each numeric element to the "hours:minutes" format.

    Parameters:
    time (int | float | list[int | float] | pd.DataFrame): The time value(s) to be converted.
        - If int or float: A single time value in minutes.
        - If list: A list of time values in minutes.
        - If pd.DataFrame: A DataFrame containing time values in minutes.

    Returns:
    str | list[str] | list[list[str]]: The formatted time string(s).
        - If input is int or float: A single string in the format "hours:minutes".
        - If input is list: A list of strings in the format "hours:minutes".
        - If input is pd.DataFrame: A list of lists of strings in the format "hours:minutes".

    Raises:
    ValueError: If the input type is invalid or if elements in the list or DataFrame are not int or float.
    """
    if isinstance(time, (int, float, np.int64, np.float64)):
        time = pd.Timedelta(round(time), unit="m")
        total_seconds = int(time.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}:{minutes:02d}"
    elif isinstance(time, list):
        formatted_times = []
        for t in time:
            if isinstance(t, (int, float, np.int64, np.float64)):
                t = pd.Timedelta(round(t), unit="m")
                total_seconds = int(t.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                formatted_times.append(f"{hours}:{minutes:02d}")
            else:
                raise ValueError("List elements must be int or float")
        return formatted_times
    elif isinstance(time, pd.DataFrame):
        formatted_times = []
        for row in time.itertuples(index=False):
            row_times = []
            for t in row:
                if isinstance(t, (int, float, np.int64, np.float64)):
                    t = pd.Timedelta(round(t), unit="m")
                    total_seconds = int(t.total_seconds())
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    row_times.append(f"{hours}:{minutes:02d}")
                else:
                    raise ValueError("DataFrame elements must be int or float")
            formatted_times.append(row_times)
        return formatted_times
    else:
        raise ValueError(f"Invalid input type: {type(time)}. Input must be int, float, list of int/float, or DataFrame")

