import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ::::::::::::::::: PAGE CONFIGURATION ::::::::::::::::: 
# Settings for the webpage
st.set_page_config(
    page_title = "Home",
    layout = "wide",
    page_icon = ":tangerine:",

)

# Image for the sidebar
# st.sidebar.image('images/orange_icon_2.png', use_column_width=True)

# Title for the page
st.title("Operations")
st.divider()

st.subheader("Table")
st.subheader("Graphs of important KPI's")

# ::::::::::::::::: DATA PLOTS AND TABLES ::::::::::::::::: 