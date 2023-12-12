import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# :::::::::::::::::::::::::::::::::: PAGE CONFIGURATION ::::::::::::::::::::::::::::::::::
# test
# Settings for the webpage
st.set_page_config(
    page_title = "Sales",
    layout = "wide",
    page_icon = ":tangerine:",

)

# Image for the sidebar
# st.sidebar.image('images/orange_icon_2.png', use_column_width=True)

# Title for the page
st.title("🧾 Sales")

# :::::::::::::::::::::::::::::::::: DATA PLOTS AND TABLES ::::::::::::::::::::::::::::::::::

# :::::::::::::::::::::::::::::::::: HELPER FUNCTIONS ::::::::::::::::::::::::::::::::::

# Defining the excel MAIN_DATA_FILE directory constant
MAIN_DATA_DIR = 'Data/MAIN_DATA_FILE.xlsx'

# Function for opening specific tabs from the main excel file
def read_table_tabs(tab_name):
    tab_df = pd.read_excel(MAIN_DATA_DIR, sheet_name = tab_name)

    # with st.expander(f"{tab_name} Table"):
    #     st.write(tab_df)

    return tab_df 

CUSTOMERS_DF = read_table_tabs('Customer')
SUPPLIERS_DF = read_table_tabs('Supplier')
PRODUCT_DF = read_table_tabs('Product')
CUSTOMER_PRODUCT_DF = read_table_tabs('Customer - Product')
FINANCE_DF = pd.read_excel('Data/FinanceReport.xlsx')
# st.write(CUSTOMERS_DF)

round_colors = {
        -2: "#8ecae6",
        -1: "#219ebc",
        0: "#126782",
        1: "#023047",
        2: "#ffb703",
        3: "#fd9e02",
        4: "#8338ec",
        5: "#06d6a0"
    }

# :::::::::::::::::::::::::::::::::: IMPORTANT KPI's SECTION ::::::::::::::::::::::::::::::::::

st.divider()
st.subheader("Important KPI's")

def important_kpis():
    
    def static_plot(data, title):
        # Create a trace for the line chart
        trace = go.Scatter(
            x=data['rounds'], 
            y=data['values'], 
            mode='lines+markers',
            # text=data['values'],  # Set the text to display on markers
            # textposition='top center',
        )

        # Create a layout for the chart
        layout = go.Layout(
            title=title,
            xaxis=dict(title='Rounds'),
            yaxis=dict(title='')
        )

        # Create annotations to display values next to markers
        annotations = []
        for i, value in enumerate(data['values']):
            annotations.append(
                dict(
                    x=data['rounds'][i],
                    y=value,
                    xref='x',
                    yref='y',
                    text=f'<b>{str(value)}</b>',
                    showarrow=False,
                    font=dict(
                        size=12,
                    ),  
                    xanchor='center',  # Center text horizontally on marker
                    yanchor='bottom',  # Position text above the marker
                    yshift=10  # Adjust vertical position
                )
            )

        layout['annotations'] = annotations

        # Combine trace and layout to create the figure
        fig = go.Figure(
            data=[trace], 
            layout=layout
        )

        fig.update_traces(
            line=dict(width=4, color = 'orange'), 
            marker=dict(size=8, color = 'grey')
        )

        fig.update_layout(height=300)

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def finance_plot(val, plot_title):
        main_df = FINANCE_DF.copy().T.reset_index()
        main_df.columns = main_df.iloc[0]
        main_df = main_df.drop(0)

        main_df = main_df[['Round', val]]
        main_df.columns = ['Round', val]

        # st.write(main_df)

        main_df['Round'] = pd.to_numeric(main_df['Round'])
        main_df[val] = pd.to_numeric(main_df[val])

        if val == "ROI":
            main_df[val] = main_df[val] * 100

        fig = px.line(
            main_df, 
            x='Round', 
            y=val, 
            title=plot_title,
            line_shape='linear',
        )

        fig.update_layout(height=300)
        fig.update_xaxes(tickvals=sorted(main_df['Round'])) 
        fig.update_traces(line=dict(width=4, color='orange'), mode='lines+markers', marker=dict(size=8, color='grey'))

        # Annotations with rounded values
        annotations = []
        for i, row in main_df.iterrows():
            value_text = f"<b>{row[val]:.1f}</b>"  # Formatting the value to one decimal place
            annotations.append(
                dict(
                    x=row['Round'],
                    y=row[val],
                    xref='x',
                    yref='y',
                    text=value_text,
                    showarrow=False,
                    font=dict(size=12),
                    xanchor='center',
                    yanchor='bottom',
                    yshift=10
                )
            )

        fig.update_layout(annotations=annotations)

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)



        # main_df = FINANCE_DF.copy().T.reset_index()
        # main_df.columns = main_df.iloc[0]  # Set the first row as column names
        # main_df = main_df.drop(0)  # Drop the first two rows


        # main_df = main_df[['Round', val]]  # Select the 'Round' and the specified value column
        # main_df.columns = ['Round', val]   # Rename the columns for clarity

        # st.write(main_df)

        # main_df['Round'] = pd.to_numeric(main_df['Round'])
        # main_df[val] = pd.to_numeric(main_df[val])

        # # st.write(main_df)

        # if val == "ROI":
        #     main_df[val] = pd.to_numeric(main_df[val])*100
            
    
        # fig = px.line(
        #     main_df, 
        #     x='Round', 
        #     y=val, 
        #     title=plot_title, 
        #     # color_discrete_sequence=color_palette,
        #     line_shape = 'linear',
        # )

        
        # fig.update_layout(height=300)
        # fig.update_xaxes(tickvals=sorted(main_df['Round']))

        # fig.update_traces(line=dict(width=4, color = 'orange'), mode='lines+markers', marker=dict(size=8, color = 'grey'))

        # st.plotly_chart(fig, theme = "streamlit", use_container_width=True)


    data_obsolete_prod = {
        'rounds': ['-2', '-1', '0', '1', '2', '3', '4', '5'],
        'values': [11.8, 11.3, 11.3, 4.0, 9.0, 2.4, 0.9, 1.4],
    }

    data_service_level = {
        'rounds': ['-2', '-1', '0', '1', '2', '3', '4', '5'],
        'values': [95.1, 92.5, 92.5, 97.3, 95.0, 94.9, 87.4, 97.4],
    }


    col1, col2 = st.columns(2, gap = "small")

    with col1:
        finance_plot('ROI', 'ROI(%)')
        static_plot(data_obsolete_prod, 'Obsolete products (%)')
    with col2:
        finance_plot('Gross margin', 'Gross margin (customer)')
        static_plot(data_service_level, 'Service level outbound order lines (%)')

