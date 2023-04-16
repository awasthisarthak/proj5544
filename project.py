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
col3, space2, col4 = st.columns((10,1,10))

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

with col3:
    """Plots Line plot of CO2 emissions per capita by country and year"""

    #read in text file of all countries
    f = open('countries','r')
    data = f.read()
    countries = data.replace('\n', ',').split(",")

    #get mean co2 per capita for each country within our time span
    country_emissions = df[['co2_per_capita', 'country', 'year']][(df['year'] >= min_year) & (df['year'] <= max_year)]
    country_emissions = country_emissions.groupby(['country', 'year']).mean().reset_index()
    country_emissions = country_emissions.dropna()
    country_emissions.year = pd.to_datetime(country_emissions.year, format='%Y')

    #filter out non-country entries
    country_emissions = country_emissions[country_emissions.country.isin(countries)]

    #generate plotly figure
    fig = px.line(country_emissions, 
                  x="year", 
                  y="co2_per_capita", 
                  color='country', 
                  title= 'CO2 Emissions by Country',
                  markers=True,
                  width=1000,
                  height=500,
                  labels={'co2_per_capita': 'CO2 per capita', 'year': 'Year', 'country': 'Country'} 
                ) 
    
    st.plotly_chart(fig)

with col4:
    """ Plots Scatterplot of CO2 per capita by GDP by country"""

    #read in text file of all countries
    f = open('countries','r')
    data = f.read()
    countries = data.replace('\n', ',').split(",")

    #group data by country
    co2_gdp = df[['country', 'gdp', 'co2_per_capita']][(df['year'] >= min_year) & (df['year'] <= max_year)]
    co2_gdp = co2_gdp.groupby('country').mean().reset_index()
    co2_gdp = co2_gdp.dropna()

    #filter out non-country entries
    co2_gdp = co2_gdp[co2_gdp.country.isin(countries)]

    #plot scatterplot
    fig = px.scatter(co2_gdp, 
                    x="gdp", 
                    y="co2_per_capita", 
                    color="country",
                    title="Relationship between CO2 per Capita and GDP",
                    width=1000,
                    height=500,
                    labels={'co2_per_capita': 'CO2 per capita', 'gdp': 'GDP', 'country': 'Country'}
            ).update_layout(
                    xaxis_title='GDP (International $)', 
                    yaxis_title='CO2 Per Capita'
            )
    st.plotly_chart(fig)



