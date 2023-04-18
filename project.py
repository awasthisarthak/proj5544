import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page title and width
st.set_page_config(page_title='CO₂ Emissions Dashboard', page_icon=':chart_with_upwards_trend:', layout='wide')

# Set app header
st.header('CO₂ Emissions Dashboard')

# Load data
url = 'owid-co2-data.csv'
df = pd.read_csv(url, usecols=['country', 'year', 'iso_code', 'cumulative_luc_co2', 'co2_per_capita', 'gdp', 'population', 'primary_energy_consumption'])

#read in text file of all countries
f = open('countries','r')
d = f.read()
country_list = d.replace('\n', ',').split(",")

# Create a slider to select a year
min_year = 2008
max_year = int(df['year'].max())
selected_year = st.slider('Select a year', min_value=min_year, max_value=max_year, value=2011)

# Filter data for the selected year
data = df[df['year'] == selected_year]

# Create two columns for the charts
col1, col2 = st.columns([12, 8])
space1, col3, space2 = st.columns([3, 14, 3])
col5, space3, col6 = st.columns((12, 2, 8))

# Add choropleth map to the first column
with col1:
    # Plots Choropleth map of CO2 emissions per capita
    fig = px.choropleth(data_frame=data,
                        locations='iso_code',
                        color='co2_per_capita',
                        range_color=(0,25),
                        hover_name='country',
                        title=f'Map of CO₂ Emissions per Capita ({selected_year})',
                        color_continuous_scale=px.colors.sequential.Plasma,
                        width=1500, 
                        height=1000
                    )
    
    fig.update_layout(title_font_size=50,
                      coloraxis_colorbar_title_text = 'CO₂ Emissions per Capita',
                      coloraxis_colorbar_title_font_size = 25,
                      coloraxis_colorbar_tickfont_size = 20
                      )
    
    st.plotly_chart(fig)

# Add bar chart to the second column
with col2:
    # Plots bar chart showing country vs. population factor in terms of CO2 emissions per capita

    # Create a selectbox to select countries
    data = data[data.country.isin(country_list)]
    countries = st.multiselect('Select one or more countries', options=data['country'].unique())

    # Filter data for selected countries
    data = data[data['country'].isin(countries)]

    # Sort data by co2_per_capita in descending order
    data = data.sort_values('population', ascending=False)

    fig = px.bar(data_frame=data,
                 x='country',
                 y='population',
                 color='co2_per_capita',
                 range_color=(0,25),
                 title=f'Populations and CO₂ Emissions per Capita by Country ({selected_year})',
                 color_continuous_scale=px.colors.sequential.Plasma,
                 width=800,
                 height=800
                 ).update_layout(
                    xaxis_title='Country', 
                    yaxis_title='Population'
                )
    
    fig.update_layout(title_font_size=30,
                      coloraxis_colorbar_title_text = 'CO₂ Emissions per Capita',
                      coloraxis_colorbar_title_font_size = 25,
                      coloraxis_colorbar_tickfont_size = 20,
                      xaxis_tickfont_size=25,
                      xaxis_title_font_size=20,
                      yaxis_tickfont_size=25,
                      yaxis_title_font_size=20
                    )
    
    st.plotly_chart(fig)

with col3:
    # Plots bubble chart showing country vs. GDP vs. primary energy consumption, with population as bubble size.

    # Filter data for selected countries
    data_filtered = data[data['country'].isin(countries)]

    # Sort data by population in descending order
    data_filtered = data_filtered.sort_values('population', ascending=False)

    fig = px.scatter(data_frame=data_filtered,
                    x='gdp',
                    y='primary_energy_consumption',
                    size='population',
                    color='co2_per_capita',
                    range_color=(0, 25),
                    size_max=100,
                    title=f'GDP vs. Primary Energy Consumption Bubble Chart ({selected_year})',
                    color_continuous_scale=px.colors.sequential.Plasma,
                    hover_name='country',
                    width=2000,
                    height=900
                    ).update_layout(
                        xaxis_title='GDP',
                        yaxis_title='Primary Energy Consumption'
                    )
    
    fig.update_layout(title_font_size=30,
                      coloraxis_colorbar_title_text = 'CO₂ Emissions per Capita',
                      coloraxis_colorbar_title_font_size = 25,
                      coloraxis_colorbar_tickfont_size = 20,
                      xaxis_tickfont_size=25,
                      xaxis_title_font_size=20,
                      yaxis_tickfont_size=25,
                      yaxis_title_font_size=20
                    )

    st.plotly_chart(fig)

with col5:
    # Plots Line plot of CO2 emissions per capita by country and year

    #get mean co2 per capita for each country within our time span
    country_emissions = df[['co2_per_capita', 'country', 'year']][(df['year'] >= min_year) & (df['year'] <= max_year)]
    country_emissions = country_emissions.groupby(['country', 'year']).mean().reset_index()
    country_emissions = country_emissions.dropna()
    country_emissions.year = pd.to_datetime(country_emissions.year, format='%Y')

    #filter out non-country entries
    country_emissions = country_emissions[country_emissions.country.isin(country_list)]

    #only get the top x countries with largest total co2 per capita summed
    top_x = 25
    top_x_countries = country_emissions[['country', 'co2_per_capita']].groupby('country').sum().reset_index()
    top_x_countries = top_x_countries.sort_values(by=['co2_per_capita'], ascending=False, ignore_index=True)[0:top_x].country
    top_x_countries = list(top_x_countries)
    country_emissions = country_emissions[country_emissions.country.isin(top_x_countries)]

    #generate plotly figure
    fig = px.line(country_emissions, 
                  x="year", 
                  y="co2_per_capita", 
                  color='country', 
                  title= f'Top {top_x} Countries with Largest CO₂ Emissions',
                  markers=True,
                  width=1500,
                  height=800,
                  labels={'co2_per_capita': 'CO2 per capita', 'year': 'Year', 'country': 'Country'} 
                ) 
    fig.update_traces(marker=dict(size=13))
    fig.update_layout(title_font_size=30,
                      xaxis_tickfont_size=25,
                      xaxis_title_font_size=20,
                      yaxis_tickfont_size=25,
                      yaxis_title_font_size=20,
                      legend_title_font_size=20
                    )
    
    st.plotly_chart(fig)

with col6:
    # Plots Scatterplot of CO2 per capita by GDP by country

    #group data by country
    co2_gdp = df[['country', 'gdp', 'co2_per_capita']][(df['year'] >= min_year) & (df['year'] <= max_year)]
    co2_gdp = co2_gdp.groupby('country').mean().reset_index()
    co2_gdp = co2_gdp.dropna()

    #filter out non-country entries
    co2_gdp = co2_gdp[co2_gdp.country.isin(country_list)]

    #plot scatterplot
    fig = px.scatter(co2_gdp, 
                    x="gdp", 
                    y="co2_per_capita", 
                    color="country",
                    title="Relationship between CO₂ Emissions per Capita and GDP",
                    width=900,
                    height=800,
                    labels={'co2_per_capita': 'CO2 per capita', 'gdp': 'GDP', 'country': 'Country'}
            ).update_layout(
                    xaxis_title='GDP (International $)', 
                    yaxis_title='CO2 Per Capita'
            )
    
    fig.update_traces(marker=dict(size=13))
    fig.update_layout(title_font_size=30,
                      xaxis_tickfont_size=25,
                      xaxis_title_font_size=20,
                      yaxis_tickfont_size=25,
                      yaxis_title_font_size=20,
                      legend_title_font_size=20
                    )
    st.plotly_chart(fig)