important_kpis()

# :::::::::::::::::::::::::::::::::: SERVICE LEVEL SECTION ::::::::::::::::::::::::::::::::::
st.divider() 
st.subheader('Service Level')

def service_level_section():
    
    def section_line_plots(col_name, title):
        main_df = CUSTOMERS_DF.copy()

        df_agg = main_df.groupby(['Customer', 'Round'], as_index = False)[col_name].sum()

        # st.write(df_agg)

        fig = go.Figure()

        # Iterate through unique customers to create traces for each customer
        for customer in df_agg['Customer'].unique():
            customer_data = df_agg[df_agg['Customer'] == customer]

            fig.add_trace(go.Scatter(
                x=customer_data['Round'],
                y=customer_data[col_name],
                mode='lines+markers',
                line = dict(width = 4),
                marker = dict(size = 8),
                name=customer,
                # title = title,
            ))

            fig.update_layout(
                title = title

            )

        if col_name != 'Attained contract index':
            fig.update_layout(
                    xaxis_title='Round',
                    yaxis_title=title,
                    yaxis=dict(
                        tickformat=".1%"  # Format y-axis ticks as percentages with two decimal places
                    )
            )

        st.plotly_chart(fig, theme = "streamlit", use_container_width=True)
       
    col1, col2 = st.columns(2, gap = "small")

    with col1:
        section_line_plots('Service level (order lines)','Service level (order lines)')

    with col2:
        section_line_plots('Service level (pieces)', 'Service level (pieces)')

    section_line_plots('Attained contract index', 'Attained contract index')

service_level_section()


# :::::::::::::::::::::::::::::::::: COMPONENTS SECTION :::::::::::::::::::::::::::::::::: 
st.divider()
st.subheader('Components')

