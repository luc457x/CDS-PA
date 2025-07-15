import datetime as dt
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from libs import (
    pd, np, load_dataset, get_metrics_company, get_metrics_deliveries, get_metrics_restaurants, 
    get_mean_ratings_by_service, get_means_ratings_by_traffic, get_mean_ratings_by_weather, 
    get_mean_pick_time_by_city, get_mean_pick_time_by_order, get_top_10_fastest_deliveries, 
    get_mean_pick_time_by_traffic, plot_orders_per_week, plot_orders_per_day, plot_orders_by_traffic, 
    plot_orders_by_traffic_and_city_type, plot_weekly_orders_per_service, plot_central_delivery_locations, 
    plot_restaurant_locations, plot_orders_heatmap, plot_deliveries_by_age, plot_deliveries_by_vehicle_condition
    )
### Loading
df_clear = load_dataset()
### Layout Streamlit
st.set_page_config(page_title="Curry Company - Dashboard", page_icon="📈", layout="wide")
with open("./css/styles.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
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
    if st.button("Delivery view"):
        st.session_state.visualizacao = 2
with col3:
    if st.button("Restaurant view"):
        st.session_state.visualizacao = 3
st.sidebar.markdown("""---""")
st.sidebar.write("**Data range**")
col1, col2 = st.sidebar.columns(2)
with col1:
    date_init = st.date_input("Start date:", value=dt.datetime(2022, 2, 11), min_value=dt.datetime(2022, 2, 11), max_value=dt.datetime(2022, 4, 6), format="DD-MM-YYYY")
with col2:
    date_end = st.date_input("End date:", value=dt.datetime(2022, 4, 6), min_value=dt.datetime(2022, 2, 11), max_value=dt.datetime(2022, 4, 6), format="DD-MM-YYYY")
age_min, age_max = st.sidebar.slider(
    "Delivery person age:",
    min_value=df_clear["Delivery_person_Age"].min(),
    max_value=df_clear["Delivery_person_Age"].max(),
    value=(df_clear["Delivery_person_Age"].min(), df_clear["Delivery_person_Age"].max()),
    step=1
)
rate_min, rate_max = st.sidebar.slider(
    "Delivery person rating:",
    min_value=df_clear["Delivery_person_Ratings"].min(),
    max_value=df_clear["Delivery_person_Ratings"].max(),
    value=(df_clear["Delivery_person_Ratings"].min(), df_clear["Delivery_person_Ratings"].max()),
    step=0.1
)
st.sidebar.markdown("""---""")
st.sidebar.write("**Filters**")
traffic_options = st.sidebar.multiselect("Traffic conditions:", ["Low", "Medium", "High", "Jam", "Unknown"], default=[])
city_options = st.sidebar.multiselect("City types:", ["Metropolitan", "Urban", "Semi-Urban", "Unknown"], default=[])
order_options = st.sidebar.multiselect("Order type:", ["Buffet", "Drinks", "Meal", "Snack"], default=[])
festival_options = st.sidebar.multiselect("During festivals:", ["Yes", "No", "Unknown"], default=[])
# Filters
df_clear = df_clear[(pd.to_datetime(df_clear["Time_Ordered"]).dt.date >= date_init) & (pd.to_datetime(df_clear["Time_Ordered"]).dt.date <= date_end)]
df_clear = df_clear[(df_clear["Delivery_person_Age"] >= age_min) & (df_clear["Delivery_person_Age"] <= age_max)]
df_clear = df_clear[(df_clear["Delivery_person_Ratings"] >= rate_min) & (df_clear["Delivery_person_Ratings"] <= rate_max)]
if traffic_options: df_clear = df_clear[df_clear["Road_traffic_density"].isin(traffic_options)]
if city_options: df_clear = df_clear[df_clear["City"].isin(city_options)]
if order_options: df_clear = df_clear[df_clear["Type_of_order"].isin(order_options)]
if festival_options: df_clear = df_clear[df_clear["Festival"].isin(festival_options)]
## Main page
# body
def viz1():
    st.title("Company View")
    tab1, tab2, tab3 = st.tabs(["Tactical", "Managerial", "Geographical"], )
    with tab1:
        with st.container(border=True):
            col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1], gap="small")
            comp_metrics = get_metrics_company(df_clear)
            with col1:
                st.metric("Total orders:", int(comp_metrics["total_deliveries"]), width="content")
                st.metric("Weekly mean:", int(comp_metrics["week_mean_deliveries"]), width="content")
            with col2:
                st.metric("Restaurants:", comp_metrics["restaurants"])
                st.metric("Weekly variability:", int(comp_metrics["week_std_dev_deliveries"]))
            with col3:
                st.metric("Delivery services:", comp_metrics["delivery_services"])
                st.metric("Mean weekly growth/decline:", int(comp_metrics["week_mean_diff_deliveries"]), f"{(comp_metrics["week_mean_diff_deliveries"] / comp_metrics["total_deliveries"]) * 100:.2f}%")
            with col4:
                st.metric("Mean orders per restaurant:", int(comp_metrics["mean_orders_per_restaurant"]))
                st.metric("Best week:", int(comp_metrics["week_max_deliveries"]), f"{((comp_metrics["week_max_deliveries"] - comp_metrics["week_mean_deliveries"]) / comp_metrics["week_mean_deliveries"]) * 100:.2f}%")
            with col5:
                st.metric("Mean orders per delivery service:", int(comp_metrics["mean_deliveries_per_service"]))
                st.metric("Worst week:", int(comp_metrics["week_min_deliveries"]), f"{-100 if np.isinf(((comp_metrics["week_min_deliveries"] - comp_metrics["week_mean_deliveries"]) / comp_metrics["week_mean_deliveries"]) * 100) else ((comp_metrics["week_min_deliveries"] - comp_metrics["week_mean_deliveries"]) / comp_metrics["week_mean_deliveries"]) * 100:.2f}%")
        with st.container():
            col1, col2 = st.columns([1, 1], gap="medium")
            with col1:
                st.plotly_chart(plot_orders_per_week(df_clear), use_container_width=True)
            with col2:
                st.plotly_chart(plot_weekly_orders_per_service(df_clear), use_container_width=True)
    with tab2:
        with st.container():
            st.plotly_chart(plot_orders_per_day(df_clear), use_container_width=True)
            col1, col2 = st.columns([1, 1], gap="medium")
            with col1:
                st.plotly_chart(plot_orders_by_traffic(df_clear), use_container_width=True)
            with col2:
                st.plotly_chart(plot_orders_by_traffic_and_city_type(df_clear), use_container_width=True)
    with tab3:
        with st.container():
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.write("Delivery central locations grouped by city type and traffic:")
                folium_static(plot_central_delivery_locations(df_clear), width=1024, height=600)
            with col2:
                st.write("Restaurant locations:")
                folium_static(plot_restaurant_locations(df_clear), width=1024, height=600)
            with col3:
                st.write("Orders HeatMap:")
                folium_static(plot_orders_heatmap(df_clear), width=1024, height=600)
    return None
                
