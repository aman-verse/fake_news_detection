from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from config import APP_NAME

from components.sidebar import render_sidebar
from components.footer import render_footer

from views.home import show as show_home
from views.verify import show as show_verify
from views.history import show as show_history
from views.about import show as show_about

st.set_page_config(
    page_title=APP_NAME,
    page_icon="assets/images/tab_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "verification_started" not in st.session_state:
    st.session_state.verification_started = False

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "verification_input" not in st.session_state:
    st.session_state.verification_input = ""

if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""

if "verify_cache" not in st.session_state:
    st.session_state.verify_cache = {}

selected_page = render_sidebar()

if selected_page == "Home":

    show_home()

elif selected_page == "Verify News":

    show_verify()

elif selected_page == "History":

    show_history()

elif selected_page == "About":

    show_about()

render_footer()
