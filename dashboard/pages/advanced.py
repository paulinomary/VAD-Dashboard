import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, callback
import re
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

dash.register_page(__name__, path='/car-finder')

all_cars = pd.read_csv('dataset/cars_named.csv')

all_cars['Unnamed: 0'] = all_cars.index

# invert colot scale
RdBu = px.colors.sequential.RdBu
BuRd = RdBu[::-1]


def extract_number(text):
    if pd.isna(text):  # Check for NaN before applying regex
        return 0
    match = re.search(r"\d+", text)
    return int(match.group(0)) if match else 0

def split_num(text):
    if pd.isna(text):  # Check for NaN before applying regex
        return 0.0
    # if float raises an error, it means that the value is a string
    try:
        return float(text.split()[0])
    except:
        try:
            return float(text.split()[0].replace(',', '.'))
        except:
            return 0.0
    
    #return float(text.split()[0])

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

### RADAR CHARTS
def make_radar_chart(name, metrics, categories):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=metrics + metrics[:1],
        theta=categories + [categories[0]],
        fill='toself',
        name=name,
        line=dict(color='#DE3F47')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[-2,2]
            )),
        showlegend=False,
        title=name
    )
    return fig

def generate_radar_charts(cars_data, max_charts=100):
    charts = []
    num_charts = min(len(cars_data), max_charts)
    for i in range(num_charts):
        car_data = cars_data.iloc[i]
        name = car_data['Name']
        metrics = car_data[['HP', 'Unladen Weight (kg)', 'Acceleration 0-62 Mph (0-100 kph)']].values.flatten().tolist()
        chart = dcc.Graph(figure=make_radar_chart(name, metrics, ['HP', 'Unladen Weight (kg)', 'Acceleration (0-100 kph)']))
        charts.append(html.Div(chart, style={'display': 'inline-block', 'width': '20%'}))
    return html.Div(charts, style={'display': 'flex', 'flex-wrap': 'wrap'})


# Apply the function to the 'text' column

all_cars['Num_cylinders'] = all_cars['Cylinders'].apply(extract_number)
all_cars['Num_cylinders'] = all_cars['Num_cylinders'].astype(int)
all_cars['Displacement'] = all_cars['Displacement'].astype(float)
all_cars['Unladen Weight (kg)'] = all_cars['Unladen Weight'].apply(extract_kg)
all_cars['Acceleration 0-62 Mph (0-100 kph)'] = all_cars['Acceleration 0-62 Mph (0-100 kph)'].apply(split_num)
all_cars['HP'] = all_cars['HP'].astype(float)
all_cars['Combined consumption (L/100Km)'] = all_cars['Combined mpg'].apply(extract_consumption)
#all_cars['First production year'] = all_cars['Production years'].apply(get_first_year)
#print(all_cars['Production years'][0].split(', '))
all_cars['Production years'] = all_cars['Production years'].apply(lambda x: x.split(', '))

df_exploded = all_cars.explode('Production years')
df_exploded['Production years'] = df_exploded['Production years'].astype(int)

# Normalize the data for radar charts
all_cars_norm = all_cars.copy()
numeric_columns = all_cars_norm.loc[:, all_cars_norm.columns != 'Unnamed: 0'].select_dtypes(include=['number']).columns
imputer = SimpleImputer(strategy='mean')
all_cars_norm[numeric_columns] = imputer.fit_transform(all_cars_norm[numeric_columns])
scaler = StandardScaler()
all_cars_norm[numeric_columns] = scaler.fit_transform(all_cars_norm[numeric_columns])
#all_cars_norm.to_csv('cars_named_norm.csv', index=False)

#print(all_cars_norm.describe())


#all_cars.to_csv('cars_named.csv', index=False)

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

# max_weight = max(all_cars['Unladen Weight (kg)'])
# print(max_weight)

# max_hp = max(all_cars['HP'])
# print(max_hp)
first_row = all_cars[all_cars['Unnamed: 0'] == 0]
#print(first_row)
#print(first_row[['HP', 'Unladen Weight (kg)', 'Acceleration 0-62 Mph (0-100 kph)']])


