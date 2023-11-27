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

# ::::::::::::::::: THINGS TO DO :::::::::::::::::
st.divider()
st.subheader("Things to do:")

st.markdown(
    """
    - ##### ~~`Cube utilization raw materials warehouse`~~ #####
    - ##### ~~`Cube utilization finished goods warehouse`~~ #####
    - ##### ~~`Warehouse salesarea table`~~ #####
        - ##### `Ratio between capacity and cube utilization` #####
        - ##### `Cost per free space` ##### 
    - ##### `Bottling line table` ##### 
    - ##### `Mixers table` ##### 
    - ##### `Product table` ##### 

    
    """
    
)

# :::::::::::::::::::::::::::::::::: HELPER FUNCTIONS ::::::::::::::::::::::::::::::::::

# Defining the excel MAIN_DATA_FILE directory constant
MAIN_DATA_DIR = 'Data/MAIN_DATA_FILE.xlsx'

# Function for opening specific tabs from the main excel file
def read_table_tabs(tab_name):
    tab_df = pd.read_excel(MAIN_DATA_DIR, sheet_name = tab_name)

    with st.expander(f"{tab_name} Table"):
        st.write(tab_df)

    return tab_df 


# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES :::::::::::::::::::::::::::::::::: 

# ::::::::::::::::: TABLE CONSTANTS FOR THE OPERATIONS PLOTS :::::::::::::::::
WAREH_SALES_AREA_DF = read_table_tabs('Warehouse, Salesarea')
PRODUCT_WAREH_DF = read_table_tabs('Product - Warehouse')
MIXERS_DF = read_table_tabs('Mixers')
BOTTLING_LINE_DF = read_table_tabs('Bottling line')
PRODUCTS_DF = read_table_tabs('Product')

# ::::::::::::::::: CUBE UTILIZATION ::::::::::::::::: 

