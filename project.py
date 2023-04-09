import streamlit as st
import pandas as pd
import plotly.express as px

# Set page title and width
st.set_page_config(page_title='CO₂ Emissions Dashboard', page_icon=':chart_with_upwards_trend:', layout='wide')

# Set app header
st.header('CO₂ Emissions Dashboard')

# Load data
url = 'owid-co2-data.csv'
df = pd.read_csv(url, usecols=['country', 'year', 'iso_code', 'cumulative_luc_co2'])

# Create a slider to select a year
min_year = int(df['year'].min())
max_year = int(df['year'].max())
selected_year = st.slider('Select a year', min_value=min_year, max_value=max_year, value=1850)

# Filter data for the selected year
data = df[df['year'] == selected_year]

# Create two columns for the charts
col1, col2 = st.columns(2)

# Add choropleth map to the first column
with col1:
    fig = px.choropleth(data_frame=data,
                        locations='iso_code',
                        color='cumulative_luc_co2',
                        hover_name='country',
                        title=f'CO₂ Emissions Map ({selected_year})')
    st.plotly_chart(fig)

# Add bar chart to the second column
with col2:
    # Create a selectbox to select countries
    countries = st.multiselect('Select one or more countries', options=data['country'].unique())

    # Filter data for selected countries
    data = data[data['country'].isin(countries)]

    fig = px.bar(data_frame=data,
                 x='country',
                 y='cumulative_luc_co2',
                 color='country',
                 title=f'CO₂ Emissions Bar Chart ({selected_year})')
    st.plotly_chart(fig)