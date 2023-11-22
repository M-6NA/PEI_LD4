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

# :::::::::::::::::::::::::::::::::: HELPER FUNCTIONS ::::::::::::::::::::::::::::::::::

# Defining the excel MAIN_DATA_FILE directory constant
MAIN_DATA_DIR = 'Data/MAIN_DATA_FILE.xlsx'

# Function for openning specific tabs from the main excel file
def read_table_tabs(sheet_name):
    tab_df = pd.read_excel(MAIN_DATA_DIR, sheet_name = sheet_name)

    with st.expander(f"{sheet_name} Table"):
        st.write(tab_df)

    return tab_df

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

# Reading the Component tab in to the dataframe

# st.text("- Product Warehouse table")

st.text("- Rejection components(%)")
st.text("- Raw material costs(%)")
st.text("- Delivery reliability suppliers")

# Getting the tables from the main data file
component_df = read_table_tabs("Component")
supplier_df = read_table_tabs("Supplier")
supplier_component_df = read_table_tabs("Supplier - Component")

# Using the COMPONENT TABLE
# component_df ['Delivery reliability (%)'] = component_df ['Delivery reliability (%)'].str.rstrip('%').astype(float)

fig_component = px.line(component_df, 
                x='Round', 
                y='Delivery reliability (%)', 
                color='Component',
                title='Delivery Reliability across Rounds for Different Components',
                labels={'Round': 'Round', 'Delivery reliability (%)': 'Delivery Reliability (%)'},
                width=800, 
                height=500
)

fig_component.update_traces(mode='markers+lines') 


tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Overview", "Round -2", "Round -1", "Round 0", "Round 1", "Round 2", "Round 3"])

with tab1:
    st.plotly_chart(fig_component, theme = "streamlit", use_container_width=True)



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