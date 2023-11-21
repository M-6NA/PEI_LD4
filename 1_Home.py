import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from PIL import Image

# :::::::::::::::::::::::::::::::::: PAGE CONFIGURATION :::::::::::::::::::::::::::::::::: 
# Settings for the webpage
st.set_page_config(
    page_title = "Home",
    layout = "wide",
    page_icon = ":tangerine:",

)

st.sidebar.image('images/orange_icon_2.png', use_column_width=True)


# Title for the page
st.title("The Fresh Connection Dashboard ")
st.divider()

# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES :::::::::::::::::::::::::::::::::: 

# ::::::::::::::::: PLOTLY WORLD MAP ::::::::::::::::: 
# st.title("World Map")
st.subheader("Worldwide suppliers")

# :::::::::::::: OLD MAP PLOT ::::::::::::::  

# fig = go.Figure(go.Scattergeo())
# fig.update_geos(
#     showcountries = True,
#     projection_type="natural earth"
#     # projection_type = "orthographic"

# )
# fig.update_layout(height = 400, margin={"r":0,"t":0,"l":0,"b":0})

# st.plotly_chart(fig, use_container_width=True)

# :::::::::::::: NEW MAP PLOT ::::::::::::::  
data = {
    "Name": [
        "Quick Pack", "Poly", "Grande", "Squeeze", "Mrs Mango",
        "Domanga", "CC best", "C plus"
    ],
    "Supply": [
        "Pack", "PET", "Orange", "Orange", "Mango",
        "Mango", "Vitamin C", "Vitamin C"
    ],
    "Country": [
        "Germany", "Italy", "USA", "Brazil", "Brazil",
        "Spain", "India", "France"
    ],
    "Qlty": [
        "Middle", "High", "High", "Middle", "Middle",
        "Middle", "High", "Middle"
    ],
    "ADR": [93, 95, 98, 95, 93, 93, 99, 93],
    "Latitude": [
        51.1657, 41.8719, 37.0902, -14.235, -20.5,  # Increased latitude difference
        40.4637, 20.5937, 46.6033
    ],
    "Longitude": [
        10.4515, 12.5674, -95.7129, -51.9253, -51.9253,
        -3.7492, 78.9629, 1.8883
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Assigning colors to different supplies
supply_colors = {
    "Pack": "#6a4c93",
    "PET": "#1982c4",
    "Orange": "#fb8500",
    "Mango": "#8ac926",
    "Vitamin C": "#ff595e"
}

# Plotly figure setup
fig = go.Figure(go.Scattergeo())

# Update geos and layout
fig.update_geos(
    showcountries=True,
    projection_type="natural earth",
    # projection_type = "orthographic",
)
fig.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Plot each product on the map
for index, row in df.iterrows():
    text = f"Name: {row['Name']}<br>" \
           f"Supply: {row['Supply']}<br>" \
           f"Country: {row['Country']}<br>" \
           f"Qlty: {row['Qlty']}<br>" \
           f"ADR(%): {row['ADR']}%"

    fig.add_trace(
        go.Scattergeo(
            lon=[row['Longitude']],  # Longitude of the country
            lat=[row['Latitude']],   # Latitude of the country
            text=text,
            mode="markers",
            marker=dict(
                size=10,
                color=supply_colors.get(row['Supply'], "grey"),  # Assign color based on supply
                opacity=0.7,
                symbol="circle"
            ),
            name=row['Name']
        )
    )

    fig.update_layout(
        height=600,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend=dict(
            yanchor="bottom",
            y=0.05  # Adjust this value to move the legend further down (0.05 moves it down slightly)
        )
    )

# Display the map
st.plotly_chart(fig, use_container_width=True)




# ::::::::::::::::: DEMAND & DELIVERY SECTION :::::::::::::::::   
def demand_delivery_section():
    # Code for bar charts
    def spliting_and_plotting(input_df, dem_company, del_company):
        # Coping the og dataframe
        company_df = input_df.copy()

        # Splitting the dataframe by company
        company_df = company_df[['Date', 'ProductName', f'{dem_company}', f'{del_company}']].copy()
        company_df = company_df[(company_df[f'{dem_company}'] != 0) | (company_df[f'{del_company}'] != 0)]

        # Calculating the FillRate and grouping by year
        company_df['Year'] = pd.to_datetime(company_df['Date']).dt.year
        company_df = company_df.groupby(['Year', 'ProductName']).apply(lambda x: round((x[f'{del_company}'].sum() / x[f'{dem_company}'].sum()) * 100, 2)).reset_index(name='FillRate')

        # Pivot the DataFrame to have separate columns for each year's fill rate
        pivot_df = company_df.pivot(index='ProductName', columns='Year', values='FillRate').reset_index()

        # Plotting the resulting dataframe
        fig = px.bar(
            pivot_df,
            x='ProductName',
            y=[2018, 2019, 2020],  # Separate columns for each year
            barmode='group',
            title=f'{dem_company.replace("Demand", "")}: Fill Rate by Product for Each Year',
            labels={'ProductName': 'Product Name', 'value': 'Fill Rate', 'variable': 'Year'},
            color_discrete_map={
                "2018": '#00b4d8',  
                "2019": '#0077b6', 
                "2020": '#ff8500'   
            }
        )

        fig.update_layout(
            xaxis={'type': 'category'},
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            plot_bgcolor='white'
        )

        return fig

    st.subheader("Demand & Delivery")
    # Table for Demand and delviery
    DemDil_df = pd.read_csv('Data/DemandDelivery_2.csv')
    # DemDil_df = load_data('Data/DemandDelivery_2.csv')
    with st.expander("Demand & Delivery data preview"):
        st.write(DemDil_df)

    always_fig = spliting_and_plotting(DemDil_df, 'DemandAlwaysbest', 'DeliveredAlwaysbest')
    top_fig = spliting_and_plotting(DemDil_df, 'DemandTop', 'DeliveredTop')
    colmart_fig = spliting_and_plotting(DemDil_df, 'DemandColMart', 'DeliveredColMart')


    tab1, tab2, tab3 = st.tabs(["Alwaysbest", "Top", "ColMart"])
    with tab1:
        # Bar plot for the COMPANY: Alwaysbest
        st.plotly_chart(always_fig, theme = "streamlit", use_container_width=True)

    with tab2:
        #  Bar plot for the COMPANY: Top
        st.plotly_chart(top_fig, theme = "streamlit", use_container_width=True)

    with tab3:
        # Bar plot for the COMPANY: ColMart
        st.plotly_chart(colmart_fig, theme = "streamlit", use_container_width=True)

demand_delivery_section()

# ::::::::::::::::: PRODUCTION SECTION :::::::::::::::::   
def production_section():
    st.divider()
    st.subheader("Production")
    production_df = pd.read_csv('Data/Production_(1).csv', delimiter = ';')

    # Cleaning the production dataframe
    production_df['ProductName'] = production_df['ProductName'].str.replace('Fressie Orange 1 l ', 'Fressie Orange 1 liter')\
                                   .str.replace('Fressie Orange 1L', 'Fressie Orange 1 liter')\
                                   .str.replace('Fressie Orange/Mango 1L', 'Fressie Orange/Mango 1 liter')
    production_df['ProductName'] = production_df['ProductName'].str.replace('0', 'O')
    production_df['ProductName'] = production_df['ProductName'].str.replace(r'(P)$', 'PET', regex = True)    


    with st.expander("Production data preview"):
        st.write(production_df)

    # Tabs for each product
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Overview", 
                                                        "Fressie Orange 1 liter", 
                                                        "Fressie Orange/Mango 1 liter", 
                                                        "Fressie Orange/Mango+C 1L", 
                                                        "Fressie Orange PET", 
                                                        "Fressie Orange/C-power PET", 
                                                        "Fressie Orange/Mango PET"])

    def production_overview(overview_df):
        
        # Calculate the average startup costs per product
        startup_costs = overview_df.groupby('ProductName')['StartupLoss'].mean().reset_index()

        # Calculate total obsoletes per product
        obsoletes = overview_df.groupby('ProductName')['Obsoletes'].sum().reset_index()

        fig_startup_costs = px.pie(
            startup_costs, 
            values = 'StartupLoss', 
            names = 'ProductName', 
        )

        # Define a different color palette
        custom_colors = px.colors.qualitative.Plotly  # Change this to any other color sequence from px.colors

        # Update the pie plot with the new color scheme
        fig_startup_costs.update_traces(marker=dict(colors=custom_colors))

        # Update layout to adjust font size for legends and text
        fig_startup_costs.update_layout(
            legend=dict(
                font=dict(size=16)  # Adjust the legend font size
            ),
            # showlegend=False,
            font=dict(size=16)  # Adjust the text font size
        )

        # Create a pie chart for total obsoletes
        fig_obsoletes = px.pie(
            obsoletes, 
            values='Obsoletes', 
            names='ProductName', 
        )

        fig_obsoletes.update_layout(
            legend=dict(
                font=dict(size=16)  # Adjust the legend font size
            ),
            font=dict(size=16)  # Adjust the text font size
        )


        col1, col2 = st.columns(2, gap = "small")
        with col1:
            st.subheader("Average Startup Costs per Product")
            st.plotly_chart(fig_startup_costs, theme = "streamlit", use_container_width=True)
        with col2:
            st.subheader("Total Obsoletes per Product")
            st.plotly_chart(fig_obsoletes, theme = "streamlit", use_container_width=True)
            
    def format_value(value):
        if value >= 1_000_000:
            return f'{round(value / 1_000_000, 2)}M'
        elif value >= 1_000:
            return f'{round(value / 1_000, 2)}k'
        else:
            return f'{round(value, 2)}' 

    def production_info(function_df, product):
        
        filtered_product = function_df[function_df['ProductName'] == product]
        filtered_product['Date'] = pd.to_datetime(filtered_product['Date'])
        filtered_product['Month'] = filtered_product['Date'].dt.to_period('M').dt.strftime('%Y-%m')

        # Average startup loss
        average_startup_loss = filtered_product['StartupLoss'].mean()
        formatted_startup_loss = format_value(average_startup_loss)
        
        # Total Obsoletes
        total_obsoletes = filtered_product['Obsoletes'].sum()
        formatted_obsoletes = format_value(total_obsoletes)

        # Total rejections
        total_rejections = filtered_product['Rejection'].sum()
        formatted_rejections = format_value(total_rejections)
    

        col1, col2, col3 = st.columns(3, gap = "small")

        with col1:
            st.markdown(
                f"""
                <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                    <div style="margin-bottom: -35px;"><h3>AVG Startup Loss:</h3></div>
                    <div style="margin-top: 0;"><h2 style="margin-top: -15px; font-weight: bold;">{formatted_startup_loss}</h2></div>
                </div>
                """,
                unsafe_allow_html=True
            )
        # st.subheader(f"AVG Startup Loss: {formatted_startup_loss}", divider = "orange") 

        with col2:

            st.markdown(
                f"""
                <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                    <div style="margin-bottom: -35px;"><h3>Total Obsololetes:</h3></div>
                    <div style="margin-top: 0;"><h2 style="margin-top: -15px; font-weight: bold;">{formatted_obsoletes}</h2></div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # st.subheader(f"Total Obsoletes: {formatted_obsoletes}", divider = "orange") 
        with col3:
            st.markdown(
                f"""
                <div class="column1" style="background-color: #e9ecef; text-align: center; border-radius: 10px; padding: 0;">
                    <div style="margin-bottom: -35px;"><h3>Total Rejected:</h3></div>
                    <div style="margin-top: 0;"><h2 style="margin-top: -15px; font-weight: bold;">{formatted_rejections}</h2></div>
                </div>
                """,
                unsafe_allow_html=True
            )
            # st.subheader(f"Total Rejected: {formatted_rejections}", divider = "orange")


        # Average StockEOD per week
        average_stock_per_month = filtered_product.groupby('Month')['StockEOD'].mean().reset_index()
        average_stock_per_month = average_stock_per_month.sort_values('Month') 


        fig = px.line(
            average_stock_per_month,
            x = 'Month',
            y = 'StockEOD',
            title = f'{product}: Average StockEOD per Month',
            # color_discrete_map={'Month': 'orange'},

        )
        fig.update_traces(line=dict(color='orange'))

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

    with tab1:
        production_overview(production_df)
        
    with tab2:
        production_info(production_df, 'Fressie Orange 1 liter')

    with tab3:
        production_info(production_df, 'Fressie Orange/Mango 1 liter')

    with tab4:
        production_info(production_df, 'Fressie Orange/Mango+C 1L')

    with tab5:
        production_info(production_df, 'Fressie Orange PET')

    with tab6:
        production_info(production_df, 'Fressie Orange/C-power PET')

    with tab7:
        production_info(production_df, 'Fressie Orange/Mango PET')

production_section()

# ::::::::::::::::: PRODUCTS SECTION :::::::::::::::::  
def products_section():

    # DATA OVERVIEW SECTION 
    st.divider()
    st.subheader("Products")
    products_df = pd.read_csv('Data/Products_(1).csv', delimiter = ';')
    products_df = products_df[:-3] # Droping the last 3 rows (Outliers)
    with st.expander("Products data preview"):
        st.write(products_df)
        
    # INFORMATION ABOUT THE PRODUCT
    def product_info(function_df, product, img):
        
        filtered_product = function_df[function_df['ProductName'] == product]
        
        if not filtered_product.empty:
            product_id = filtered_product['ProductID'].values[0]
            product_name = filtered_product['ProductName'].values[0]

            shelf_life = filtered_product['ShelfLifeInWeeks'].values[0]
            pallet_layer = filtered_product['NumberPerPalletLayer'].values[0]
            pallet_count = filtered_product['NumberPerPallet'].values[0]
            liters_per_pack = filtered_product['LitersPerPack'].values[0]
            
            orange_amount = round(filtered_product['AmountOrange'].values[0] * 100, 2)
            mango_amount = round(filtered_product['AmountMango'].values[0] * 100, 2)
            vitamin_c_amount = round(filtered_product['AmountVitaminC'].values[0] * 100, 2)
            water_amount = filtered_product['AmountWater'].values[0]
        
            sales_price_retail = filtered_product['SalesPriceRetail'].values[0]

        col1, col2, col3, col4 = st.columns([0.05, 0.45, 0.45, 0.05], gap = "small")

        with col1:
            pass
        with col2:
            # st.header(f"{product_name}")
            st.code(f"{product_name}| ID: {product_id}")
            image = Image.open(f'images/{img}')
            st.image(image)
        with col3:
            st.code("Product Information:")
            col_31, col_32 = st.columns([0.5, 0.5], gap = "small")

            with col_31:
                st.code(f"Shelf Life: {shelf_life} weeks")
                st.code(f"Nr. Per Pallet Layer: {pallet_layer}")
                st.code(f"Nr. Per Pallet: {pallet_count}")
                st.code(f"Liters Per Pack: {liters_per_pack}")

            with col_32:
                st.code(f"Amount of Orange: {orange_amount}%")
                st.code(f"Amount of Mango: {mango_amount}%")
                st.code(f"Amount of Vitamin C: {vitamin_c_amount}%")
                st.code(f"Amount of Water: {water_amount}%")

            st.code(f"Sales Price: {sales_price_retail}")


        with col4:
            pass

        
        

    tab1, tab2, tab3, tab4, tab5, tab6  = st.tabs(["Fressie Orange 1 liter", 
                                                    "Fressie Orange/Mango 1 liter", 
                                                    "Fressie Orange/Mango+C 1L", 
                                                    "Fressie Orange PET", 
                                                    "Fressie Orange/C-power PET", 
                                                    "Fressie Orange/Mango PET"])

    with tab1:
        product_info(products_df, 'Fressie Orange 1 liter', 'Fressie_Orange_1_liter_AI_removebg.png')
    with tab2:
        product_info(products_df, 'Fressie Orange/Mango 1 liter', 'Fressie_Orange_Mango_1_liter_AI-removebg.png')
    with tab3:
        product_info(products_df, 'Fressie Orange/Mango+C 1L', 'Fressie_Orange_Mango_C_1L_AI-removebg.png')
    with tab4:
        product_info(products_df, 'Fressie Orange PET', 'Fressie_Orange_1_liter_PET_AI-removebg.png')
    with tab5:
        product_info(products_df, 'Fressie Orange/C-power PET', 'Fressie_Orange_Cpower_AI-removebg.png')
    with tab6:
        product_info(products_df, 'Fressie Orange/Mango PET', 'Fressie_Orange_Mango_PET_AI-removebg.png')

products_section()


# ::::::::::::::::: PENALTIES PER CUSTOMER SECTION :::::::::::::::::  
def penalties_section():
    st.divider()
    st.subheader("Penalties per customer")

    cust_penal_df = pd.read_excel('Data/Penalties_per_customer_(1).xlsx', header = [0,1])
    with st.expander("Penalties per customer data preview"):
        st.write(cust_penal_df)
 
penalties_section()


# ::::::::::::::::: SHELFLIFE AND SERVICELEVEL VS CONTRACTINDEX SECTION :::::::::::::::::  
def shelflife_section():
    st.divider()
    st.subheader("Shelflife and servicelevel vs Contractindex")

shelflife_section()