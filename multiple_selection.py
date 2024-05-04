import pandas as pd
import sqlite3
import streamlit as st

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

# Verify column names in df_projects
st.write(df_projects.head())  # Print the first few rows to see column names

# Adjust the code to use the correct column name for years
selected_years = st.multiselect('Choose Years', df_projects['ActualYearColumnName'].unique())

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

# Sort by total contribution
sorted_df = grouped_df.sort_values(by='TotalContribution', ascending=False)

# Display the dataframe
st.write('Table of Partner Contributions per Country')
st.write(sorted_df, index=False)

# Save datasets as CSV files
st.text('Download the Data Below')

@st.cache
def convert_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

st.download_button(label='Download Partners CSV', data=convert_to_csv(sorted_df), file_name='partners.csv', mime='text/csv')

# Plot the graph with evolution of received grants per partners according to activityType
st.text('Graph with evolution of received grants per partners according to activityType')

# Filter data for the selected countries, years, and activity types
filtered_data = df_participants[df_participants['Country'].isin(selected_countries)]
filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]
filtered_data = filtered_data[filtered_data['ActivityType'].isin(selected_activity_types)]

# Group by activityType and sum the contributions
df_grants = filtered_data.groupby(['Country', 'Year', 'ActivityType'])['Contribution'].sum().reset_index()

# Plot the graph
for activity_type in selected_activity_types:
    data = df_grants[df_grants['ActivityType'] == activity_type]
    st.line_chart(data.set_index('Year')['Contribution'], use_container_width=True)

# Close the database connection
conn.close()











 