def warehouse_info_section():

    st.divider()
    st.subheader("Warehousing")

    # Function for the OVERVIEW TAB
    def cube_util_plot():
        main_df = WAREH_SALES_AREA_DF.copy()
        main_df['Cube utilization (%)'] = main_df['Cube utilization (%)'] * 100

        fig = px.line(
            main_df, 
            x='Round', 
            y='Cube utilization (%)', 
            color='Warehouse',
            title='Cube Utilization per Round for Each Warehouse')
        
        fig.update_layout(xaxis_title='Round', yaxis_title='Cube Utilization (%)')

        # Show the plot
        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    # Function for plotting the gauge plot for warehouses
    def plot_cube_util_gauge(round_val, wh_name):
        
        main_df = WAREH_SALES_AREA_DF.copy()
        
        # st.code(wh_name)
        # Filter the DataFrame for the specified warehouse and round
        filtered_df = main_df[(main_df['Warehouse'] == wh_name) & (main_df['Round'] == round_val)]

        # Extract cube utilization percentage
        cube_utilization = filtered_df['Cube utilization (%)'].values[0]
        cube_utilization = cube_utilization * 100 

        # Extracting the capacity and usage values
        capacity = filtered_df['Capacity'].values[0]
        usage = round(filtered_df['Usage'].values[0], 2)
        order_lines_per_week = round(filtered_df['Orderlines per week'].values[0],2)
        pallets_tanks_per_week = round(filtered_df['Pallets/Tanks per week'].values[0],2)
        flexible_manpower = round(filtered_df['Flexible manpower (FTE)'].values[0], 2)


        # Create a Plotly gauge plot
        fig = go.Figure(go.Indicator( 
            mode = "gauge+number",
            value = cube_utilization,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"{wh_name}"},
            gauge = {
                'axis': {'range': [0, 100], 'visible': False},
                'bar': {'color': "#52b788"},
                'steps' : [
                    {'range': [0, 25], 'color': "white"},
                    {'range': [25, 50], 'color': "white"},
                    {'range': [50, 75], 'color': "white"},
                    {'range': [75, 100], 'color': "white"}],
                },
            number = {'suffix': '%'}
            )
        )
 
        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)


        st.markdown(
                f"""
                <div class="column1" style="background-color: rgba(233, 236, 239, 0.5); text-align: left; border-radius: 10px; padding-left: 20px; margin-top: -95px;">
                    <div style="margin-bottom: -35px;"><h4 style = "color: rgba(0, 0, 0, 1); padding-top: 10px;">Other information</h4></div>
                    <hr class="solid" style = "margin-right: 20px;">
                    <div style="margin-bottom: -35px; margin-top: -40px;"><h6 style = "color: rgba(0, 0, 0, 1); padding-top: 20px; font-weight: normal; font-family: 'Consolas', monospace;">- Capacity: {capacity}</h6></div>
                    <div style="margin-bottom: -35px; padding-top: 20px;"><h6 style = "color: black; font-weight: normal; font-family: 'Consolas', monospace;">- Usage: {usage}</h6></div>
                    <div style="margin-bottom: -35px; padding-top: 20px;"><h6 style = "color: black; font-weight: normal; font-family: 'Consolas', monospace;">- Orderlines/week: {order_lines_per_week}</h6></div>
                    <div style="margin-bottom: -35px; padding-top: 20px;"><h6 style = "color: black; font-weight: normal; font-family: 'Consolas', monospace;">- Pallets/Tanks/week: {pallets_tanks_per_week}</h6></div>
                    <div style="margin-bottom: -35px; padding-top: 20px;"><h6 style = "color: black; font-weight: normal; font-family: 'Consolas', monospace;">- Flexible manpower: {flexible_manpower}</h6></div>
                    <div style="margin-top: 0;"><h2 style="margin-top: -15px; font-weight: bold; color: black;"></h2></div>
                </div>
                """,
            unsafe_allow_html=True
        )

    def plot_stock_vs_demand_bars(round_val):

        main_df = PRODUCT_WAREH_DF.copy()

        # Filter main_df by the selected round value
        filtered_df = main_df[main_df['Round'] == round_val]

        # Create a grouped bar chart using Plotly Express
        fig = px.bar(filtered_df, x='Product', y=['Demand per week (value)', 'Stock value'],
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    barmode='group',
                    labels={'Product': 'Product', 'value': 'Value', 'variable': 'Metric'},
                    title=f'Demand vs Stock Value | Round: {round_val}')

        # Update the layout to place the legend inside the plot
        fig.update_layout(
            legend=dict(
                orientation="h",  # Set the orientation to horizontal
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.6
            )
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Overview",
            "Round -2",
            "Round -1",
            "Round 0",
            "Round 1",
            "Round 2",
            "Round 3"
    ])

 
    with tab1:
        cube_util_plot()

    with tab2:
        
        # Cube utilization text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Cube utilization (%) | Round -2</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3, gap = "small")

        with col1:
            plot_cube_util_gauge(-2,'Raw materials warehouse')
        with col2:
            plot_cube_util_gauge(-2,'Tank yard')
        with col3:
            plot_cube_util_gauge(-2,'Finished goods warehouse')

        # Products text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: -2</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2, gap = "small")

        with col1:
            plot_stock_vs_demand_bars(-2)
        with col2:
            st.header("Column 2")

    with tab3:
        # Cube utilization text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Cube utilization (%) | Round: -1</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3, gap = "small")

        with col1:
            plot_cube_util_gauge(-1,'Raw materials warehouse')
        with col2:
            plot_cube_util_gauge(-1,'Tank yard')
        with col3:
            plot_cube_util_gauge(-1,'Finished goods warehouse')
        
        # Products text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: -1</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        plot_stock_vs_demand_bars(-1)

    with tab4:
        # Cube utilization text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Cube utilization (%) | Round: 0</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3, gap = "small")

        with col1:
            plot_cube_util_gauge(0,'Raw materials warehouse')
        with col2:
            plot_cube_util_gauge(0,'Tank yard')
        with col3:
            plot_cube_util_gauge(0,'Finished goods warehouse')

        
        # Products text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: 0</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        plot_stock_vs_demand_bars(0)

    with tab5:
        # Cube utilization text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Cube utilization (%) | Round: 1</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3, gap = "small")

        with col1:
            plot_cube_util_gauge(1,'Raw materials warehouse')
        with col2:
            plot_cube_util_gauge(1,'Tank yard')
        with col3:
            plot_cube_util_gauge(1,'Finished goods warehouse')

        # Products text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: 1</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        plot_stock_vs_demand_bars(1)

    with tab6:
        # Cube utilization text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Cube utilization (%) | Round: 2</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        ) 
        col1, col2, col3 = st.columns(3, gap = "small")

        with col1:
            plot_cube_util_gauge(2,'Raw materials warehouse')
        with col2:
            plot_cube_util_gauge(2,'Tank yard')
        with col3:
            plot_cube_util_gauge(2,'Finished goods warehouse')

        # Products text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: 2</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        plot_stock_vs_demand_bars(2)
    
    with tab7:
        # Cube utilization text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Cube utilization (%) | Round: 3</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        ) 
        col1, col2, col3 = st.columns(3, gap = "small")

        with col1:
            plot_cube_util_gauge(3,'Raw materials warehouse')
        with col2:
            plot_cube_util_gauge(3,'Tank yard')
        with col3:
            plot_cube_util_gauge(3,'Finished goods warehouse')

        # Products text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: 3</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        )

        plot_stock_vs_demand_bars(3)


def mixers_fillers_section():
    st.divider()
    st.subheader("Mixing and bottling")

    def overview_pie_plot():
        pass

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "Overview",
            "Round -2",
            "Round -1",
            "Round 0",
            "Round 1",
            "Round 2",
            "Round 3"

    ])

    with tab1:
        pass
    
    with tab2:
        pass

    with tab3:
        pass

    with tab4:
        pass

    with tab5:
        pass

    with tab6:
        pass

    with tab7:
        pass

warehouse_info_section()

mixers_fillers_section()





