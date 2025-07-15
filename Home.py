import streamlit as st
from PIL import Image

### Layout Streamlit
st.set_page_config(page_title="Curry Company - Home", page_icon="📈", layout="wide")
with open("./css/styles.css") as css:
        st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
## Sidebar
col1, col2, col3, col4 = st.sidebar.columns([0.5, 3, 2, 0.5])
with col2:
    curry_comp_logo = Image.open("./img/logo.png")
    st.image(curry_comp_logo, width=180)
with col3:
    st.markdown("# Curry Company")
    st.markdown("### Fastest in Town")
st.sidebar.markdown("""---""")
col1, col2, col3 = st.sidebar.columns([0.75, 2, 1])
with col2:
    lucas7x_logo = Image.open("./img/lucas7x.png")
    st.image(lucas7x_logo, width=180)
st.sidebar.write(
    """
    Ask for Help
    - E-mail: contato@lucas7x.win 
    - Discord: <a href="https://discord.com/users/515708003442491392">luc457x</a>
    - LinkedIn: <a href="https://www.linkedin.com/in/lucas-de-paula-teixeira-24148a177/">Lucas de Paula Teixeira</a>
    """,
    unsafe_allow_html=True
    )
## Main page
# body
st.title("Curry Company Growth Dashboard")
st.write(
    """
    This Growth Dashboard was built to track the growth metrics of Curry Company, a digital platform that connects Delivery Services and Restaurants.

    What this Growth Dashboard shows?
    - **Company View**:
        - Tactical View: Weekly growth indicators.
        - Managerial View: General behavior metrics.
        - Geographical View: Geolocation insights.
    - **Delivery Person View**:
        - Relevant metrics to track the performance of delivery services.
    - **Restaurant View**:
        - Relevant metrics to track the performance of restaurants.
    """
)
st.markdown("""---""")
st.write("*Powered by lucas7x*")