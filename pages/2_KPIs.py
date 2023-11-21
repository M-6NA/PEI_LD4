import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# :::::::::::::::::::::::::::::::::: PAGE CONFIGURATION :::::::::::::::::::::::::::::::::: 
# Settings for the webpage
st.set_page_config(
    page_title = "Home",
    layout = "wide",
    page_icon = ":tangerine:",

)

# st.sidebar.image('images/orange_icon_2.png', use_column_width=True)


# Title for the page
st.title("All KPI's")
st.divider()


# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES :::::::::::::::::::::::::::::::::: 
# :::::::::::::::: PURCHASING SECTION ::::::::::::::::  
st.subheader("Purchasing")
st.divider()

# :::::::::::::::: OPERATIONS SECTION :::::::::::::::: 
st.subheader("Operations")
st.divider()

# :::::::::::::::: SALES SECTION :::::::::::::::: 
st.subheader("Sales")
st.divider()

# :::::::::::::::: SUPPLY CHAIN SECTION :::::::::::::::: 
st.subheader("Supply Chain")
st.divider()

# :::::::::::::::: FINANCES SECTION :::::::::::::::: 
st.subheader("Finances")
st.divider()