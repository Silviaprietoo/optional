import pandas as pd
import numpy as np
import sqlite3
from sqlite3 import connect
import streamlit as st
from PIL import Image

# Connect to the database
conn = sqlite3.connect('ecsel_database.db')

# Read data from the database tables
df_projects = pd.read_sql('SELECT * FROM PROJECTS', conn)
df_participants = pd.read_sql('SELECT * FROM PARTICIPANTS', conn)
df_countries = pd.read_sql('SELECT * FROM COUNTRIES', conn)

# Define country acronyms dictionary
country_acronyms = {
    'Belgium': 'BE', 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany': 'DE', 
    'Estonia': 'EE', 'Ireland': 'IE', 'Greece': 'EL', 'Spain': 'ES', 'France': 'FR', 
    'Croatia': 'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT',
    'Luxembourg': 'LU', 'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 
    'Poland': 'PL', 'Portugal': 'PT', 'Romania': 'RO', 'Slovenia': 'SI', 'Slovakia': 'SK', 
    'Finland': 'FI', 'Sweden': 'SE'
}

# Title and image
st.title('Partner Search App')
image = Image.open('Logo-KDT-JU.webp')
st.image(image)

# Multiple selection for countries
selected_countries = st.multiselect('Choose Countries', sorted(country_acronyms.keys()))

# Multiple selection for years
selected_years = st.multiselect('Choose Years', df_projects['Year'].unique())

# Multiple selection for activity types
selected_activity_types = st.multiselect('Choose Activity Types', df_projects['ActivityType'].unique())

# Function to convert country name to acronym
def country_to_acronym(country_name):
    return country_acronyms.get(country_name)

# Filter data based on selected criteria
filtered_df = df_participants[df_participants['Country'].isin(selected_countries)]
filtered_df = filtered_df[filtered_df['Year'].isin(selected_years)]
filtered_df = filtered_df[filtered_df['ActivityType'].isin(selected_activity_types)]

# Group by organization and calculate total contribution
grouped_df = filtered_df.groupby(['OrganizationID', 'ShortName', 'ActivityType', 'OrganizationURL'])['Contribution'].sum().reset_index()
grouped_df.rename(columns={'Contribution': 'TotalContribution'}, inplace=True)

# Sort by total contribution for participants
sorted_df_participants = grouped_df.sort_values(by='TotalContribution', ascending=False)

# Display the dataframe for participants
st.write('Table of Partner Contributions per Country')
st.write(sorted_df_participants, index=False)

# Save datasets as CSV files for participants
st.text('Download the Data Below')

@st.cache
def convert_to_csv_participants(df):
    return df.to_csv(index=False).encode('utf-8')

st.download_button(label='Download Participants CSV', data=convert_to_csv_participants(sorted_df_participants), file_name='participants.csv', mime='text/csv')

# Generate a new dataframe with project coordinators
# Filter project coordinators
df_project_coordinators = df_participants[df_participants['Role'] == 'Coordinator']
df_project_coordinators = df_project_coordinators[df_project_coordinators['Country'].isin(selected_countries)]
df_project_coordinators = df_project_coordinators[df_project_coordinators['Year'].isin(selected_years)]
df_project_coordinators = df_project_coordinators[df_project_coordinators['ActivityType'].isin(selected_activity_types)]

# Display the dataframe for project coordinators
st.write('Table of Project Coordinators per Country')
st.write(df_project_coordinators[['ShortName', 'ActivityType', 'ProjectAcronym', 'Name']], index=False)

# Save datasets as CSV files for project coordinators
st.text('Download the Data Below')

@st.cache
def convert_to_csv_project_coordinators(df):
    return df.to_csv(index=False).encode('utf-8')

st.download_button(label='Download Project Coordinators CSV', data=convert_to_csv_project_coordinators(df_project_coordinators), file_name='project_coordinators.csv', mime='text/csv')

# Display a graph showing the evolution of received grants
# Filter data for the selected countries, years, and activity types
filtered_data = df_participants[df_participants['Country'].isin(selected_countries)]
filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]
filtered_data = filtered_data[filtered_data['ActivityType'].isin(selected_activity_types)]

# Group by activityType and sum the contributions
df_grants = filtered_data.groupby(['Year', 'ActivityType'])['Contribution'].sum().reset_index()

# Plot the graph
st.text('Graph with evolution of received grants per partners according to activityType')
for activity_type in selected_activity_types:
    data = df_grants[df_grants['ActivityType'] == activity_type]
    st.line_chart(data.set_index('Year')['Contribution'])

# Close the database connection
conn.close()













 