def components_section():
    

    # round_colors = {
    #     -2: "#8ecae6",
    #     -1: "#219ebc",
    #     0: "#126782",
    #     1: "#023047",
    #     2: "#ffb703",
    #     3: "#fd9e02",
    #     4: "#8338ec"
    # }


    def section_bar_plots(col_name, plot_name):
        main_df = SUPPLIERS_DF.copy()

        df_agg = main_df.groupby(['Round', 'Component']).agg({col_name: 'mean'}).reset_index()
        df_agg[col_name] *= 100

        # st.write(df_agg)

        df_agg['Color'] = df_agg['Round'].map(lambda x: round_colors.get(x))

        fig = go.Figure()
        for round, data in df_agg.groupby('Round'):
            fig.add_trace(
                go.Bar(
                    x = data['Component'],
                    y = data[col_name],
                    name = round,
                    marker = dict(
                        color = round_colors[round]
                    ),
                )
            )
        
        fig.update_layout(
            title=plot_name,
            xaxis_title='Component',
            yaxis_title= col_name,
            legend_title='Component',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                title = '',

            ),
            showlegend=True,
            barmode='group'

        )

        fig.update_traces(
            texttemplate='<b>%{y:.0f}</b>',
            textposition='outside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


    col1, col2 = st.columns(2, gap = "small")

    with col1:
        section_bar_plots('Delivery reliability (%)', 'Delivery reliability (%) by Component'), 

    with col2:
        section_bar_plots('Rejection  (%)', 'Rejection (%) by Component')
        
components_section()


# :::::::::::::::::::::::::::::::::: PRODUCTIONS SECTION ::::::::::::::::::::::::::::::::::
st.divider()
st.subheader('Products')

def production_section():
    
    product_colors = {
        "Fressie Orange PET": "#264653",
        "Fressie Orange/C-power PET": "#2a9d8f",
        "Fressie Orange/Mango PET": "#8ab17d",
        "Fressie Orange 1 liter": "#e9c46a",
        "Fressie Orange/Mango 1 liter": "#f4a261",
        "Fressie Orange/Mango+C 1L": "#e76f51"
    }

    # round_colors = {
    #     -2: "#8ecae6",
    #     -1: "#219ebc",
    #     0: "#126782",
    #     1: "#023047",
    #     2: "#ffb703",
    #     3: "#fd9e02",
    #     4: "#8338ec"
    # }

    def product_section_bar_plots(col_name, plot_name):
        main_df = PRODUCT_DF.copy()

        df_agg = main_df.groupby(['Round', 'Product']).agg({col_name: 'mean'}).reset_index()
        df_agg[col_name] *= 100

        # st.write(df_agg)

        df_agg['Color'] = df_agg['Round'].map(lambda x: round_colors.get(x))

        fig = go.Figure()
        for round, data in df_agg.groupby('Round'):
            fig.add_trace(
                go.Bar( 
                    x = data['Product'],
                    y = data[col_name],
                    name = round,
                    marker = dict(
                        color = round_colors[round]
                    ),
                )

            )

        fig.update_layout(
            title = plot_name, 
            xaxis_title = 'Product',
            yaxis_title = col_name,
            legend = dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                title = '',
            ),
            showlegend = True,
            barmode = 'group'

        )

        fig.update_traces(
            texttemplate='<b>%{y:.0f}</b>',
            textposition='outside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)


    col1, col2 = st.columns(2, gap = "small")

    with col1:
        product_section_bar_plots('Service level (order lines)', 'Service level (%) by Product')

    with col2:
        product_section_bar_plots('Obsoletes (%)', 'Obsoletes (%) by Product')

production_section()


# ::::::::::::::::::::::::::::::::::CUSTOMERS SECTION ::::::::::::::::::::::::::::::::::
st.divider()
st.subheader('Customers')

def customers_section():

    # round_colors = {
    #     -2: "#8ecae6",
    #     -1: "#219ebc",
    #     0: "#126782",
    #     1: "#023047",
    #     2: "#ffb703",
    #     3: "#fd9e02"
    # }
    
    def customer_section_bar_plots(cust_name, col_name, plot_name):
        main_df = CUSTOMER_PRODUCT_DF.copy()
        main_df = main_df[main_df['Customer'] == cust_name]

        df_agg = main_df.groupby(['Customer', ' Product', 'Round']).agg({col_name: 'mean'}).reset_index()
        df_agg[col_name] *= 100

        # st.write(df_agg)

        df_agg['Color'] = df_agg['Round'].map(lambda x: round_colors.get(x))

        fig = go.Figure()
        for round, data in df_agg.groupby('Round'):
            fig.add_trace(
                go.Bar(
                    x = data[' Product'],
                    y = data[col_name],
                    name = round,
                    marker = dict(
                        color = round_colors[round]
                    ),
                )

            )
        
        fig.update_layout(
            title = plot_name,
            xaxis_title = 'Product',
            yaxis_title = col_name,
            legend = dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                title = '',
            ),
            showlegend = True,
            barmode = 'group'
        )

        fig.update_traces(
            texttemplate='<b>%{y:.2f}</b>',
            textposition='outside',
            marker=dict(
                line=dict(
                    width=1, color='DarkSlateGray'
                    )
                )
        )

        st.plotly_chart(fig, theme="streamlit", use_container_width=True)




    tab1, tab2, tab3 = st.tabs([
        "Always Best",
        "Top",
        "Colmart",
    ])

    with tab1:
        customer_section_bar_plots('Always Best','Additional sales as a result of promotions (%)', 'Additional sales as a result of promotions (%) | Always Best')

    with tab2:
        customer_section_bar_plots('Top','Additional sales as a result of promotions (%)', 'Additional sales as a result of promotions (%) | Top')

    with tab3:
        customer_section_bar_plots('Colmart','Additional sales as a result of promotions (%)', 'Additional sales as a result of promotions (%) | Colmart')

customers_section()

st.divider()
st.subheader("Tables utilized")

def show_table(df, name):
    with st.expander(f"{name} Table"):
        st.write(df)

show_table(CUSTOMERS_DF, 'Customers')
show_table(SUPPLIERS_DF, 'Supplier')
show_table(PRODUCT_DF, 'Product')
show_table(CUSTOMER_PRODUCT_DF, 'Customer - Product')