fig.add_trace(
    go.Parcoords(
        line=dict(color=all_cars['HP'], colorscale=BuRd, showscale=True),
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

scatter_fig = px.scatter(all_cars, x='HP', y='Displacement', color='Company')

layout = html.Div(id='page-content', children=[
    html.H4('Top Speed Evolution by Year and Brand'),
    html.H6('Select the years of production:'),
    dcc.RangeSlider(
        id='start-year-dropdown',
        min=1910, 
        max=2024,
        step=1,
        marks={i: str(i) for i in range(1910, 2025, 10)},
        tooltip={"placement": "bottom", "always_visible": True}
    ),
    dcc.Graph(id="parallel_coords", figure=fig),
    dcc.Graph(id="scatter_test", figure=scatter_fig),
    html.Div(id="radar_charts")

])

# auxiliar var for the parallel coordinates plot brushing
par_coords_dimensions_dict = {
    0: 'Combined consumption (L/100Km)',
    1: 'Num_cylinders',
    2: 'Displacement',
    3: 'Unladen Weight (kg)',
    4: 'Acceleration 0-62 Mph (0-100 kph)',
    5: 'HP'
}

# CALLBACKS

@callback(
    Output('parallel_coords', 'figure'),
    Input('start-year-dropdown', 'value')
)

def update_parallel_coords(years):
    #print(years)
    if years is None:
        filtered_cars = all_cars
    else:
        years_to_filter = list(range(years[0], years[1] + 1))
        #print(years_to_filter)
        #df_exploded = all_cars.explode('Production years')

        # Step 2: Apply the filter
        #df_exploded['Production years'] = df_exploded['Production years'].astype(int)
        df_filtered = df_exploded[df_exploded['Production years'].isin(years_to_filter)]

        # Step 3: (Optional) Group back if needed, to get lists of years again
        agg_dict = {'Production years': list}

        agg_dict.update({col: 'first' for col in df_filtered.columns if col not in ['Production years', 'Unnamed: 0']})

        filtered_cars = df_filtered.groupby('Unnamed: 0').agg(agg_dict)#.reset_index()

    # Create a parallel coordinates plot based on the filtered
    #filtered_cars['HP'] = filtered_cars['HP'].dropna().astype(float)
    #filtered_cars.to_csv('filtered_cars.csv', index=False)
    fig = go.Figure()
    fig.add_trace(
        go.Parcoords(
            line=dict(color=filtered_cars['Combined consumption (L/100Km)'], colorscale=BuRd, showscale=True),
            dimensions=[
                dict(range=[0,40], label='Consumption (L/100Km)', values=filtered_cars['Combined consumption (L/100Km)']),
                dict(range=[0,15], label='Cylinders', values=filtered_cars['Num_cylinders']),
                dict(label='Displacement', values=filtered_cars['Displacement']),
                dict(range=[0, 4500], label='Weight (kg)', values=filtered_cars['Unladen Weight (kg)']),
                dict(range=[0,20], label='Acceleration', values=filtered_cars['Acceleration 0-62 Mph (0-100 kph)']),
                #dict(label='Year', values=filtered_cars['First production year']),
                dict(label='HP', values=filtered_cars['HP']),
            ]
        )
    )
    return fig

@callback(
    Output('scatter_test', 'figure'),
    Input('parallel_coords', 'restyleData'),
    Input('start-year-dropdown', 'value')
)

def update_scatter(restyleData, years):
    if years is None:
        years_filtered_cars = all_cars
    else:
        years_to_filter = list(range(years[0], years[1] + 1))
        #print(years_to_filter)
        #df_exploded = all_cars.explode('Production years')

        # Step 2: Apply the filter
        df_exploded['Production years'] = df_exploded['Production years'].astype(int)
        df_filtered = df_exploded[df_exploded['Production years'].isin(years_to_filter)]

        # Step 3: (Optional) Group back if needed, to get lists of years again
        agg_dict = {'Production years': list}

        agg_dict.update({col: 'first' for col in df_filtered.columns if col not in ['Production years', 'Unnamed: 0']})

        years_filtered_cars = df_filtered.groupby('Unnamed: 0').agg(agg_dict)#.reset_index()


    print(restyleData)
    if restyleData is None:
        filtered_cars = years_filtered_cars # from the year filter
    else:
        # Extracting indices of the selected data points
        print(restyleData)
        print(type(restyleData[0]))
        for k, v in restyleData[0].items():
            num_dim = k.split('[')[1].split(']')[0]
            if num_dim.isdigit():
                print('dimension =', int(num_dim))
                print('column name =', par_coords_dimensions_dict[int(num_dim)])
                print('range = ', v)
                print(type(v))
                interval = v[0]
                min_val = interval[0]
                max_val = interval[1]
                print('min =', min_val, '\nmax =', max_val, '\ncolumn = ', par_coords_dimensions_dict[int(num_dim)])
                filtered_cars = years_filtered_cars[(years_filtered_cars[par_coords_dimensions_dict[int(num_dim)]] >= min_val) & (years_filtered_cars[par_coords_dimensions_dict[int(num_dim)]] <= max_val)]


    # Create a scatter plot based on the filtered 
    #print(filtered_cars)
    scatter_fig = px.scatter(filtered_cars, x='HP', y='Displacement', color='Company')
    return scatter_fig


@callback(
    Output('radar_charts', 'children'),
    Input('parallel_coords', 'restyleData'),
    Input('start-year-dropdown', 'value')
)

def update_radar(restyleData, years):
    if years is None:
        years_filtered_cars = all_cars
    else:
        years_to_filter = list(range(years[0], years[1] + 1))
        #print(years_to_filter)
        #df_exploded = all_cars.explode('Production years')

        # Step 2: Apply the filter
        df_exploded['Production years'] = df_exploded['Production years'].astype(int)
        df_filtered = df_exploded[df_exploded['Production years'].isin(years_to_filter)]

        # Step 3: (Optional) Group back if needed, to get lists of years again
        agg_dict = {'Production years': list}

        agg_dict.update({col: 'first' for col in df_filtered.columns if col not in ['Production years', 'Unnamed: 0']})

        years_filtered_cars = df_filtered.groupby('Unnamed: 0').agg(agg_dict).reset_index()


    if restyleData is None:
        filtered_cars = years_filtered_cars # from the year filter
        all_cars_norm_filtered = all_cars_norm[all_cars_norm['Unnamed: 0'].isin(filtered_cars['Unnamed: 0'])]
    else:
        # Extracting indices of the selected data points
        #print(restyleData)
        #print(type(restyleData[0]))
        for k, v in restyleData[0].items():
            num_dim = k.split('[')[1].split(']')[0]
            if num_dim.isdigit():
                #print('dimension =', int(num_dim))
                #print('column name =', par_coords_dimensions_dict[int(num_dim)])
                #print('range = ', v)
                #print(type(v))
                interval = v[0]
                min_val = interval[0]
                max_val = interval[1]
                print('min =', min_val, '\nmax =', max_val, '\ncolumn = ', par_coords_dimensions_dict[int(num_dim)])
                filtered_cars = years_filtered_cars[(years_filtered_cars[par_coords_dimensions_dict[int(num_dim)]] >= min_val) & (years_filtered_cars[par_coords_dimensions_dict[int(num_dim)]] <= max_val)]
                #print('filtered_cars', filtered_cars['Unnamed: 0'])
                #print('all_cars_norm', all_cars_norm['Unnamed: 0'])
                all_cars_norm_filtered = all_cars_norm[all_cars_norm['Unnamed: 0'].isin(filtered_cars['Unnamed: 0'])]


    return generate_radar_charts(all_cars_norm[all_cars_norm['Unnamed: 0'].isin(filtered_cars['Unnamed: 0'])])
