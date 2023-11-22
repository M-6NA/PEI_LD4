import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# :::::::::::::::::::::::::::::::::: PAGE CONFIGURATION :::::::::::::::::::::::::::::::::: 
# Settings for the webpage
st.set_page_config(
    page_title = "Purchasing",
    layout = "wide",
    page_icon = ":tangerine:",

)

# st.sidebar.image('images/orange_icon_2.png', use_column_width=True)


# Title for the page
st.title("Purchasing")
st.divider()

# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES ::::::::::::::::::::::::::::::::::

# :::::: WORLD MAP SECTION ::::::
def supply_world_map():

    st.subheader("Worldwide Suppliers")

    def display_world_map(data_df):
        # Create a DataFrame
        map_df = pd.DataFrame(data_df)

        # Assigning colors to different supplies
        supply_colors = {
            "Pack": "#6a4c93",
            "PET": "#1982c4",
            "Orange": "#fb8500",
            "Mango": "#8ac926",
            "Vitamin C": "#ff595e"
        }

        # Plotly figure setup
        fig = go.Figure()

        # Update geos and layout
        fig.update_geos(
            showcountries=True,
            projection_type="natural earth",
            # projection_type = "orthographic",
        )
        fig.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})

        fig.update_layout(
            legend=dict(
                orientation='h',    # Horizontal orientation
                yanchor='bottom',   # Anchor to bottom of the plot
                y=1.05,             # Adjust this value to position the legend further down
                xanchor='left',     # Anchor to right side
                x=0                 # Anchor to right side of the plot
            )
        )

        # Add a dot for the Netherlands
        fig.add_trace(
            go.Scattergeo(
                lon=[4.8952],  # Longitude of the Netherlands
                lat=[52.3676],  # Latitude of the Netherlands
                text="Netherlands",
                mode="markers",
                marker=dict(
                    size=10,
                    color='blue',  # Color of the Netherlands dot
                    opacity=0.7,
                    symbol="circle"
                ),
                name="Netherlands"
            )
        )

        # Plot each product on the map and add arrows to the Netherlands
        for index, row in map_df.iterrows():

            # Add arrows from each location to the Netherlands
            fig.add_trace(
                go.Scattergeo(
                    lon=[row['Longitude'], 4.8952],
                    lat=[row['Latitude'], 52.3676],
                    mode='lines',
                    line=dict(width=2, color='rgba(255, 0, 110, 0.3)', dash='dashdot'),
                    showlegend=False
                )
            )

            
            text_sup = f"Name: {row['Name']}<br>" \
                    f"Supply: {row['Supply']}<br>" \
                    f"Country: {row['Country']}<br>" \
                    f"Qlty: {row['Qlty']} <br>"\
                    f"Deliveries: {row['Deliveries']}<br>"\
                    f"AVG order size: {row['AVG_order_size']}<br>"\
                    f"TansP mode: {row['TransP_mode']}<br>"\
                    f"Trade unit: {row['Trade_unit']}<br>"

            fig.add_trace(
                go.Scattergeo(
                    lon=[row['Longitude']],
                    lat=[row['Latitude']],
                    text=text_sup,
                    mode="markers",
                    marker=dict(
                        size=10,
                        color=supply_colors.get(row['Supply'], "grey"),
                        opacity=0.7,
                        symbol="circle"
                    ),
                    name=row['Name']
                )
            )


        # Display the map
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    
    added_sup_df = pd.read_excel('Data/Suppliers.xlsx')

    round_0_data = added_sup_df[added_sup_df['Round'] == 0]
    round_1_data = added_sup_df[added_sup_df['Round'] == 1]
    round_2_data = added_sup_df[added_sup_df['Round'] == 2]
    round_3_data = added_sup_df[added_sup_df['Round'] == 3]
 
    
    # Displaying the maps in tabs for each round
    tab1, tab2, tab3, tab4 = st.tabs(["Round 0", "Round 1", "Round 2", "Round 3"])
    
    with tab1:
        display_world_map(round_0_data)

    with tab2:
        display_world_map(round_1_data)

    with tab3:
        display_world_map(round_2_data)

    with tab4:
        display_world_map(round_3_data)

supply_world_map()

# :::::: IMPORTANT KPI'S SECTION ::::::  
def purchasing_tables():
    st.subheader("Important KPI's")


purchasing_tables()    



st.subheader("Graphs of important KPI's")

