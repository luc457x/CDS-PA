import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("train.csv")
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
df["Weatherconditions"] = df["Weatherconditions"].str.replace("NaN", "Unknown", regex=False)
df["Road_traffic_density"] = df["Road_traffic_density"].str.replace("NaN", "Unknown", regex=False)
df["City"] = df["City"].str.replace("NaN", "Unknown", regex=False)
df["Festival"] = df["Festival"].str.replace("NaN", "Unknown", regex=False)
df.loc[df["Delivery_person_Ratings"] > 5.0, "Delivery_person_Ratings"] = 5.0
df = df.dropna(thresh=len(df.columns) - 2).reset_index(drop=True)
df = df.dropna(subset=["Time_taken(min)"]).reset_index(drop=True)
df["Restaurant_location"] = list(zip(df["Restaurant_latitude"], df["Restaurant_longitude"]))
df["Delivery_location"] = list(zip(df["Delivery_location_latitude"], df["Delivery_location_longitude"]))
df.drop(columns=["Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude"], inplace=True)
df["Time_Ordered"] = pd.to_datetime(df["Order_Date"] + " " + df["Time_Ordered"], format="%Y-%m-%d %H:%M:%S")
df["Time_Order_picked"] = pd.to_datetime(df['Order_Date'] + " " + df["Time_Order_picked"], format="%Y-%m-%d %H:%M:%S")
df["Time_Order_picked"] = df.apply(lambda row: row["Time_Order_picked"] + pd.Timedelta(days=1) if row["Time_Ordered"] > row["Time_Order_picked"] else row["Time_Order_picked"], axis=1)
df["Time_Order_delivered"] = df["Time_Order_picked"] + pd.to_timedelta(df["Time_taken(min)"], unit="m")
df.drop(["Order_Date", "Time_taken(min)"], axis=1, inplace=True)
df["Delivery_person_Age"] = df['Delivery_person_Age'].fillna(df['Delivery_person_Age'].median())
df_aux = df[["Delivery_person_ID", "Delivery_person_Ratings"]].dropna()
df_aux = df_aux.groupby(["Delivery_person_ID"]).mean().reset_index()
df = df.merge(df_aux, on="Delivery_person_ID", how="left", suffixes=('', '_mean'))
df["Delivery_person_Ratings"] = df["Delivery_person_Ratings"].fillna(df["Delivery_person_Ratings_mean"])
df.drop(columns=["Delivery_person_Ratings_mean"], inplace=True)
df_aux = df[["Time_Ordered", "Time_Order_picked", "Time_Order_delivered", "Type_of_order"]].dropna()
df_aux["Time_to_pick"] = (df_aux["Time_Order_picked"] - df_aux["Time_Ordered"]).dt.total_seconds() / 60
df_aux["Time_to_delivery"] = (df_aux["Time_Order_delivered"] - df_aux["Time_Order_picked"]).dt.total_seconds() / 60
df_aux = df_aux.drop(columns=["Time_Ordered", "Time_Order_picked", "Time_Order_delivered"])
df_times_grouped = df_aux.groupby(["Type_of_order"]).agg(["mean", "median"]).reset_index()
df["Time_Ordered"] = df["Time_Ordered"].fillna(df["Time_Order_picked"] - pd.to_timedelta(df_times_grouped.loc[0, ("Time_to_pick", "median")], unit="m"))
df["multiple_deliveries"] = df["multiple_deliveries"].fillna(1)


print(df.info())