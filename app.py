import streamlit as st

# MUST be the very first Streamlit command
st.set_page_config(
    page_title="AI Career Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar on landing page
)

# Initialize session state for routing
if "page" not in st.session_state:
    st.session_state.page = "home"

def switch_page(page_name):
    st.session_state.page = page_name

# Import pages
from pages.home import show_home
# We will import analyzer dynamically to avoid loading all ML models instantly

# Router Logic
if st.session_state.page == "home":
    show_home(switch_page)
elif st.session_state.page == "analyzer":
    from pages.analyzer import show_analyzer
    show_analyzer(switch_page)