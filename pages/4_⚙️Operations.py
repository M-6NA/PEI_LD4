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
st.title("⚙️ Operations")

# :::::::::::::::::::::::::::::::::: HELPER FUNCTIONS ::::::::::::::::::::::::::::::::::

# Defining the excel MAIN_DATA_FILE directory constant
MAIN_DATA_DIR = 'Data/MAIN_DATA_FILE.xlsx' 

# Function for opening specific tabs from the main excel file
def read_table_tabs(tab_name):
    tab_df = pd.read_excel(MAIN_DATA_DIR, sheet_name = tab_name)

    # with st.expander(f"{tab_name} Table"):
    #     st.write(tab_df)

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

    # # Function for the OVERVIEW TAB
    # def cube_util_plot():
    #     main_df = WAREH_SALES_AREA_DF.copy()
    #     main_df['Cube utilization (%)'] = main_df['Cube utilization (%)'] * 100

    #     fig = px.line(
    #         main_df, 
    #         x='Round', 
    #         y='Cube utilization (%)', 
    #         color='Warehouse',
    #         title='Cube Utilization per Round for Each Warehouse',
    #         mode='lines+markers',
    #         line = dict(width = 4),
    #         marker = dict(size = 8),
    #     )
        
    #     fig.update_layout(
    #         xaxis_title='Round', 
    #         yaxis_title='Cube Utilization (%)',
    #     )

    #     # Show the plot
    #     st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    def cube_util_plot():
        main_df = WAREH_SALES_AREA_DF.copy()
        main_df['Cube utilization (%)'] = main_df['Cube utilization (%)'] * 100

        fig = go.Figure()

        for warehouse, data in main_df.groupby('Warehouse'):
            fig.add_trace(
                go.Scatter(
                    x=data['Round'],
                    y=data['Cube utilization (%)'],
                    mode='lines+markers',
                    name=warehouse,
                    line=dict(width=4),
                    marker=dict(size=8)
                )
            )

        fig.update_layout(
            xaxis_title='Round',
            yaxis_title='Cube Utilization (%)',
            title='Cube Utilization per Round for Each Warehouse',
            showlegend=True,
            barmode = 'group',
            legend=dict(
                orientation='h',
                yanchor='top',
                y=1.15,
                xanchor='left',
                x=0,
            )
        )

        # Show the plot
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    # def plot_stock_vs_demand_bars():
        # main_df = PRODUCT_WAREH_DF.copy()

        # # Filter main_df by the selected round value
        # filtered_df = main_df[main_df['Round'] == round_val]

        # # Create a grouped bar chart using Plotly Express
        # fig = go.Figure()

        # for metric in ['Demand per week (value)', 'Stock value']:
        #     fig.add_trace(
        #         go.Bar(
        #             x=filtered_df['Product'],
        #             y=filtered_df[metric],
        #             name=metric
        #         )
        #     )

        # fig.update_layout(
        #     barmode='group',
        #     xaxis_title='Product',
        #     yaxis_title='Value',
        #     title=f'Demand vs Stock Value by Round',
        #     legend=dict(
        #         orientation="h",  # Set the orientation to horizontal
        #         yanchor="bottom",
        #         y=1.02,
        #         xanchor="right",
        #         x=0.6
        #     ),
        # )

        # st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    def plot_stock_vs_demand_bars():

        # main_df = PRODUCT_WAREH_DF.copy()

        # # Grouping by 'Round' and summing the values
        # grouped_df = main_df.groupby('Round').agg({'Demand per week (value)': 'sum', 'Stock value': 'sum'}).reset_index()

        # custom_palette = ['#ef233c', '#8d99ae', '#2ca02c', '#d62728']

        # fig = go.Figure()

        # fig.add_trace(
        #     go.Bar(
        #         x=grouped_df['Round'],
        #         y=grouped_df['Demand per week (value)'],
        #         name='Demand per week (value)',
        #         color_discrete_sequence=custom_palette[0],
        #     )
        # )

        # fig.add_trace(
        #     go.Bar(
        #         x=grouped_df['Round'],
        #         y=grouped_df['Stock value'],
        #         name='Stock value'
        #     )
        # )

        # fig.update_layout(
        #     barmode='group',
        #     xaxis_title='Round',
        #     yaxis_title='Value',
        #     title='Total Demand vs Stock Value by Round',
        #     legend=dict(
        #         orientation="h",  # Set the orientation to horizontal
        #         yanchor="bottom",
        #         y=1.02,
        #         xanchor="right",
        #         x=0.6
        #     ),
        # )

        # st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        main_df = PRODUCT_WAREH_DF.copy()

        # Grouping by 'Round' and summing the values
        grouped_df = main_df.groupby('Round').agg({'Demand per week (value)': 'sum', 'Stock value': 'sum'}).reset_index()

        custom_palette = ['#ef233c', '#8d99ae', '#2ca02c', '#d62728']

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=grouped_df['Round'],
                y=grouped_df['Demand per week (value)'],
                name='Demand per week (value)',
                marker_color=custom_palette[0],  # Setting color for the first bar
            )
        )

        fig.add_trace(
            go.Bar(
                x=grouped_df['Round'],
                y=grouped_df['Stock value'],
                name='Stock value',
                marker_color=custom_palette[1],  # Setting color for the second bar
            )
        )

        fig.update_traces(
            texttemplate='<b>%{y:.0s}</b>',
            textposition='outside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        fig.update_layout(
            barmode='group',
            xaxis_title='Round',
            yaxis_title='Value',
            title='Total Demand vs Stock Value by Round',
            legend=dict(
                orientation="h",  # Set the orientation to horizontal
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=0.6
            ),
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


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


    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "Overview",
            "Round -2",
            "Round -1",
            "Round 0",
            "Round 1",
            "Round 2",
            "Round 3",
            "Round 4"
    ])

 
    with tab1:

        col1, col2 = st.columns(2, gap = "small")

        with col1:
            cube_util_plot()

        with col2:
            plot_stock_vs_demand_bars()

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
        # st.markdown(
        #     f"""
        #     <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
        #         <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: -2</h4></div>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )

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
        # st.markdown(
        #     f"""
        #     <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
        #         <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: -1</h4></div>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )

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
        # st.markdown(
        #     f"""
        #     <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
        #         <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: 0</h4></div>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )

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
        # st.markdown(
        #     f"""
        #     <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
        #         <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: 1</h4></div>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )


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
        # st.markdown(
        #     f"""
        #     <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
        #         <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: 2</h4></div>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )

    
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
        # st.markdown(
        #     f"""
        #     <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0; margin-top: 10px;">
        #         <div style="margin-bottom: -15px;"><h4 style = "color: black;">Products in finished goods warehouse | Round: 3</h4></div>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )

    with tab8:
        # Cube utilization text
        st.markdown(
            f"""
            <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                <div style="margin-bottom: -15px;"><h4 style = "color: black;">Cube utilization (%) | Round: 4</h4></div>
            </div>
            """,
            unsafe_allow_html=True
        ) 
        col1, col2, col3 = st.columns(3, gap = "small")

        with col1:
            plot_cube_util_gauge(4,'Raw materials warehouse')
        with col2:
            plot_cube_util_gauge(4,'Tank yard')
        with col3:
            plot_cube_util_gauge(4,'Finished goods warehouse')


