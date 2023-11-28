import streamlit as st
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ::::::::::::::::: PAGE CONFIGURATION ::::::::::::::::: 
# Settings for the webpage
st.set_page_config(
    page_title = "Finances",
    layout = "wide",
    page_icon = ":tangerine:",

)

# Image for the sidebar
# st.sidebar.image('images/orange_icon_2.png', use_column_width=True)

# Title for the page
st.title("Finances")
st.divider()

# ::::::::::::::::: DATA PLOTS AND TABLES ::::::::::::::::: 

# Table for finances
FINANCE_DF = pd.read_excel('Data/FinanceReport.xlsx')
with st.expander("Finance Report data preview"):
    st.write(FINANCE_DF)

# ::::::::::::::::: HELPER FUNCTIONS ::::::::::::::::: 

def plot_data(val_1, val_2):
    main_df = FINANCE_DF.copy().T.reset_index()
    main_df.columns = main_df.iloc[0]  # Set the first row as column names
    main_df = main_df.drop(0)  # Drop the first row

    selected_columns = [col for col in main_df.columns if val_1 in col]
    selected_columns += [val_2]  # Include the additional column

    main_df = main_df[['Round'] + selected_columns]  # Select 'Round' and the specified columns

    main_df.columns = ['Round'] + [col.split(' - ')[-1] for col in selected_columns]  # Rename columns for clarity

    for col in main_df.columns[1:]:
        main_df[col] = pd.to_numeric(main_df[col])

    fig = px.line(
        main_df,
        x='Round',
        y=main_df.columns[1:],  # Plot all columns except 'Round'
        title=f'{val_1} over Rounds',
        line_shape='linear',
    )

    fig.update_layout(height=400)
    fig.update_xaxes(tickvals=sorted(main_df['Round']))
    
    fig.update_traces(
        mode='lines+markers',
        line = dict(width = 4),
        marker = dict(size = 8),
    ) 

    # Set legend position to top left
    fig.update_layout(
        legend=dict(
            x=0, 
            y=1.20, 
            traceorder='normal', 
            orientation='h',
            title='',
        )
    )



    st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

def plot_data_2(val):
    main_df = FINANCE_DF.copy().T.reset_index()
    main_df.columns = main_df.iloc[0]  # Set the first row as column names
    main_df = main_df.drop(0)  # Drop the first two rows


    main_df = main_df[['Round', val]]  # Select the 'Round' and the specified value column
    main_df.columns = ['Round', val]   # Rename the columns for clarity

    # st.write(main_df)

    main_df['Round'] = pd.to_numeric(main_df['Round'])
    main_df[val] = pd.to_numeric(main_df[val])

    # st.write(main_df)

    if val == "ROI":
        main_df[val] = pd.to_numeric(main_df[val])*100

    # Generate a random color sequence
    # color_palette = random.sample(px.colors.qualitative.Plotly, 4)

    fig = px.line(
        main_df, 
        x='Round', 
        y=val, 
        title=f'{val} over Rounds', 
        # color_discrete_sequence=color_palette,
        line_shape = 'linear',
    )

    
    fig.update_layout(height=300)
    fig.update_xaxes(tickvals=sorted(main_df['Round']))

    fig.update_traces(line=dict(width=4, color = 'orange'), mode='lines+markers', marker=dict(size=8, color = 'grey'))

    st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

def plot_data_bar(val):
    main_df = FINANCE_DF.copy().T.reset_index()
    main_df.columns = main_df.iloc[0]  # Set the first row as column names
    main_df = main_df.drop(0)  # Drop the first row

    # Replace spaces and special characters in column names for easy plotting
    main_df.columns = main_df.columns.str.replace(' ', '_').str.replace('-', '_')

    # Plotting the Gross margin - Cost of goods sold - Purchase value across rounds
    fig = px.bar(
        main_df, 
        x=main_df.index, 
        y='Gross_margin___Cost_of_goods_sold___Purchase_value',
        title='Gross Margin - COGS - Purchase Value across Rounds',
        labels={'index': 'Round', 'Gross_margin___Cost_of_goods_sold___Purchase_value': 'Value'}
    )

    fig.update_layout(xaxis_title='Round', yaxis_title='Value')

    st.plotly_chart(fig)

