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
        projection_type="equirectangular",
        showcoastlines=True,
        countrycolor="rgba(0, 0, 0, 0.2)", 
        coastlinecolor="rgba(0, 0, 0, 0.2)",
        showland=True,
        landcolor = "rgba(218, 223, 233, 0.4)"

    )
    fig.update_layout(height=600, margin={"r": 0, "t": 0, "l": 0, "b": 210})

    fig.update_layout(
        legend=dict(
            orientation='h',    # Horizontal orientation
            yanchor='bottom',   # Anchor to bottom of the plot
            y=0,             # Adjust this value to position the legend further down
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
                line=dict(
                    width=2, 
                    color='rgb(249, 190, 71, 0.5)', 
                    dash='dashdot'
                ),
                showlegend=False
            )
        )

        
    added_supplies = {}

    for index, row in map_df.iterrows():
        supply = row['Supply']
        
        text_sup = f"Name: {row['Name']}<br>" \
            f"Supply: {row['Supply']}<br>" \
            f"Country: {row['Country']}<br>" \
            f"Qlty: {row['Qlty']} <br>"\
            f"Deliveries: {row['Deliveries']}<br>"\
            f"AVG order size: {row['AVG_order_size']}<br>"\
            f"TansP mode: {row['TransP_mode']}<br>"\
            f"Trade unit: {row['Trade_unit']}<br>"

        # Check if the supply has already been added to the legend
        if supply not in added_supplies:
            added_supplies[supply] = True  # Mark the supply as added
            
            fig.add_trace(
                go.Scattergeo(
                    lon=[row['Longitude']],
                    lat=[row['Latitude']],
                    text=text_sup,
                    mode="markers",
                    marker=dict(
                        size=10,
                        color=supply_colors.get(row['Supply'], "grey"),
                        opacity=0.8,
                        symbol="circle",
                        line=dict(color='black', width=1)
                    ),
                    name=row['Supply']  # Use the supply instead of row['Name']
                )
            )
        else:
            # Add a trace without adding to the legend for subsequent occurrences of the same supply
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
                        symbol="circle",
                            line=dict(color='black', width=1)
                    ),
                    showlegend=False  # Do not add to legend
                )
            )


    # Display the map
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

def display_report(df):

    css_styles = """
            <style>
                .column1 {
                    background-color: rgb(244, 245, 247);
                    text-align: left;
                    border-radius: 10px;
                    padding-left: 20px;
                    margin-top: 40px;
                    padding-bottom: 10px;
                }

                .column1 h4 {
                    color: rgb(0, 0, 0, 1);
                    padding-top: 10px;
                }

                table {
                    width: 100%;
                    border: none!important;
                }


                th {
                    text-align: center;
                    font-size: 14px;
                }

                tr {
                    height: 10px;
                    font-size: 14px;
                }

                table, td, th{
                    border: none!important;
                }

                td, th {
                    border: none;
                    padding-top: 1px!important;

                }

                p {
                    margin: 0;
                }

                .right-align {
                    text-align: right;
                }

                .left-align {
                    text-align: left;
                }

                .center-align {
                    text-align: center;
                }

                .bold {
                    font-weight: bold;
                }

                .monospace {
                    font-family: 'Consolas', monospace;
                }

            </style>
        """

    table_header = "<div class='column1'><div style='margin-bottom: -35px;'><h4 class='bold monospace'>Round supplier report</h4></div><br><div style='margin-bottom:-10px; margin-top: -4px; padding-right: 20px; padding-top: -5px;'><table cellspacing='0' cellpadding='0'><tr><th class='bold left-align'>Trade unit</th><th class='bold right-align'>Order size</th><th class='bold right-align'>Purchases</th><th class='bold right-align'>Purchase value</th><th class='bold right-align'>Transport costs</th></tr>"
    
    color_mapping = {
        'Pack1L': 'rgb(135, 110, 168)',
        'PET': 'rgb(92, 154, 207)',
        'Orange': 'rgb(245, 158, 52)',
        'Mango': 'rgb(165, 213, 89)',
        'Vitamin C': 'rgb(249, 121, 125)'
    }

    table_rows = ""
    current_trade_unit = None
    for index, row in df.iterrows():
        if row['Trade unit'] != current_trade_unit:
            table_rows += f"<tr><th class='bold left-align'>{row['Trade unit']}</th></tr>"
            item_info = df.loc[df['Trade unit'] == row['Trade unit'], ['Item', 'Order size', 'Purchases', 'Purchase value', 'Transport costs']]
            for _, item_row in item_info.iterrows():
                item_color = color_mapping.get(item_row['Item'], 'black')  # Default color if not found in the mapping
                table_rows += f"<tr><td class='right-align monospace' style='font-weight: bold; color: {item_color};'>{item_row['Item']}</td><td class='right-align monospace'>{item_row['Order size']}</td><td class='right-align monospace'>{item_row['Purchases']}</td><td class='right-align monospace'>{item_row['Purchase value']}</td><td class='right-align monospace'>{item_row['Transport costs']}</td></tr>"
            current_trade_unit = row['Trade unit']

    table_footer = "</table></div></div>"

    # Construct the complete HTML table
    table_html = f"{css_styles}{table_header}{table_rows}{table_footer}"

    # Display the HTML table in Streamlit using markdown
    st.markdown(table_html, unsafe_allow_html=True)

