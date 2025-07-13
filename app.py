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
df_clear = df_clear[(pd.to_datetime(df_clear["Time_Ordered"]).dt.date >= date_init) & (pd.to_datetime(df_clear["Time_Ordered"]).dt.date <= date_end)]
df_clear = df_clear[(df_clear["Delivery_person_Age"] >= age_min) & (df_clear["Delivery_person_Age"] <= age_max)]
if traffic_options: df_clear = df_clear[df_clear["Road_traffic_density"].isin(traffic_options)]
if city_options: df_clear = df_clear[df_clear["City"].isin(city_options)]
if festival_options: df_clear = df_clear[df_clear["Festival"].isin(festival_options)]
## Main page
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
            
