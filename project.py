import streamlit as st
import pandas as pd
import plotly.express as px

# Set page title and width
st.set_page_config(page_title='CO₂ Emissions Dashboard', page_icon=':chart_with_upwards_trend:', layout='wide')

# Set app header
st.header('CO₂ Emissions Dashboard')

# Load data
url = 'owid-co2-data.csv'
df = pd.read_csv(url, usecols=['country', 'year', 'iso_code', 'cumulative_luc_co2', 'co2_per_capita', 'gdp'])

# Create a slider to select a year
min_year = 2008
max_year = int(df['year'].max())
selected_year = st.slider('Select a year', min_value=min_year, max_value=max_year, value=2011)

# Filter data for the selected year
data = df[df['year'] == selected_year]

# Create two columns for the charts
col1, space, col2 = st.columns([10, 1, 10])

# Add choropleth map to the first column
with col1:
    fig = px.choropleth(data_frame=data,
                        locations='iso_code',
                        color='co2_per_capita',
                        range_color=(0,25),
                        hover_name='country',
                        title=f'CO₂ Emissions Map per Capita ({selected_year})',
                        color_continuous_scale='blues')
    st.plotly_chart(fig)

# Add bar chart to the second column
with col2:
    # Create a selectbox to select countries
    countries = st.multiselect('Select one or more countries', options=data['country'].unique())

    # Filter data for selected countries
    data = data[data['country'].isin(countries)]

    # Sort data by co2_per_capita in descending order
    data = data.sort_values('co2_per_capita', ascending=False)

    fig = px.bar(data_frame=data,
                 x='country',
                 y='co2_per_capita',
                 color='country',
                 title=f'CO₂ Emissions per Capita Bar Chart ({selected_year})')
    
    st.plotly_chart(fig)

col3, space2, col4, space3, col5 = st.columns((10,1,10,1,10))

with col3:

    # Get top 10 countries by co2_per_capita for the selected year range
    top_10_countries = df[(df['year'] >= min_year) & (df['year'] <= max_year)].nlargest(82, 'co2_per_capita')['country'].tolist()

    # Filter data for the top 10 countries
    data = df[df['country'].isin(top_10_countries)]

    # Create a line plot with markers for the top 10 countries
    fig = px.line(data_frame=data,
                x='year',
                y='co2_per_capita',
                color='country',
                title=f'Top 10 CO₂ Emissions per Capita (2008 - 2021)',
                markers=True,
                line_group='country',
                range_x=[min_year, max_year],
                range_y=[0, 50])
    st.plotly_chart(fig)

with col4:
    # Get the top 30 countries by GDP
    top_30_countries = df[df['year'] == max_year].nlargest(82, 'gdp')['country'].tolist()

    # Filter data for the top 30 countries and the selected year range
    data = df[(df['country'].isin(top_30_countries)) & (df['year'] >= min_year) & (df['year'] <= max_year)]

    # Create a scatter plot of GDP vs. cumulative LUC CO2 for the top 30 countries
    fig = px.scatter(data_frame=data,
                     x='cumulative_luc_co2',
                     y='gdp',
                     color='country',
                     hover_name='country',
                     title='Relationship between GDP and Cumulative LUC CO2 (Top 30 Countries)',
                     labels={'cumulative_luc_co2': 'Cumulative LUC CO2', 'gdp': 'GDP'},
                     trendline='ols')
    st.plotly_chart(fig)


