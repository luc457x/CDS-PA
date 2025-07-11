import libs
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import datetime as dt
### Loading
df_clear = libs.load_dataset()

### Layout Streamlit
st.set_page_config(page_title="Curry Company - Visão Empresa", page_icon="📈", layout="wide")
## Sidebar
col1, col2, col3, col4 = st.sidebar.columns([0.5, 3, 2, 0.5])
with col2:
    img = Image.open("./img/logo.png")
    st.image(img, width=180)
with col3:
    st.markdown("# Curry Company")
    st.markdown("### Fastest in Town")
st.sidebar.markdown("""---""")
col1, col2, col3 = st.sidebar.columns(3, gap="medium")
with col1:
    if st.button("Company view"):
        st.session_state.visualizacao = 1
with col2:
    if st.button("Restaurant view"):
        st.session_state.visualizacao = 2
with col3:
    if st.button("Delivery view"):
        st.session_state.visualizacao = 3
st.sidebar.markdown("""---""")
st.sidebar.write("**Data range**")
col1, col2 = st.sidebar.columns(2)
with col1:
    date_init = st.date_input("Time:", value=dt.datetime(2022, 2, 11), min_value=dt.datetime(2022, 2, 11), max_value=dt.datetime(2022, 4, 6), format="DD-MM-YYYY")
with col2:
    date_end = st.date_input("", value=dt.datetime(2022, 4, 6), min_value=dt.datetime(2022, 2, 11), max_value=dt.datetime(2022, 4, 6), format="DD-MM-YYYY")
age_min, age_max = st.sidebar.slider(
    "Delivery person age:",
    min_value=df_clear["Delivery_person_Age"].min(),
    max_value=df_clear["Delivery_person_Age"].max(),
    value=(df_clear["Delivery_person_Age"].min(), df_clear["Delivery_person_Age"].max()),
    step=1
)
st.sidebar.markdown("""---""")
st.sidebar.write("**Filters**")
traffic_options = st.sidebar.multiselect("Traffic conditions:", ["Low", "Medium", "High", "Jam", "Unknown"], default=[])
city_options = st.sidebar.multiselect("City types:", ["Metropolitan", "Urban", "Semi-Urban", "Unknown"], default=[])
festival_options = st.sidebar.multiselect("During festivals:", ["Yes", "No", "Unknown"], default=[])
# Filters
df_clear = df_clear[(df_clear["Time_Ordered"].dt.date >= date_init) & (df_clear["Time_Ordered"].dt.date <= date_end)]
df_clear = df_clear[(df_clear["Delivery_person_Age"] >= age_min) & (df_clear["Delivery_person_Age"] <= age_max)]
if traffic_options: df_clear = df_clear[df_clear["Road_traffic_density"].isin(traffic_options)]
if city_options: df_clear = df_clear[df_clear["City"].isin(city_options)]
if festival_options: df_clear = df_clear[df_clear["Festival"].isin(festival_options)]
## Main page
# graphs & Metrics
df_clear["Day_Ordered"] = pd.to_datetime(df_clear["Time_Ordered"]).dt.date
df = df_clear[["ID", "Day_Ordered"]].groupby("Day_Ordered").count().reset_index()
df = df[["Day_Ordered", "ID"]].pivot_table(index="Day_Ordered", aggfunc="sum").reset_index()
fig01 = px.bar(df, x="Day_Ordered", y="ID", title="Daily orders", labels={"Day_Ordered": "Date", "ID": "Quantity"})
fig01.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
df_clear["Week_Ordered"] = pd.to_datetime(df_clear["Day_Ordered"]).dt.strftime("%W").astype(int)
df = df_clear[["Week_Ordered", "ID"]].pivot_table(index="Week_Ordered", aggfunc="count").reset_index()
all_weeks = pd.DataFrame({"Week_Ordered": range(df["Week_Ordered"].min(), df["Week_Ordered"].max() + 1)})
df = pd.merge(all_weeks, df, on="Week_Ordered", how="left").fillna(0)
fig02 = px.line(df, x="Week_Ordered", y="ID", title="Weekly orders", labels={"Week_Ordered": "Week of the year", "ID": "Quantity"}, markers=True)
fig02.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
metric01 = df["ID"].sum()
metric02 = df["ID"].max()
metric03 = df["ID"].min()
metric04 = df["ID"].mean()
metric05 = df["ID"].std()
metric06 = df["ID"].diff().mean()
df = df_clear[["ID", "Road_traffic_density"]].groupby("Road_traffic_density").count().reset_index()
df["percent"] = df["ID"] / df["ID"].sum()
fig03 = px.pie(df, values="percent", names="Road_traffic_density", title="Orders distribution by traffic density")
fig03.update_layout(width=700, height=600,
    title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    legend={"font": {"size": 18}})
