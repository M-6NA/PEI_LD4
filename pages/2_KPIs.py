import streamlit as st
import os
import random

import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as pc
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
st.subheader("Generic information")

def generic_section():

    finance_df = pd.read_excel('Data/FinanceReport.xlsx')
    with st.expander("Finance Report data preview"):
        st.write(finance_df)

    def finance_plot(val):

        main_df = finance_df.copy().T.reset_index()
        main_df.columns = main_df.iloc[0]  # Set the first row as column names
        main_df = main_df.drop([0, 1])  # Drop the first two rows

        main_df = main_df[['Round', val]]  # Select the 'Round' and the specified value column
        main_df.columns = ['Round', val]  # Rename the columns for clarity

        main_df['Round'] = pd.to_numeric(main_df['Round'])
        main_df[val] = pd.to_numeric(main_df[val])

        if val == "ROI":
            main_df[val] = pd.to_numeric(main_df[val])*100
    
        # Generate a random color sequence
        color_palette = random.sample(px.colors.qualitative.Plotly, 4)

        fig = px.line(
            main_df, 
            x='Round', 
            y=val, 
            title=f'{val} over Rounds', 
            color_discrete_sequence=color_palette
        )

        fig.update_layout(height=300)

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    col1, col2 = st.columns(2, gap = "small")

    with col1:
        finance_plot("ROI")
        finance_plot("Operating profit")

    with col2:
        finance_plot("Gross margin")
        finance_plot("Investment")

generic_section()

# st.text("- ROI%")
# st.text("- Gross Margin (customer)")
# st.text("- Obsoloete products(%)")
# st.text("- Service level outbound order lines")

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

read_table_tabs('Bottling line')
read_table_tabs('Mixers')
read_table_tabs('Warehouse, Salesarea')
read_table_tabs('Product')

st.divider()

# :::::::::::::::: SALES SECTION :::::::::::::::: 
st.subheader("Sales")

st.text("- Gross margin (customer)")
st.text("- Obsolete products(%)")
st.text("- Service level outbound order lines")

read_table_tabs('Customer')
read_table_tabs('Customer - Product')
read_table_tabs('Salesarea - Customer - Product')
read_table_tabs('Distributor')

# st.text("- Customer table")
# st.text("- Customer Product table")
# st.text("- Salesarea Customer Production table")
# st.text("- Distributor table")

st.divider()

# :::::::::::::::: SUPPLY CHAIN SECTION :::::::::::::::: 
st.subheader("Supply Chain")

st.text("- Availability components (%)")
st.text("- Stock components (weeks)")
st.text("- Stock products (week)")

read_table_tabs('Component')
read_table_tabs('Supplier - Component')
read_table_tabs('Product - Warehouse')
read_table_tabs('Distributor')

# st.text("- Component table")
# st.text("- Supplier Component table")
# st.text("- Product warehouse table")
# st.text("- Distributor table")

st.divider()

