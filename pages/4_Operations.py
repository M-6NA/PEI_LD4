import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ::::::::::::::::: PAGE CONFIGURATION ::::::::::::::::: 
# Settings for the webpage
st.set_page_config(
    page_title = "Operations",
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
st.divider()

# ::::::::::::::::: DATA PLOTS AND TABLES ::::::::::::::::: 

col1, col2, col3 = st.columns(3, gap = "small")

with col1:
    st.header("Column 1")

with col2:
    st.header("Column 2")

with col3:
    st.header("Column 3")
