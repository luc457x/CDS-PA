from utils import *
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static
import datetime as dt
### Cleaning
DF_RAW = pd.read_csv("train.csv")
df_clear = DF_RAW.copy()
df_clear = df_clear.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
df_clear["Delivery_person_Age"] = df_clear["Delivery_person_Age"].apply(pd.to_numeric, errors="coerce").astype("Int64")
df_clear["Delivery_person_Ratings"] = df_clear["Delivery_person_Ratings"].apply(pd.to_numeric, errors="coerce")
df_clear["multiple_deliveries"] = df_clear["multiple_deliveries"].apply(pd.to_numeric, errors="coerce").astype("Int64")
df_clear.rename(columns={"Time_Orderd": "Time_Ordered"}, inplace=True)
df_clear["City"] = df_clear["City"].str.replace("Metropolitian", "Metropolitan", regex=False)
df_clear["Order_Date"] = pd.to_datetime(df_clear["Order_Date"], format="%d-%m-%Y").astype("string")
df_clear["Time_Ordered"] = pd.to_datetime(df_clear["Time_Ordered"], format="%H:%M:%S").dt.time.astype("string")
df_clear["Time_Order_picked"] = pd.to_datetime(df_clear["Time_Order_picked"], format="%H:%M:%S").dt.time.astype("string")
df_clear["Time_taken(min)"] = df_clear["Time_taken(min)"].str.extract(r'(\d+)').astype("Int64")
df_clear["Weatherconditions"] = df_clear["Weatherconditions"].str.replace("conditions ", "", regex=False)
cols = ["Weatherconditions", "Road_traffic_density", "City", "Festival"]
for col in cols:
    df_clear[col] = df_clear[col].str.replace("NaN", "Unknown", regex=False)
df_clear.loc[df_clear["Delivery_person_Ratings"] > 5.0, "Delivery_person_Ratings"] = 5.0
df_clear = df_clear.dropna(thresh=len(df_clear.columns) - 2).reset_index(drop=True)
cols = ["Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude"]
for col in cols:
    df_clear[col] = abs(df_clear[col])
df_clear["Restaurant_location"] = list(zip(df_clear["Restaurant_latitude"], df_clear["Restaurant_longitude"]))
df_clear["Delivery_location"] = list(zip(df_clear["Delivery_location_latitude"], df_clear["Delivery_location_longitude"]))
df_clear.drop(columns=["Restaurant_latitude", "Restaurant_longitude", "Delivery_location_latitude", "Delivery_location_longitude"], inplace=True)
df_clear["Time_Ordered"] = pd.to_datetime(df_clear["Order_Date"] + " " + df_clear["Time_Ordered"], format="%Y-%m-%d %H:%M:%S")
df_clear["Time_Order_picked"] = pd.to_datetime(df_clear['Order_Date'] + " " + df_clear["Time_Order_picked"], format="%Y-%m-%d %H:%M:%S")
df_clear["Time_Order_picked"] = df_clear.apply(lambda row: row["Time_Order_picked"] + pd.Timedelta(days=1) if row["Time_Ordered"] > row["Time_Order_picked"] else row["Time_Order_picked"], axis=1)
df_clear["Time_Order_delivered"] = df_clear["Time_Order_picked"] + pd.to_timedelta(df_clear["Time_taken(min)"], unit='m')
df_clear.drop(["Order_Date"], axis=1, inplace=True)
df_clear["Delivery_person_Age"] = df_clear['Delivery_person_Age'].fillna(df_clear['Delivery_person_Age'].median())
df_aux = df_clear[["Delivery_person_ID", "Delivery_person_Ratings"]].dropna()
df_aux = df_aux.groupby(["Delivery_person_ID"]).mean().reset_index()
df_clear = df_clear.merge(df_aux, on="Delivery_person_ID", how="left", suffixes=('', '_mean'))
df_clear["Delivery_person_Ratings"] = df_clear["Delivery_person_Ratings"].fillna(df_clear["Delivery_person_Ratings_mean"])
df_clear.drop(columns=["Delivery_person_Ratings_mean"], inplace=True)
df_aux = df_clear[["Time_Ordered", "Time_Order_picked", "Time_Order_delivered", "Type_of_order"]].dropna()
df_aux["Time_to_pick"] = (df_aux["Time_Order_picked"] - df_aux["Time_Ordered"]).dt.total_seconds() / 60
df_aux["Time_to_delivery"] = (df_aux["Time_Order_delivered"] - df_aux["Time_Order_picked"]).dt.total_seconds() / 60
df_aux = df_aux.drop(columns=["Time_Ordered", "Time_Order_picked", "Time_Order_delivered"])
df_times_grouped = df_aux.groupby(["Type_of_order"]).agg(["mean", "median"]).reset_index()
df_clear["Time_Ordered"] = df_clear["Time_Ordered"].fillna(df_clear["Time_Order_picked"] - pd.to_timedelta(df_times_grouped.loc[0, ("Time_to_pick", "median")], unit="m"))
### Layout Streamlit
st.set_page_config(page_title="Curry Company - Visão Empresa", page_icon="📈", layout="wide")
## Sidebar
col1, col2, col3, col4 = st.sidebar.columns([1, 1.5, 2, 1])
with col2:
    img = Image.open("./img/logo.png")
    st.image(img, width=120)
