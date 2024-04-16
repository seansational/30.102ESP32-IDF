import boto3
import boto3.dynamodb
import streamlit as st
import pandas as pd
from functools import reduce   # Only in Python 3, omit this in Python 2.x
from decimal import *

pump_activation = {}
humidity_levels = {}

ddb = boto3.resource('dynamodb')

table = ddb.Table('esp32c6_data')
response = table.scan(
    AttributesToGet=[
        'data', 'time',
    ],
    Limit=2,
)

print(response)
for iter, result in enumerate(response['Items']):
    pump_activation[iter] = reduce(lambda rst, x: rst * 10 + x, result['data']['pump_activated'].as_tuple().digits)
    humidity_levels[iter] = reduce(lambda rst, x: rst * 10 + x, result['data']['humidity'].as_tuple().digits)

pump_pd = pd.DataFrame(list(pump_activation.items()), columns=['iteration', 'pump activated'])
humidity_pd = pd.DataFrame(list(humidity_levels.items()), columns=['iteration', 'humidity'])

print(pump_pd)
print(humidity_pd)
# st.line_chart(pump_pd, y='pump activated', x='iteration')
# st.line_chart(humidity_pd, y='humidity', x='iteration')

