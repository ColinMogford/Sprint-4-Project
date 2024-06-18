# Import necessary libraries
import pandas as pd
import numpy as np
import math as mt
import streamlit as st
import plotly.express as px
from scipy import stats as st

# Import Data
df = pd.read_csv('df_us.csv')

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
df['paint_color'] = df['paint_color'].fillna('N/A')
# Fill null values in is_4wd column with 0.00 to indicate no 4-wheel drive
df['is_4wd'] = df['is_4wd'].fillna(0.00)

# create a text header above the dataframe
st.header('Data viewer') 
# display the dataframe with streamlit
st.dataframe(df)