def viz2():
    st.title("Delivery View")
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        del_metrics = get_metrics_deliveries(df_clear)
        with col1:
            st.metric("Lowest rating:", round(del_metrics["ratings_min"], 2))
            st.metric("Mean delivery distance:", f"{del_metrics["delivery_distance_mean"]:.1f} km")
        with col2:
            st.metric("Highest rating:", round(del_metrics["ratings_max"], 2))
            st.metric("Mean delivery time:", del_metrics["delivery_time_mean"])
        with col3:
            st.metric("Mean rating:", round(del_metrics["ratings_mean"], 2))
            st.metric("Max delivery time:", del_metrics["delivery_time_max"])
        with col4:
            st.metric("Median rating:", round(del_metrics["ratings_median"], 2))
            st.metric("Min delivery time:", del_metrics["delivery_time_min"])
        with col5:
            st.metric("Ratings variability:", round(del_metrics["ratings_std_dev"], 2))
            st.metric("Delivery time variability:", del_metrics["delivery_time_std_dev"])
    with st.container():
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(plot_deliveries_by_age(df_clear), use_container_width=True)
        with col2:
            st.plotly_chart(plot_deliveries_by_vehicle_condition(df_clear), use_container_width=True)
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            st.caption("Mean ratings by delivery service:")
            st.dataframe(get_mean_ratings_by_service(df_clear), use_container_width=True, height=560)
        with col2:
            st.caption("Mean ratings and variation by traffic:")
            st.dataframe(get_means_ratings_by_traffic(df_clear), use_container_width=True)
            st.caption("Mean ratings and variation by weather:")
            st.dataframe(get_mean_ratings_by_weather(df_clear), use_container_width=True)
    return None

def viz3():
    st.title("Restaurant View")
    with st.container(border=True):
        res_metrics = get_metrics_restaurants(df_clear)
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            st.metric("Mean order Pick-up time:", res_metrics["Pick_time_mean"])
        with col2:
            st.metric("Slowest order Pick-up time:", res_metrics["Pick_time_max"])
        with col3:
            st.metric("Fastest order Pick-up time:", res_metrics["Pick_time_min"])
        with col4:
            st.metric("Variation of order Pick-up time:", res_metrics["Pick_time_std_dev"])
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.caption("Mean Pick-up time by order:")
            st.dataframe(get_mean_pick_time_by_order(df_clear))
        with col2:
            st.caption("Mean Pick-up time by city type:")
            st.dataframe(get_mean_pick_time_by_city(df_clear))
        with col3:
            st.caption("Mean Pick-up time by traffic density:")
            st.dataframe(get_mean_pick_time_by_traffic(df_clear), height=177)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.caption("Top 10 fastest deliveries:")
            st.dataframe(get_top_10_fastest_deliveries(df_clear))
        with col2:
            st.caption("Top 10 fastest deliveries:")
            st.dataframe(get_top_10_fastest_deliveries(df_clear, reverse=True))
    return None

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
