import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# :::::::::::::::::::::::::::::::::: PAGE CONFIGURATION :::::::::::::::::::::::::::::::::: 
# Settings for the webpage
st.set_page_config(
    page_title = "KPI's",
    layout = "wide",
    page_icon = ":tangerine:",

)

# st.sidebar.image('images/orange_icon_2.png', use_column_width=True)


# Title for the page
st.title("All KPI's")
st.divider()

# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES :::::::::::::::::::::::::::::::::: 
# :::::::::::::::: PURCHASING SECTION ::::::::::::::::  
st.subheader("Generic")

st.text("- ROI%")
st.text("- Gross Margin (customer)")
st.text("- Obsoloete products(%)")
st.text("- Service level outbound order lines")

st.divider()

# :::::::::::::::: PURCHASING SECTION ::::::::::::::::  
st.subheader("Purchasing")

st.text("- Rejection components(%)")
st.text("- Raw material costs(%)")
st.text("- Delivery reliability suppliers")

st.text("- Component table")

st.text("- Supplier table")
st.text("- Supplier Component table")
st.text("- Product Warehouse table")


st.divider()


# :::::::::::::::: OPERATIONS SECTION :::::::::::::::: 
st.subheader("Operations")

st.text("- Cube utilization raw materials warehouse")
st.text("- Cube utilization finished goods warehouse")
st.text("- Product plan adherence")

st.text("- Bottling line table")
st.text("- Mixers table")
st.text("- Warehosue salesarea table")
st.text("- Product table")

st.divider()

# :::::::::::::::: SALES SECTION :::::::::::::::: 
st.subheader("Sales")

st.text("- Gross margin (customer)")
st.text("- Obsolete products(%)")
st.text("- Service level outbound order lines")

st.text("- Customer table")
st.text("- Customer Product table")
st.text("- Salesarea Customer Production table")
st.text("- Distributor table")

st.divider()

# :::::::::::::::: SUPPLY CHAIN SECTION :::::::::::::::: 
st.subheader("Supply Chain")

st.text("- Availability components (%)")
st.text("- Stock components (weeks)")
st.text("- Stock products (week)")

st.text("- Component table")
st.text("- Supplier Component table")
st.text("- Product warehouse table")
st.text("- Distributor table")

st.divider()

# :::::::::::::::: FINANCES SECTION :::::::::::::::: 
st.subheader("Finances")

st.text("- Some finances KPI's")

st.divider()