def plot_data_h_bar(data, name):
    df = pd.DataFrame(data)

    # Melt the DataFrame to have a suitable format for the plot
    melted_df = df.melt(id_vars='Round', var_name='Purchase_Type', value_name='Value')

    # Plotting the horizontal clustered bar chart
    fig = px.bar(
        melted_df, 
        x='Value', 
        y='Purchase_Type', 
        color='Round', 
        orientation='h',
        title=f'Gross Margin - COGS - {name}',
        labels={'Value': 'Value', 'Purchase_Type': 'Purchase Type'})

    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_title='Value')
    st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

def plot_op_prof(keyword):

    main_df = FINANCE_DF.copy().transpose()
    main_df.columns = main_df.iloc[0]
    main_df = main_df.drop(main_df.index[0])
    
    # Filter duplicate columns based on the first occurrence
    main_df = main_df.loc[:, ~main_df.columns.duplicated()]

    selected_cols = [col for col in main_df.columns if keyword in col]

    # st.write(selected_cols)
    # Filter the DataFrame to get columns associated with the keyword
    keyword_data = main_df[selected_cols]

    # Extracting legend labels based on the characters after the last '-' character
    legend_labels = [col.split(' - ')[-1] for col in keyword_data.columns]

    # Create a Plotly figure
    fig = go.Figure()

    # Add traces (lines) for each column associated with the keyword
    for i, column in enumerate(keyword_data.columns):
            fig.add_trace(go.Scatter(
                    x=keyword_data.index, 
                    y=keyword_data[column], 
                    mode='lines+markers', 
                    name=legend_labels[i],
                    line = dict(width = 4),
                    marker = dict(size = 8),
                )
            )


    # Update layout
    fig.update_layout(
        xaxis_title='Round',
        yaxis_title='Operating Profit',
        title=f'Operating Profit for {keyword}',
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.15,
            xanchor='left',
            x=0,
        )
    )

    st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

def plot_invest(keyword):
    
    main_df = FINANCE_DF.copy().transpose()
    main_df.columns = main_df.iloc[0]
    main_df = main_df.drop(main_df.index[0])
    
    # Filter duplicate columns based on the first occurrence
    main_df = main_df.loc[:, ~main_df.columns.duplicated()]

    selected_cols = [col for col in main_df.columns if keyword in col]

    # st.write(selected_cols)
    # Filter the DataFrame to get columns associated with the keyword
    keyword_data = main_df[selected_cols]

    # Extracting legend labels based on the characters after the last '-' character
    legend_labels = [col.split(' - ')[-1] for col in keyword_data.columns]

    # Create a Plotly figure
    fig = go.Figure()

    # Add traces (lines) for each column associated with the keyword
    for i, column in enumerate(keyword_data.columns):
            fig.add_trace(go.Scatter(
                    x=keyword_data.index, 
                    y=keyword_data[column], 
                    mode='lines+markers', 
                    name=legend_labels[i],
                    line = dict(width = 4),
                    marker = dict(size = 8),
                )
            )


    # Update layout
    fig.update_layout(
        xaxis_title='Round',
        yaxis_title='Investment',
        title=f'Investments',
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.15,
            xanchor='left',
            x=0,
        )
    )

    st.plotly_chart(fig, theme = "streamlit", use_container_width=True)

# ::::::::::::::::: REALIZED REVENUE SECTION ::::::::::::::::: 
st.divider()
st.subheader("Revenue")

