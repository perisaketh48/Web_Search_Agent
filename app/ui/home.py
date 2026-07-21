import streamlit as st
from app.config import constants
from app.ui.search import render_search
from app.ui.sidebar import render_sidebar
from app.telemetry.logfire_config import configure_logfire


def run_app():

    configure_logfire()

    st.set_page_config(
        page_title=constants.APP_NAME,
        layout="wide",
    )

    st.title(constants.APP_NAME)
    st.caption("Search the web. Get concise, source-backed answers.")
    st.divider()

    if "use_app_keys" not in st.session_state:
        st.session_state.use_app_keys = True

    if "gemini_api_key" not in st.session_state:
        st.session_state.gemini_api_key = ""

    if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = ""


    render_sidebar()
    render_search()