import streamlit as st
import pandas as pd

# ::::::::::::::::: PAGE CONFIGURATION ::::::::::::::::: 
# Settings for the webpage
st.set_page_config(
    page_title = "Home",
    layout = "wide",
    page_icon = ":tangerine:",

)

# Image for the sidebar
st.sidebar.image('images/orange_icon_2.png', use_column_width=True)

# Title for the page
st.title("Finances")
st.divider()

# ::::::::::::::::: DATA PLOTS AND TABLES ::::::::::::::::: 

# Table for finances
finance_df = pd.read_excel('Data/FinanceReport.xlsx')
with st.expander("Finance Report data preview"):
    st.write(finance_df)

st.divider()
st.title("Graphs of important KPI's")