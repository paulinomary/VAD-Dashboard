import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import re
import numpy as np


app = Dash(__name__)

# Sample data
all_cars = pd.read_csv('../dataset/cars_named.csv')

def extract_number(text):
    if pd.isna(text):  # Check for NaN before applying regex
        return 0
    match = re.search(r"\d+", text)
    return int(match.group(0)) if match else 0

def split_num(text):
    if pd.isna(text):  # Check for NaN before applying regex
        return 0.0
    
    return text.split()[0]

# Function to extract the weight in kg
def extract_kg(text):
    #print(text)
    if pd.isna(text):  # Check for NaN before applying regex
        return 0.0
    match = re.search(r'\((\d+)\s*', text)
    #print(match.group(1))
    return float(match.group(1)) if match else 0.0

# Function to extract the consumtion in l/100km
def extract_consumption(text):
    #print(text)
    if pd.isna(text):  # Check for NaN before applying regex
        return 0.0

    liters = text.split()[3]
    #print("space", liters)
    liters = liters.split("(")[1]
    #print("(", liters)
    return float(liters)

def get_first_year(text):
    #print(text)
    if pd.isna(text):  # Check for NaN before applying regex
        return 0
    match = re.search(r"\d+", text)
    #print(match.group(0))
    return int(match.group(0)) if match else 0

# Apply the function to the 'text' column

all_cars['Num_cylinders'] = all_cars['Cylinders'].apply(extract_number)
all_cars['Num_cylinders'] = all_cars['Num_cylinders'].astype(int)
all_cars['Displacement'] = all_cars['Displacement'].astype(float)
all_cars['Unladen Weight (kg)'] = all_cars['Unladen Weight'].apply(extract_kg)
all_cars['Acceleration 0-62 Mph (0-100 kph)'] = all_cars['Acceleration 0-62 Mph (0-100 kph)'].apply(split_num)
# all_cars['HP'] = all_cars['HP'].astype(float)
all_cars['Combined consumption (L/100Km)'] = all_cars['Combined mpg'].apply(extract_consumption)
#all_cars['First production year'] = all_cars['Production years'].apply(get_first_year)


all_cars.to_csv('cars_named.csv', index=False)

line_colors = ['#1865A5', '#76C1EF', '#f9d29f', '#EBA74C', '#DE3F47','#950E3F']
# color dict
comment = """custom_colors = {
                    'our_blue': '#1865A5',
                    'our_light_blue': '#76C1EF',
                    'our_yellow': '#f9d29f',
                    'our_orange': '#EBA74C',
                    'our_red': '#DE3F47',
                    'our_dark_red': '#950E3F'
                }"""


fig = go.Figure()

# fig.add_trace(
#     go.Parcoords(dimensions=all_cars, color='HP', line=dict(color='HP', colorscale='Viridis', showscale=True)),
# )

#max_time_acceleration = max(all_cars['Acceleration 0-62 Mph (0-100 kph)'])
#print(max_time_acceleration)

max_weight = max(all_cars['Unladen Weight (kg)'])
print(max_weight)

max_hp = max(all_cars['HP'])
print(max_hp)


fig.add_trace(
    go.Parcoords(
        line=dict(color=all_cars['HP'], colorscale='Viridis', showscale=True),
        dimensions=[
            dict(range=[0,40], label='Consumption (L/100Km)', values=all_cars['Combined consumption (L/100Km)']),
            dict(range=[0,15], label='Cylinders', values=all_cars['Num_cylinders']),
            dict(label='Displacement', values=all_cars['Displacement']),
            dict(range=[0, 4500], label='Weight (kg)', values=all_cars['Unladen Weight (kg)']),
            dict(range=[0,20], label='Acceleration', values=all_cars['Acceleration 0-62 Mph (0-100 kph)']),
            #dict(label='Year', values=all_cars['First production year']),
            dict(label='HP', values=all_cars['HP']),
        ]
    )
)

app.layout = html.Div(id='page-content', children=[
    html.H4('Top Speed Evolution by Year and Brand'),
    dcc.Graph(id="graph", figure=fig)
])


if __name__ == '__main__':
    app.run_server(debug=True)
