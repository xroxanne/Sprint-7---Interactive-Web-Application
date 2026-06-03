'''Create virtual enviroment:
1. Create env: python3 -m venv .venv 
2. Activate environment: source .venv/bin/activate'''

import pandas as pd
import streamlit as st
import plotly.express as px

st.header("Data visualization with streamlit and plotly for vehicle data")
st.subheader("Data Filter")

# 1. Load and clean data
df = pd.read_csv('vehicles_us.csv')
# Year to int and drop rows with missing year
df_clean = df.dropna(subset=['model_year']).copy()
df_clean['model_year'] = df_clean['model_year'].astype(int)


def get_options(series):
    opts = series.sort_values().unique()
    return opts


# Get the options from the data for the dropdowns after cleaning the Data Frame
model_options = get_options(df_clean['model'])
year_options = get_options(df_clean['model_year'])

# Leave 'default=None' to indicate by defect everything is selected
model_selected = st.multiselect(
    "Select Model (Leave empty for ALL)",
    options=model_options,
    max_selections=5,
    default=None
)

year_selected = st.multiselect(
    "Select Model Year (Leave empty for ALL)",
    options=year_options,
    max_selections=5,
    default=None
)

# 2. Filter the logic
filter_df = df_clean.copy()

# If the user select specific models the code filters, If not, the data doesn't change.
if model_selected:
    filter_df = filter_df[filter_df['model'].isin(model_selected)]

# If the user selected specific years, the code filter. If not, we keep all.
if year_selected:
    filter_df = filter_df[filter_df['model_year'].isin(year_selected)]

st.subheader("Data Viewer")
# Show the number of rows to confirm that the filter works
st.write(f"Mostrando {filter_df.shape[0]} de {df.shape[0]} filas.")
st.dataframe(filter_df)

#Vehicle type by manufacturer
visual = px.bar(filter_df, x='model', color='type', title='Vehicle Type by Manufacturer')
st.plotly_chart(visual)


st.subheader('Condition vs Model Year')
build_histogram = st.checkbox('Select to Build Histogram')  # checkbox to build the histogram
if build_histogram:  # if the checkbox is selected build a histogram
#Histogram condition vs Model_year
    visual2 = px.histogram(filter_df, x='model_year', color='condition', title='Condition vs Model Year')
    st.plotly_chart(visual2)

st.subheader('Average Price by Vehicle Type')
build_barchart = st.checkbox('Select to Build Bar Chart')
if build_barchart:
    avg_price = filter_df.groupby('type')['price'].mean().reset_index()
    visual3 = px.bar(
        avg_price,
        x='type',
        y='price',
        title='Average Price by Vehicle Type'
    )
    st.plotly_chart(visual3)

st.subheader('Scatter Plot of Price vs Odometer Reading')
build_scatter = st.checkbox('Select to Build Scatter Plot')
if build_scatter:
    scatter_plot = px.scatter(
        filter_df,
        x='odometer',
        y='price',
        color='condition',
        hover_data=['model', 'model_year'],
        trendline='ols',
        title='Vehicle Price vs Odometer Reading')

    st.plotly_chart(scatter_plot)