def realized_revenue_section():

    col1, col2 = st.columns(2, gap = "small")

    # plot_data('Contracted sales revenue - Contracted sales revenue')
    with col1:
        plot_data('Contracted sales revenue - Contracted sales revenue', 'Realized revenue - Contracted sales revenue')
    with col2:
        plot_data('Bonus or penalties - Contracted sales revenue', 'Realized revenue - Bonus or penalties')

    plot_data_2('Realized revenue')

realized_revenue_section()

# ::::::::::::::::: GROSS MARGIN SECTION ::::::::::::::::: 
st.divider()
st.subheader("Gross margin")

def gross_margin_section():

    col1, col2 = st.columns(2, gap = "small")

    # plot_data('Contracted sales revenue - Contracted sales revenue')
    with col1:
         # plot_data_2('Gross margin'
        data_1 = {
            'Round': ['-2', '-1', '0', '1', '2', '3'],
            'Total': [154869.9504, 160052.154, 160052.154, 151176.355, None, None],
            'Quick_Pack': [None, None, 160776.1067, 149105.8207, None, None],
            'WWP': [332034.7297, 308801.2769, 308801.2769, 290067.4128, None, None],
            'Poly': [None, None, 316087.8167, 291664.5286, None, None],
            'Grande': [721543.1878, 737682.5616, 737682.5616, 689302.9083, 738763.4526, 682471.1905],
            'Pure': [96580.2079, 87284.9423, 87284.9423, 85615.3402, None, None],
            'Vital': [55500.1878, 50446.2072, 50446.2072, 60391.3446, None, None],
            'Domanga': [None, None, None, None, 4899.8155, 2432.6749],
            'Mrs_Mango': [None, None, None, None, 100495.26, 83807.6832],
            'C_plus': [None, None, None, None, 951.6109, 173.4627],
            'CC_best': [None, None, None, None, 68941.7645, 58109.5643],
            'Purchase_value': [1360528.264, 1344267.142, 1344267.142, 1276553.361, 1390915.827, 1267764.925]
        }

        plot_data_h_bar(data_1, 'Purchase Value Across Rounds')

    with col2:
        data_2 = {
            'Round': ['-2', '-1', '0', '1', '2', '3'],
            'Bottling_lines_fixed_costs': [50000, 50000, 50000, 50000, 75000, 50000],
            'Permanent_employees': [300000, 300000, 300000, 300000, 560000, 400000],
            'Flexible_manpower': [87064.8116, 97585.1772, 97585.1772, 45219.4217, 26073.9423, 6707.1015],
            'Outsourcing': [17285.624, 24675.5827, 24675.5827, 1478.8449, 3511.3416, 237.2543],
            'Mixer_fixed_costs': [31250, 31250, 31250, 31250, 31250, 31250],
            'Mixer_variable_costs': [187140.7594, 189888.0379, 189888.0379, 187777.5949, 236710.2531, 245055.7594],
            'Production_costs': [672741.1951, 693398.7979, 693398.7979, 615725.8616, 932545.5372, 733250.1154],
            'Cost_of_goods_sold': [2033269.459,	2037665.94,	2037665.94,	1892279.223, 2323461.364, 2001015.041]

        }

        plot_data_h_bar(data_2, 'Production costs')

    

    plot_data_2('Gross margin')

gross_margin_section()

# ::::::::::::::::: OPERATING PROFIT SECTION ::::::::::::::::: 
st.divider()
st.subheader("Operating profit")

def operating_profit_section():
 
    col1, col2 = st.columns(2, gap = "small")

    with col1:
        plot_op_prof('Overhead')
        plot_op_prof('Distribution costs')
        

    with col2:
        plot_op_prof('Handling costs')
        plot_op_prof('Project costs')

    plot_data_2('Operating profit')

operating_profit_section()

# ::::::::::::::::: INVESTMENT SECTION ::::::::::::::::: 
st.divider()
st.subheader("Investment")

def investment_section():
    plot_invest('Investment')

investment_section()