def mixers_fillers_section():
    st.divider()
    st.subheader("Bottling and mixing")

    def plot_bottling_line_usage(round_number, bottling_line):
        
        main_df = BOTTLING_LINE_DF.copy()
        filtered_data = main_df[(main_df['Bottling line'] == bottling_line) & (main_df['Round'] == round_number)]

        
        if filtered_data.empty:
            st.write(f"No data found for Round{round_number}")
            return
        
        usage_columns = ['Run time (%)', 'Changeover time (%)', 'Breakdown time (%)', 'Unused capacity (%)']
        usage_data = filtered_data.iloc[0][usage_columns]
        overtime_value = round(filtered_data.iloc[0]['Overtime (%)'],2)

        fig = px.pie(
            values=usage_data.values,
            names=usage_data.index,
            title=f'{bottling_line} Usage for Round {round_number}',
            labels={'names': 'Usage Type'}
        )

        fig.update_layout(
            title_font=dict(size=20), 
            font=dict(size=17)
        )

        # Add overtime value to the legend
        fig.add_annotation(
            text=f'- Overtime: {overtime_value}%',
            x=1.25,
            y=0.6,
            showarrow=False,
            font=dict(size=17, color='black')
        )

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    # def plot_avg_lot_size_per_round():
        
    #     main_df = MIXERS_DF.copy()
    #     avg_lot_size_per_round = main_df.groupby('Round')['Average lot size'].mean().reset_index()

    #     fig = px.bar(
    #         avg_lot_size_per_round,
    #         x='Round',
    #         y='Average lot size',
    #         title='Mixer Average Lot Size per Round',
    #         labels={'Round': 'Round', 'Average lot size': 'Average Lot Size'},
    #         color_continuous_scale=px.colors.qualitative.Pastel, 
    #     )
 

    #     st.plotly_chart(fig, theme = "streamlit", use_container_width=True)
    
    def plot_avg_lot_size_per_round():
        main_df = MIXERS_DF.copy()
        avg_lot_size_per_round = main_df.groupby('Round')['Average lot size'].mean().reset_index()

        fig = go.Figure( 
            data=[
                go.Bar(
                    x=avg_lot_size_per_round['Round'],
                    y=avg_lot_size_per_round['Average lot size'],
                    marker=dict(color='#ff4d6d'),
                )
            ],
            layout=go.Layout(
                title='Mixer Average Lot Size per Round',
                xaxis=dict(title='Round'),
                yaxis=dict(title='Average Lot Size'),
            )
            
        )

        fig.update_traces(
            texttemplate='<b>%{y:.3s}</b>',
            textposition='outside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        fig.update_layout(barmode='group')

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    col1, col2 = st.columns(2, gap = "small")

    with col1:
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
                "Round -2",
                "Round -1",
                "Round 0",
                "Round 1",
                "Round 2",
                "Round 3",
                "Round 4",

        ])
        

        with tab1:
            plot_bottling_line_usage(-2, 'AllFill 1')
        
        with tab2:
            plot_bottling_line_usage(-1, 'AllFill 1')
           
        with tab3:
            plot_bottling_line_usage(0, 'AllFill 1')

        with tab4:
            plot_bottling_line_usage(1, 'AllFill 1')

        with tab5:
            plot_bottling_line_usage(2, 'AllFill 1')
            plot_bottling_line_usage(2, 'Double Dutch 1')

        with tab6:
            plot_bottling_line_usage(3, 'AllFill 1')

        with tab7:
            plot_bottling_line_usage(4, 'AllFill 1')

    with col2:
        plot_avg_lot_size_per_round()

warehouse_info_section()
mixers_fillers_section()

st.divider()
st.subheader("Tables utilized")

def show_table(df, name):
    with st.expander(f"{name} Table"):
        st.write(df)

show_table(WAREH_SALES_AREA_DF, 'Warehouse, Salesarea')
show_table(PRODUCT_WAREH_DF, 'Product - Warehouse')
show_table(MIXERS_DF, 'Mixers')
show_table(BOTTLING_LINE_DF, 'Bottling line')
show_table(PRODUCTS_DF, 'Product')