def display_quant_per_unit():
        st.markdown(
        f"""
        <div class="column1" style="background-color: #f4f5f7; text-align: center; border-radius: 10px; padding-left: 10px; padding-top: 5px; margin-top: 10px;">
            <p style="text-align: left; font-weight: bold; font-family: 'Consolas', monospace;">Quantities per Unit: </p>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); grid-gap: 10px;">
                <div style="font-weight: normal; font-family: 'Consolas', monospace; font-size: 15px; text-align: left;">Content drum (liter): <span style="color: #5eb889;">250</span></div>
                <div style="font-weight: normal; font-family: 'Consolas', monospace; font-size: 15px; text-align: left;">Content IBC (liter): <span style="color: #5eb889;">1,000</span></div>
                <div style="font-weight: normal; font-family: 'Consolas', monospace; font-size: 14px; text-align: left;">Content tank truck (liter): <span style="color: #5eb889;">30,000</span></div>
                <div style="font-weight: normal; font-family: 'Consolas', monospace; font-size: 15px; text-align: left;">Pallets per FTL: <span style="color: #5eb889;">30</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

added_sup_df = pd.read_excel('Data/Suppliers.xlsx')

round_0_data = added_sup_df[added_sup_df['Round'] == 0]
round_1_data = added_sup_df[added_sup_df['Round'] == 1]
round_2_data = added_sup_df[added_sup_df['Round'] == 2]
round_3_data = added_sup_df[added_sup_df['Round'] == 3]


st.subheader("Worldwide Suppliers")
# Displaying the maps in tabs for each round
tab1, tab2, tab3, tab4 = st.tabs(["Round 0", "Round 1", "Round 2", "Round 3"])

with tab1:

    col1, col2 = st.columns(2, gap = "small")
    
    with col1:
        display_world_map(round_0_data)

    with col2:

        data_0 = {
            'Trade unit':       ['Drum',        'Pallet',       'Pallet',       'Tank',         'IBC'],
            'Item':             ['Vitamin C',   'Pack1L',       'PET',          'Orange',       'Mango'],
            'Order size':       ['2,775',       '1,173,483',    '1,068,679',    '288,000',      '14,893'],
            'Purchases':        [5.3,            5.2,            5.3,            4.9,            5.2],
            'Purchase value':   ['€50,446' ,    '€160,052',     '€308,801',     '€737,683',     '€87,285'],
            'Transport costs':  ['€6,081',      '€8,797',       '€145,501',     '€69,102',      '€6,240']
        }

        data_round_0 = pd.DataFrame(data_0)

        display_report(data_round_0)

        display_quant_per_unit()
    
with tab2:

    col1, col2 = st.columns(2, gap = "small")
    
    with col1:
        display_world_map(round_1_data)

    with col2:

        data_1 = {
            'Trade unit':       ['Drum',        'Pallet',       'Pallet',       'Tank',         'IBC'],
            'Item':             ['Vitamin C',   'Pack1L',       'PET',          'Orange',       'Mango'],
            'Order size':       ['2,317',       '819,917',      '722,260',      '201,410',      '11,830'],
            'Purchases':        [6.1,            7.0,            7.3,            6.6,            6.3],
            'Purchase value':   ['€60,391' ,    '€151,176',     '€290,067',     '€689,303',     '€85,615'],
            'Transport costs':  ['€6,039',      '€8,683',       '€137,240',     '€64,966',      '€6,358']
        }

        data_round_1 = pd.DataFrame(data_1)

        display_report(data_round_1)

        display_quant_per_unit()

with tab3:

    col1, col2 = st.columns(2, gap = "small")
    
    with col1:
        display_world_map(round_2_data)
    with col2:

        data_2 = {
            'Trade unit':       ['Drum',        'Pallet',       'Pallet',       'Tank',         'Tank'],
            'Item':             ['Vitamin C',   'Pack1L',       'PET',          'Orange',       'Mango'],
            'Order size':       ['4,353',       '307,616',      '281,497',      '861,053',      '62,400'],
            'Purchases':        [3.8,            19.4,           20.3,            1.7,            1.5],
            'Purchase value':   ['€69,893' ,    '€160,776',     '€316,088',     '€738,763',     '€105,395'],
            'Transport costs':  ['€6,128',      '€12,944',      '€145,172',     '€68,544',      '€5,012']
        }

        data_round_2 = pd.DataFrame(data_2)

        display_report(data_round_2)

        display_quant_per_unit()

with tab4:

    col1, col2 = st.columns(2, gap = "small")
    
    with col1:
        display_world_map(round_3_data)
    with col2:
         
        data_3 = {
            'Trade unit':       ['Drum',        'Pallet',       'Pallet',       'Tank',     'Tank'],
            'Item':             ['Vitamin C',   'Pack1L',       'PET',          'Orange',   'Mango'],
            'Order size':       ['2,659',       '524,632',      '490,166',      '308,163',  '30,000'],
            'Purchases':        [5.2,           10.6,           10.9,           4.3,         2.5],
            'Purchase value':   ['€58,283',     '€149,106',     '€291,665',     '€682,471', '€86,240'],
            'Transport costs':  ['€5,460',      '€10,381',      '€132,654',     '€63,870',  '€4,398']
        }

        data_round_3 = pd.DataFrame(data_3)

        display_report(data_round_3)

        display_quant_per_unit()



# :::::::::::::::::::::::::::::::::: IMPORTANT KPI'S SECTION ::::::::::::::::::::::::::::::::::  
  
# :::::::::::::::::::::::::::::::::: HELPER FUNCTIONS ::::::::::::::::::::::::::::::::::

# Defining the excel MAIN_DATA_FILE directory constant
MAIN_DATA_DIR = 'Data/MAIN_DATA_FILE.xlsx'

# Function for opening specific tabs from the main excel file
def read_table_tabs(tab_name):
    tab_df = pd.read_excel(MAIN_DATA_DIR, sheet_name = tab_name)

    with st.expander(f"{tab_name} Table"):
        st.write(tab_df)

    return tab_df 

def plot_bar_charts_group(data, col_name, plot_name, mode):
    df = data.copy()

    # Define color mapping
    component_colors = {
        "Pack 1L": "#6a4c93",
        "PET": "#1982c4",
        "Orange": "#fb8500",
        "Mango": "#8ac926",
        "Vitamin C": "#ff595e"
    }

    df_agg = df.groupby(['Component', 'Round'], as_index = False)[col_name].sum()

    if col_name == 'Rejection  (%)':
        df_agg['Rejection  (%)'] = df_agg['Rejection  (%)'] * 100
        # st.write(df_agg)
    else:
        pass

    df_agg['Color'] = df_agg['Component'].map(lambda x: component_colors.get(x))


    # Grouped bar plot
    fig = go.Figure()
    for component, data in df_agg.groupby('Component'):
        fig.add_trace(go.Bar(
                x=data['Round'],
                y=data[col_name],
                name=component,
                marker=dict(color=component_colors[component])
            )
        )

    fig.update_layout(
            title=plot_name,
            xaxis_title='Round',
            yaxis_title= col_name,
            legend_title='Component',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            showlegend=True,
            barmode='stack'
    )

    if mode == 'stacked':
        fig.update_layout(
            barmode = 'stack'
        )
    elif mode == 'grouped': 
        fig.update_layout(
            barmode = 'group'
        )

    if col_name == 'Order lines previous round':
        fig.update_traces(
            texttemplate='<b>%{y:.1f}</b>',
            textposition='outside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )
    
    elif col_name == 'Rejection  (%)':
        fig.update_traces(
            texttemplate='<b>%{y:.2f}%</b>',
            textposition='inside',
            textfont=dict(size=13),
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

    elif col_name == 'Stock (pieces or liters)':
        top_line = df_agg.groupby('Round')['Stock (pieces or liters)'].sum()

        fig.update_traces(
            texttemplate='<b>%{y:.3s}</b>',
            textposition='inside',
            textfont=dict(size=13),
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        fig.add_trace(go.Scatter(
            x=top_line.index,
            y=top_line.values,
            mode='lines',
            name='Top Line',
                line=dict(
                    color='red',
                    width=3,
                    dash = 'dashdot',
                ),
            hoverinfo='none'
        ))

    elif col_name == 'Stock (weeks)':
        fig.update_traces(
            texttemplate='<b>%{y:.1f}</b>',
            textposition='inside',
            textfont=dict(size=13),
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )


    elif col_name == 'Purchase  value previous round' or 'Transport costs by Rounds':
        fig.update_traces(
            texttemplate='<b>%{y:.3s}</b>',
            textposition='outside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )
    

    

    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

def plot_bar_charts_group2(data, col_name, plot_name, mode):
    df = data.copy()

    # Define color mapping
    component_colors = { 
        "Pack 1L": "#6a4c93",
        "PET": "#1982c4",
        "Orange": "#fb8500",
        "Mango": "#8ac926",
        "Vitamin C": "#ff595e"
    }

    df_agg = df.groupby(['Component', 'Round']).agg({col_name: 'mean'}).reset_index()
    df_agg[col_name] *= 100


    # Grouped bar plot
    fig = go.Figure()
    for component, data in df_agg.groupby('Component'):
        fig.add_trace(go.Bar(
                x=data['Round'],
                y=data[col_name],
                name=component,
                marker=dict(color=component_colors[component])
            )
        )

    if col_name == 'Delivery reliability (%)': 
        fig.add_shape(
            type="line",
            x0=df_agg['Round'].min()-0.5,
            y0=95,
            x1=df_agg['Round'].max()+0.5,
            y1=95,
            line=dict(
                color="rgba(0,0,0,0.5)", 
                width=2, 
                dash="dashdot"
            ),
        )
    elif col_name == 'Rejection  (%)':
         fig.add_shape(
            type="line",
            x0=df_agg['Round'].min()-0.5,
            y0=2,
            x1=df_agg['Round'].max()+0.5,
            y1=2,
            line=dict(
                color="rgba(0,0,0,0.5)", 
                width=2, 
                dash="dashdot"
            ),
        )


    fig.update_layout(
            title=plot_name,
            xaxis_title='Round',
            yaxis_title= col_name,
            legend_title='Component',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            showlegend=True,
    )

    if mode == 'stacked':
        fig.update_layout(
            barmode = 'stack'
        )
    elif mode == 'grouped': 
        fig.update_layout(
            barmode = 'group'
        )


    fig.update_traces(
        texttemplate='<b>%{y:.0f}%</b>',
        textposition='outside',
        marker=dict(
            line=dict(
                width=1, color='DarkSlateGray'
                )
            )
    )


    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

# :::::: ORDER LINES BY ROUNDS SECTION ::::::
st.divider()
st.subheader("Important KPI's")

SUPPLIER_DF = read_table_tabs('Supplier')
COMPONENT_DF = read_table_tabs('Component')

def order_lines_by_rounds_section():
    plot_bar_charts_group(SUPPLIER_DF, 'Order lines previous round', 'Order lines by Rounds', 'grouped')

order_lines_by_rounds_section()


# :::::: PURCHASE VALUE BY ROUNDS SECTION ::::::
st.divider()

def purchase_value_by_rounds_section():

    plot_bar_charts_group(SUPPLIER_DF, 'Purchase  value previous round', 'Purchase value by Rounds', 'grouped')

purchase_value_by_rounds_section()

# :::::: TRANSPORT COSTS BY ROUNDS SECTION ::::::
st.divider()

def transport_costs_by_rounds_section():
      plot_bar_charts_group(SUPPLIER_DF, 'Transport costs previous round', 'Transport costs by Rounds', 'grouped')

transport_costs_by_rounds_section()


# :::::: SUM OF REJECTION(%) BY ROUND AND COMPONENT SECTION ::::::
st.divider()

def sum_rejection_section():
   plot_bar_charts_group(SUPPLIER_DF, 'Rejection  (%)', 'Sum of Rejection(%) by Round and Component', 'stacked')


sum_rejection_section()


# :::::: SUM OF STOCK (PIECES OR LITERS) ... SECTION ::::::
st.divider()

def sum_of_stock_section():

   plot_bar_charts_group(COMPONENT_DF, 'Stock (pieces or liters)', 'Sum of Stock (pieces or liters) by Round and Component', 'stacked')

sum_of_stock_section()


# :::::: SUM OF STOCK (WEEKS) BY ROUND AND COMPONENT SECTION ::::::
st.divider()

def sum_of_stock_weeks_section():
    plot_bar_charts_group(COMPONENT_DF, 'Stock (weeks)', 'Sum of Stock (weeks) by Round and Component', 'stacked')

sum_of_stock_weeks_section()

# :::::: RAW MATERIAL COSTS% SECTION ::::::
st.divider()
st.subheader('Raw Material costs%? Where? In the finances table?')

# :::::: DELIVERY RELIABILITY% SECTION ::::::
st.divider()

plot_bar_charts_group2(SUPPLIER_DF, "Delivery reliability (%)", "Delivery Reliability (%) by Round and Component (\u2191)", 'grouped')


# :::::: REJECTION COMPONENTS% SECTION ::::::
st.divider()
plot_bar_charts_group2(SUPPLIER_DF, 'Rejection  (%)', 'Rejection (%) by Round and Component (\u2193)', 'grouped')






