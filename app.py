# Import necessary libraries
import pandas as pd
import numpy as np
import math as mt
import streamlit as st
import plotly.express as px

# Import Data
df = pd.read_csv("vehicles_us.csv")

# Rename model column to make_model to prepare for change
df = df.rename(columns={'model':'make_model'})

# Split items in make_model column and assign them to individual make and model columns
df['make'] = df['make_model'].str.split().str[0]
df['model'] = df['make_model'].str.split().str[1:]
# Above change leaves the model column as a series of lists. Below will concatenate the lists into single spaced strings
df['model'] = df['model'].apply(lambda x:' '.join(x))

# Fill null values
df['model_year'] = df['model_year'].fillna('N/A')
df['cylinders'] = df['cylinders'].fillna('N/A')
df['odometer'] = df['odometer'].fillna('N/A')
# Fill null values in is_4wd column with 0.00 to indicate no 4-wheel drive
df['is_4wd'] = df['is_4wd'].fillna(0.0)

# Streamlit Apps

# Create a text header above the dataframe
st.header('Data viewer') 
# display the dataframe with streamlit
st.dataframe(df)

# Create Vehicle types by manufacturer histogram
st.header('Vehicle type by Manufactuer')
fig = px.histogram(df, x='make',color='type')
# Display with streamlit
st.write(fig)

# Create Price versus Vehicle Color
st.header('Price by Vehicle Color')
color_map = df['paint_color'].unique()
fig = px.histogram(df, x='paint_color', y='price', 
                   color='paint_color',
                   color_discrete_map={'white':'white','red':'red','black':'black', 'blue':'blue', 'grey':'grey', 'silver':'silver', 'custom':'teal', 'orange':'orange', 'yellow':'yellow', 'brown':'brown', 'green':'green', 'purple':'purple'},
                   labels={'price':'price ($)','paint_color':'vehicle color'})
fig.update_layout(plot_bgcolor = 'tan')
st.write(fig)

# Create Price versus Days Listed

# Create price distribution
st.header('Compare price distribution between manufacturers')
# get a list of car manufacturers
manufac_list = sorted(df['make'].unique())
# get user's inputs from a dropdown menu
manufacturer_1 = st.selectbox(
                              label='Select Manufacturer 1', # title of the select box
                              options=manufac_list, # options listed in the select box
                              index=manufac_list.index('chevrolet') # default pre-selected option
                              )
# repeat for the second dropdown menu
manufacturer_2 = st.selectbox(
                              label='Select Manufacturer 2',
                              options=manufac_list, 
                              index=manufac_list.index('hyundai')
                              )
# filter the dataframe 
mask_filter = (df['make'] == manufacturer_1) | (df['make'] == manufacturer_2)
df_filtered = df[mask_filter]

# add a checkbox if a user wants to normalize the histogram
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

# create a plotly histogram figure
fig = px.histogram(df_filtered,
                      x='price',
                      nbins=30,
                      color='make',
                      histnorm=histnorm,
                      barmode='overlay')
# display the figure with streamlit
st.write(fig)

# Create Various Price Scatter
st.header('Price Scatter by Various')
x_list = ['model_year','odometer','days_listed']
x_select = st.selectbox(
                        label='Select data',
                        options=x_list,
                        index=x_list.index('model_year')
)
# Select Unique Options for each scatter plot
if x_select == 'model_year':
    color_select = ['blue']
    title_select = 'Price by Vehicle Year'
    label_select = {'price':'Price ($)','model_year':'Vehicle Year'}
elif x_select == 'odometer':
    color_select = ['green']
    title_select = 'Price by Mileage'
    label_select = {'price':'Price ($)','odometer':'Mileage (mi)'}
elif x_select == 'days_listed':
    color_select = ['brown']
    title_select = 'Price by Time Listed'
    label_select = {'price':'Price ($)','days_listed':'No. Days Listed'}
# Create Scatterplots
fig = px.scatter(df, x=x_select, y='price',
                 color_discrete_sequence=color_select,
                 title=title_select,
                 labels=label_select
                )
st.write(fig)