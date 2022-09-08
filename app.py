import streamlit as st
import pandas as pd
import numpy as np

DATA_URL= "Motor_Vehicle_Collisions.csv"


st.title("Motor Vehicle Collission in New York City")
st.markdown("This Application is a Streamlit dashboard that can be  to analyze motor vehicle collisions in NYC 🚗")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows = nrows, parse_dates=[['CRASH DATE','CRASH TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'],inplace =True)
    lowercase = lambda x: str(x).lower().replace(" ","_")
    data.rename(lowercase, axis ='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time':'date,time'})
    return data

data = load_data(1000)
st.header("Where are the most people injured in YC?")
injured_people = st.slider("Number of Injured",0,19)
st.map(data.query("number_of_persons_injured>= @injured_people")[['latitude','longitude']].dropna(how='any'))

if st.checkbox("Show row Data", False):
    st.subheader('Raw Data')
    st.write(data)