df = df_clear[["ID", "City", "Road_traffic_density"]].groupby(["City", "Road_traffic_density"]).count().reset_index()
fig04 = px.bar(df, x="City", y="ID", color="Road_traffic_density", title="Orders by city type grouped by traffic density", labels={"City": "City type", "ID": "Quantity", "Road_traffic_density": "Traffic"}, barmode="stack", log_y=True)
fig04.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
df_aux = df_clear.groupby(["Week_Ordered", "Delivery_person_ID"]).size().reset_index(name="ID_Count")
df_aux = df_aux.groupby("Week_Ordered").agg({"ID_Count": "sum", "Delivery_person_ID": "nunique"}).reset_index()
df_aux["Order_by_delivery"] = df_aux["ID_Count"] / df_aux["Delivery_person_ID"]
df_aux = pd.merge(all_weeks, df_aux, on="Week_Ordered", how="left").fillna(0)
fig05 = px.line(df_aux, x="Week_Ordered", y="Order_by_delivery", title="Average weekly orders by delivery service", labels={"Week_Ordered": "Week of the year", "Order_by_delivery": "Average orders", "ID_Count": "Total orders", "Delivery_person_ID": "Actively delivery services"}, markers=True, hover_data=["ID_Count", "Delivery_person_ID"])
fig05.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
df_aux = df_clear[["City", "Road_traffic_density", "Delivery_location"]].copy()
df_aux[["Delivery_location_x", "Delivery_location_y"]] = pd.DataFrame(df_aux["Delivery_location"].tolist(), index=df_aux.index)
df_aux = df_aux.drop(columns=["Delivery_location"])
df_aux = df_aux.groupby(["City", "Road_traffic_density"]).median().reset_index()
df_aux["Delivery_location"] = list(zip(df_aux["Delivery_location_x"], df_aux["Delivery_location_y"]))
df_aux = df_aux.drop(columns=["Delivery_location_x", "Delivery_location_y"])
df_aux = df_aux[df_aux["Delivery_location"].apply(lambda loc: loc[0] >= 1 and loc[1] >= 1)]
fig06 = folium.Map(location=(20.904992, 79.417227), zoom_start=5)
for index, location_info in df_aux.iterrows():
    popup_html = f"""
    <div style="max-width: 150px">
        {location_info["Delivery_location"][0]}° N, {location_info["Delivery_location"][1]}° W<br>
        City type: {location_info['City']}<br>
        Traffic: {location_info['Road_traffic_density']}
    </div>
    """
    folium.Marker(location_info["Delivery_location"], popup=folium.Popup(popup_html, max_width=350)).add_to(fig06)
df_aux = df_clear[["Delivery_person_ID", "Delivery_person_Age"]].groupby("Delivery_person_Age").nunique().reset_index().sort_values(by="Delivery_person_Age")
fig07 = px.bar(df_aux, x="Delivery_person_Age", y="Delivery_person_ID", title="Number of delivery workers by age", labels={"Delivery_person_Age": "Age", "Delivery_person_ID": "Quantity"})
fig07.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True},
    yaxis={"title_font": {"size": 18}, "showgrid": True})
df_aux = df_clear[["Delivery_person_ID", "Vehicle_condition"]].groupby("Vehicle_condition").nunique().reset_index().sort_values(by="Vehicle_condition")
x_values = df_aux["Vehicle_condition"].unique()
fig08 = px.bar(df_aux, x="Vehicle_condition", y="Delivery_person_ID", title="Number of vehicles by condition", labels={"Vehicle_condition": "Condition", "Delivery_person_ID": "Quantity"})
fig08.update_layout(title={"x": 0.5, "xanchor": "center", "font": {"size": 24}},
    xaxis={"title_font": {"size": 18}, "showgrid": True, "tickmode": "array", "tickvals": x_values, "ticktext": ["muito ruim", "ruim", "bom", "muito bom"]},
    yaxis={"title_font": {"size": 18}, "showgrid": True, "type": "log"})
fig09 = df_clear[["Delivery_person_ID", "Delivery_person_Ratings"]].groupby("Delivery_person_ID").mean().sort_values(by="Delivery_person_Ratings", ascending=False).rename(columns={"Delivery_person_Ratings": "Mean_rating"}).reset_index()
fig09.index = fig09.index +1
fig09["Mean_rating"] = fig09["Mean_rating"].round(2)
fig10 = df_clear[["Delivery_person_Ratings", "Road_traffic_density"]].groupby("Road_traffic_density").agg({"Delivery_person_Ratings": ["mean", "std"]})
fig10.columns = ["Mean_Rating", "Std_Rating"]
fig10.reset_index(inplace=True)
fig10.index = fig10.index +1
fig11 = df_clear[["Delivery_person_Ratings", "Weatherconditions"]].groupby("Weatherconditions").agg({"Delivery_person_Ratings": ["mean", "std"]})
fig11.columns = ["Mean_Rating", "Std_Rating"]
fig11.reset_index(inplace=True)
fig11.index = fig11.index +1
fig12 = df_clear[["Delivery_person_ID", "Velocity(km/h)"]].groupby("Delivery_person_ID").mean().sort_values("Velocity(km/h)", ascending=False).reset_index()
fig12 = fig12.head(10).reset_index(drop=True)
fig12.index = fig12.index +1
fig13 = df_clear[["Delivery_person_ID", "Velocity(km/h)"]].groupby("Delivery_person_ID").mean().sort_values("Velocity(km/h)").reset_index()
fig13 = fig13.head(10).reset_index(drop=True)
fig13.index = fig13.index +1
fig14 = folium.Map(location=(20.904992, 79.417227), zoom_start=5)
df_aux = df_clear[df_clear["Restaurant_location"].apply(lambda loc: loc[0] >= 1 and loc[1] >= 1)]
df_aux = df_clear[["ID", "Restaurant_location"]].groupby("Restaurant_location").count().reset_index()
for index, location_info in df_aux.iterrows():
    popup_html = f"""
    <div style="max-width: 150px">
        {location_info['Restaurant_location'][0]}° N, {location_info['Restaurant_location'][1]}° W<br>
        Number of deliveries: {location_info['ID']}
    </div>
    """
    folium.Marker(location_info["Restaurant_location"], popup=folium.Popup(popup_html, max_width=350)).add_to(fig14)