with col3:
    st.markdown("# Curry Company")
    st.markdown("### Fastest in Town")
st.sidebar.markdown("""---""")
col1, col2, col3 = st.sidebar.columns(3, gap="medium")
with col1:
    if st.button("Visão Empresa"):
        st.session_state.visualizacao = 1
with col2:
    if st.button("Visão Entregadores"):
        st.session_state.visualizacao = 2
with col3:
    if st.button("Visão Restaurantes"):
        st.session_state.visualizacao = 3
st.sidebar.markdown("""---""")
col1, col2 = st.sidebar.columns(2)
with col1:
    date_slider_init = st.date_input("Intervalo de tempo:", value=dt.datetime(2022, 2, 11), min_value=dt.datetime(2022, 2, 11), max_value=dt.datetime(2022, 4, 6), format="DD-MM-YYYY")
with col2:
    date_slider_end = st.date_input("", value=dt.datetime(2022, 4, 6), min_value=dt.datetime(2022, 2, 11), max_value=dt.datetime(2022, 4, 6), format="DD-MM-YYYY")
st.sidebar.markdown("""---""")
traffic_options = st.sidebar.multiselect("Condições de trânsito:", ["Low", "Medium", "High", "Jam", "Unknown"], default=["Low", "Medium", "High", "Jam", "Unknown"])
st.sidebar.markdown("""---""")
city_options = st.sidebar.multiselect("Tipos de cidades:", ["Metropolitan", "Urban", "Semi-Urban", "Unknown"], default=["Metropolitan", "Urban", "Semi-Urban", "Unknown"])
error = False
if not traffic_options:
    st.error("Por favor selecione ao menos uma condição de trânsito.")
    error = True
if not city_options:
    st.error("Por favor selecione ao menos um tipo de cidade.")
    error = True
if error == True: st.stop()
# Filters
df_clear = df_clear[(df_clear["Time_Ordered"].dt.date >= date_slider_init) & (df_clear["Time_Ordered"].dt.date <= date_slider_end)]
df_clear = df_clear[df_clear["Road_traffic_density"].isin(traffic_options)]
df_clear = df_clear[df_clear["City"].isin(city_options)]
## Main page
# graphs
df_clear["Day_Ordered"] = pd.to_datetime(df_clear["Time_Ordered"]).dt.date
df = df_clear[["ID", "Day_Ordered"]].groupby("Day_Ordered").count().reset_index()
df = df[["Day_Ordered", "ID"]].pivot_table(index="Day_Ordered", aggfunc="sum").reset_index()
fig01 = px.bar(df, x="Day_Ordered", y="ID", title="Quantidade de pedidos por dia", labels={"Day_Ordered": "Data", "ID": "Quantidade de pedidos"})
fig01.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
df_clear["Week_Ordered"] = pd.to_datetime(df_clear["Day_Ordered"]).dt.strftime("%W").astype(int)
df = df_clear[["Week_Ordered", "ID"]].pivot_table(index="Week_Ordered", aggfunc="count").reset_index()
min_week = df["Week_Ordered"].min()
max_week = df["Week_Ordered"].max()
all_weeks = pd.DataFrame({"Week_Ordered": range(min_week, max_week + 1)})
df = pd.merge(all_weeks, df, on="Week_Ordered", how="left").fillna(0)
fig02 = px.line(df, x="Week_Ordered", y="ID", title="Quantidade de pedidos por semana", labels={"Week_Ordered": "Semana do ano", "ID": "Quantidade de pedidos"}, markers=True)
fig02.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
df = df_clear[["ID", "Road_traffic_density"]].groupby("Road_traffic_density").count().reset_index()
df["percent"] = df["ID"] / df["ID"].sum()
fig03 = px.pie(df, values="percent", names="Road_traffic_density", title="Distribuição de pedidos por densidade de tráfego")
fig03.update_layout(width=700, height=600,
    title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    legend={"font": {"size": 18}})
