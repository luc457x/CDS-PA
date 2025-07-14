import streamlit as st
from PIL import Image

### Layout Streamlit
st.set_page_config(page_title="Curry Company - Home", page_icon="📈", layout="wide")
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
st.write("<h1>Curry Company Growth Dashboard</h1>", unsafe_allow_html=True)
st.write(
    """
    Este Growth Dashboard foi construído para acompanhar as métricas de crescimento da companhia Curry Company, plataforma digital que une Entregadores e Restaurantes.
    Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Metricas relevantes para acompanhar a performance dos entregadores.
    - Visão Restaurante:
        - Metricas relevantes para acompanhar a performance dos restaurantes.
    """
)
st.markdown("""---""")
st.write("*Powered by lucas7x*")