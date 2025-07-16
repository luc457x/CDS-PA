import streamlit as st
from PIL import Image

### Layout Streamlit
st.set_page_config(page_title="Curry Company - Home", page_icon="📈", layout="wide")
## Sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 465px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
col1, col2, col3, col4 = st.sidebar.columns([0.1, 3, 2, 0.5])
with col2:
    img = Image.open("./img/logo.png")
    st.image(img, width=190)
with col3:
    st.markdown("# Curry Company")
    st.markdown("### Fastest in Town")
st.sidebar.markdown("""---""")
st.sidebar.write(
    """
    Ask for Help
    - E-mail: contato@lucas7x.win 
    - Discord: <a href="https://discord.com/users/515708003442491392">luc457x</a>
    - LinkedIn: <a href="https://www.linkedin.com/in/luc457x/">Lucas de Paula Teixeira</a>
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
        <br>
    More info on <a href="https://github.com/luc457x/CDS_PA-Curry_Company">Project's GitHub Repository</a>
    """,
    unsafe_allow_html=True
)
st.markdown("""---""")
st.write("*Powered by lucas7x*")