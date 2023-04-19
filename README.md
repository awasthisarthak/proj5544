# Final Project: CSE 5544
Streamlit app dashboard (using Plotly.)

all code produced
all processed datasets + a link to the original dataset(s)
description of how the completed project corresponds to the proposal
a user's guide describing how to use your project
all source materials for your paper (including figures)


# Dataset

Original dataset can be found in owid-co2-data.csv. Dataset was obtained here https://github.com/owid/co2-data . 
Any dataset processing was done inside of project.py, which only involved selecting specific columns and filtering based on conditions. 

# Description

In our project proposal, we aimed to produce an efficient way to visualize global CO2 emissions in a way that incorporates population and economic data. Our goal was to enable accountability and transperancy by visualizing the data on CO2 emissions sourced from *Our World in Data*. To this extent, this repository contains all code and data needed to generate a dashboard that provides the user with interactivity on selecting for specific countries for which to compare global CO2 emissions. We also include summary figures that provide insight as to trends in CO2 emissions by country, year, and factor in additional information such as GDP (in international $) and population size.

# How to Run Project
1. `streamlit run project.py` 
2. Toggle timeline at top of dashboard to view CO2 emissions chloropleth map and bar chart by year.
3. Enter desired countries to compare populations for (timeline slider also controls the info displayed here). 
