import boto3
import boto3.dynamodb
import streamlit as st
import pandas as pd
from functools import reduce   # Only in Python 3, omit this in Python 2.x
from decimal import *
import plotly.express as px  # interactive charts
import plotly
from datetime import datetime
plotly.io.json.config.default_engine = 'orjson'

#streamlit page config setup
st.set_page_config(
page_title="Plant Stats",
page_icon="📊",
layout="wide",
)
st.title("Plant Statistics 📊")

#initalise dictionary for saving database entries
pump_activation = {}
humidity_levels = {}

#setup database access
ddb = boto3.resource('dynamodb')

table = ddb.Table('esp32c6_data')

#accessing table contents
response = table.scan(
    AttributesToGet=[
        'time',
        'data',
    ],
    # Limit=20,
)

#reading table contents in to preinitalised variables
for iter, result in enumerate(response['Items']):
    epoch = int(result['time']/1000)
    date_iter = datetime.fromtimestamp(epoch)
    pump_activation[date_iter] = reduce(lambda rst, x: rst * 10 + x, result['data']['pump_activated'].as_tuple().digits)
    humidity_levels[date_iter] = reduce(lambda rst, x: rst * 10 + x, result['data']['humidity'].as_tuple().digits)

#loading into dataframe for easy visualisation
pump_pd = pd.DataFrame(list(pump_activation.items()), columns=['date', 'pump activated'])
humidity_pd = pd.DataFrame(list(humidity_levels.items()), columns=['date', 'humidity'])
pump_pd.sort_values(by='date', ascending=True,inplace=True)
humidity_pd.sort_values(by='date', ascending=True,inplace=True)

#visualising data using plotly into streamlit app
st.markdown("### Watering Chart")
fig = px.line(
                data_frame=pump_pd, y="pump activated", x="date"
)
st.plotly_chart(fig,use_container_width=True)

st.markdown("### Soil Humidity Chart")
fig = px.line(
                data_frame=humidity_pd, y="humidity", x="date",range_y=[0,100]
)
st.plotly_chart(fig,use_container_width=True)

