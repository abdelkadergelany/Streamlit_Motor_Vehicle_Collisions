import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL= "Motor_Vehicle_Collisions.csv"


st.title("Motor Vehicle Collission in New York City")
st.markdown("This Application is a Streamlit dashboard that can be  to analyze motor vehicle collisions in NYC 🚗")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows = nrows, parse_dates=[['CRASH DATE','CRASH TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'],inplace =True)
    lowercase = lambda x: str(x).lower().replace(" ","_")
    data.rename(lowercase, axis ='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time':'date_time'},inplace =True)
    return data

data = load_data(1000)


st.header("Where are the most people injured in YC?")
injured_people = st.slider("Number of Injured",0,19)
st.map(data.query("number_of_persons_injured>= @injured_people")[['latitude','longitude']].dropna(how='any'))

st.header("How many collisions occur during a given time of day?")
hour = st.slider("Hour to look at", 0,23)
data =  data[data["date_time"].dt.hour == hour]

st.markdown("Vehicle collision betweem %i:00 and %i:00" % (hour,(hour+1)%24))


midpoint = (np.average(data['latitude']),np.average(data['longitude']))

st.write(pdk.Deck(
map_style="mapbox://styles/mapbox/light-v9",
initial_view_state={
"latitude":midpoint[0],
"longitude":midpoint[1],
"zoom":11,
"pitch":50,
},
layers = [
pdk.Layer(
"HexagonLayer",
data=data[['date_time','latitude', 'longitude']],
get_position = ['longitude','latitude'],
radius =  100,
extruded = True,
pickable=True,
elevation_scale = 4,
elevation_range = [0,1000],
),
],
))

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour,(hour+1)%24))
filtered = data[
(data['date_time'].dt.hour >= hour)& (data['date_time'].dt.hour<(hour + 1))
]
hist = np.histogram(filtered['date_time'].dt.minute, bins=60,range=(0,60))[0]
chart_data =  pd.DataFrame({'minute':range(60),'crashes':hist})
fig = px.bar(chart_data,x='minute',y='crashes', hover_data = ['minute','crashes'], height=400)
st.write(fig)


if st.checkbox("Show row Data", False):
    st.subheader('Raw Data')
    st.write(data)