df = df_clear[["ID", "City", "Road_traffic_density"]].groupby(["City", "Road_traffic_density"]).count().reset_index()
df = df.pivot(index="City", columns="Road_traffic_density", values="ID").fillna(0)
fig04 = px.bar(df, x=df.index, y=df.columns, title="Pedidos por tipo de cidade agrupados por densidade de tráfego", labels={"City": "Tipo de cidade", "value": "Quantidade de pedidos em escala log", "Road_traffic_density": "Densidade de tráfego"}, barmode="stack", log_y=True)
fig04.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
df1 = df_clear[["ID", "Week_Ordered"]].groupby("Week_Ordered").count().reset_index()
df2 = df_clear[["Delivery_person_ID", "Week_Ordered"]].groupby("Week_Ordered").nunique().reset_index()
df_aux = pd.merge(df1, df2, how="inner", on="Week_Ordered")
df_aux["Oder_by_delivery"] = df_aux["ID"] / df_aux["Delivery_person_ID"]
df_aux = pd.merge(all_weeks, df_aux, on="Week_Ordered", how="left").fillna(0)
fig05 = px.line(df_aux, x="Week_Ordered", y="Oder_by_delivery", title="Quantidade de pedidos por entregador agrupados por semana", labels={"Week_Ordered": "Semana", "Oder_by_delivery": "Quantidade de pedidos por entregador"}, markers=True)
fig05.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
df_aux = df_clear[["City", "Road_traffic_density", "Delivery_location"]].copy()
df_aux[["Delivery_location_x", "Delivery_location_y"]] = pd.DataFrame(df_aux["Delivery_location"].tolist(), index=df_aux.index)
df_aux = df_aux.drop(columns=["Delivery_location"])
df_aux = df_aux.groupby(["City", "Road_traffic_density"]).median().reset_index()
df_aux["Delivery_location"] = list(zip(df_aux["Delivery_location_x"], df_aux["Delivery_location_y"]))
df_aux = df_aux.drop(columns=["Delivery_location_x", "Delivery_location_y"])
fig06 = folium.Map(location=(18.5554895, 76.6276725), zoom_start=6)
for index, location_info in df_aux.iterrows():
    popup_html = f"""
    <div style="max-width: 150px">
        City type: {location_info['City']}<br>
        Traffic: {location_info['Road_traffic_density']}<br>
        Coordinates: {location_info['Delivery_location']}
    </div>
    """
    folium.Marker(location_info["Delivery_location"], popup=folium.Popup(popup_html, max_width=350)).add_to(fig06)
# ===============================
df_aux = df_clear[["ID", "Delivery_person_Age"]].groupby("Delivery_person_Age").count().reset_index().sort_values(by="Delivery_person_Age")
fig07 = px.bar(df_aux, x="Delivery_person_Age", y="ID", title="Quantidade de entregadores por idade", labels={"Delivery_person_Age": "Idade", "ID": "Quantidade"})
fig07.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
df_aux = df_clear[["ID", "Vehicle_condition"]].groupby("Vehicle_condition").count().reset_index().sort_values(by="Vehicle_condition")
x_values = df_aux["Vehicle_condition"].unique()
fig08 = px.bar(df_aux, x="Vehicle_condition", y="ID", title="Quantidade de entregadores por condição de veículo", labels={"Vehicle_condition": "Condição", "ID": "Quantidade"})
fig08.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True, "tickmode": "array", "tickvals": x_values, "ticktext": ["muito ruim", "ruim", "bom", "muito bom"]},
    yaxis={"title_font": {"size": 18}, "showgrid": True, "type": "log"})
# ===============================
# body
def viz1():
    tab1, tab2, tab3 = st.tabs(["Gerencial", "Tático", "Geográfico"], )
    with tab1:
        st.plotly_chart(fig01, use_container_width=True)
        col1, col2 = st.columns([1, 1.5], gap="medium")
        with col1:
            st.plotly_chart(fig03, use_container_width=True)
        with col2:
            st.plotly_chart(fig04, use_container_width=True)
    with tab2:
        st.plotly_chart(fig02, use_container_width=True)
        st.plotly_chart(fig05, use_container_width=True)
    with tab3:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Localização central de entregas agrupados por tipo de cidade e tráfego")
            folium_static(fig06, width=1024, height=600)
def viz2():
    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        st.plotly_chart(fig07, use_container_width=True)
    with col2:
        st.plotly_chart(fig08, use_container_width=True)
def viz3():
    st.write("Em construção")
if 'visualizacao' not in st.session_state:
    st.session_state.visualizacao = 1
if st.session_state.visualizacao == 1:
    viz1()
elif st.session_state.visualizacao == 2:
    viz2()
elif st.session_state.visualizacao == 3:
    viz3()
st.markdown("""---""")
st.markdown("### *Powered by lucas7x*")
            