metric07 = df_aux["Restaurant_location"].nunique()
metric08 = df_aux["ID"].mean()
df_aux = df_clear[["Delivery_person_ID", "ID"]].groupby("Delivery_person_ID").count().reset_index()
metric09 = df_aux["Delivery_person_ID"].nunique()
metric10 = df_aux["ID"].mean()
df_aux = df_clear[df_clear["Delivery_location"].apply(lambda loc: loc[0] >= 1 and loc[1] >= 1)]["Delivery_location"].to_numpy()
fig15 = folium.Map(location=(20.904992, 79.417227), zoom_start=5)
HeatMap(data=df_aux, radius=20).add_to(fig15)
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
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1], gap="small")
            with col1:
                st.metric("Pedidos no período", int(metric01), width="content")
                st.metric("Média semanal", int(metric04), width="content")
            with col2:
                st.metric("Restaurantes ativos", metric07)
                st.metric("Desvio padrão semanal", int(metric05))
            with col3:
                st.metric("Serviços de entrega ativos", metric09)
                st.metric("Variação média semanal", int(metric06), f"{(metric06 / metric01) * 100:.2f}%")
            with col4:
                st.metric("Média de pedidos por restaurante", int(metric08))
                st.metric("Melhor semana", int(metric02), f"{((metric02 - metric04) / metric04) * 100:.2f}%")
            with col5:
                st.metric("Média de pedidos por serviço de entrega", int(metric10))
                st.metric("Pior semana", int(metric03), f"{-100 if np.isinf(((metric03 - metric04) / metric04) * 100) else ((metric03 - metric04) / metric04) * 100:.2f}%")
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            st.plotly_chart(fig02, use_container_width=True)
        with col2:
            st.plotly_chart(fig05, use_container_width=True)
    with tab3:
        col1, col2, col3 = st.columns([0.3, 1, 0.3])
        with col2:
            st.write("Localização central de entregas por tipo de cidade e tráfego")
            folium_static(fig06, width=1024, height=600)
            
def viz2():
    tab1, tab2, tab3 = st.tabs(["Gerencial", "Tático", "Geográfico"], )
    with tab1:
        st.write("Em construção")
    with tab3:
        col1, col2, col3 = st.columns([0.3, 1, 0.3])
        with col2:
            st.write("Localização dos restaurantes")
            folium_static(fig14, width=1024, height=600)
def viz3():
    tab1, tab2, tab3 = st.tabs(["Gerencial", "Tático", "Geográfico"], )
    with tab1:
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            st.plotly_chart(fig07, use_container_width=True)
        with col2:
            st.plotly_chart(fig08, use_container_width=True)
        col1, col2 = st.columns([1, 2], gap="medium")
        with col1:
            st.write("Avaliação média por serviço de entrega")
            st.dataframe(fig09, use_container_width=True)
        with col2:
            st.write("Avaliação média e desvio padrão por tráfego")
            st.dataframe(fig10, use_container_width=True)
            st.write("Avaliação média e desvio padrão por condições climáticas")
            st.dataframe(fig11, use_container_width=True)
        col1, col2 = st.columns([1, 1], gap="medium")
        with col1:
            st.write("TOP 10 entregadores mais rápidos")
            st.dataframe(fig12, use_container_width=True)
        with col2:
            st.write("TOP 10 entregadores mais lentos")
            st.dataframe(fig13, use_container_width=True)
    with tab3:
        col1, col2, col3 = st.columns([0.3, 1, 0.3])
        with col2:
            st.write("HeatMap de pedidos")
            folium_static(fig15, width=1024, height=600)
if 'visualizacao' not in st.session_state:
    st.session_state.visualizacao = 1
if st.session_state.visualizacao == 1:
    viz1()
elif st.session_state.visualizacao == 2:
    viz2()
elif st.session_state.visualizacao == 3:
    viz3()
st.markdown("""---""")
st.write("*Powered by lucas7x*")
            
