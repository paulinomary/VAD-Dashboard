import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, callback

dash.register_page(__name__, path='/basic')

# Sample data
evolution_top_speed = pd.read_csv('dataset/evolution_top_speed.csv')

# Define the colors for the lines
line_colors = ['#1865A5', '#76C1EF', '#f9d29f', '#EBA74C', '#DE3F47']

# Define the initial 5 brands
brands_filter = ['BMW', 'AUDI', 'MERCEDES BENZ', 'TOYOTA', 'FERRARI']

# Filter the dataframe based on the initial brands
filtered_evolution_top_speed = evolution_top_speed[evolution_top_speed['Company'].isin(brands_filter)]

# Create the initial figure
fig = px.line(filtered_evolution_top_speed,
              x='Year',
              y='Mean Top Speed km/h',
              color='Company',
              color_discrete_sequence=line_colors,
              width=600,
              height=400)

# Change line width
fig.update_traces(line=dict(width=4))

# Add a slider to select the year
fig.update_layout(xaxis_title='Year',
                  yaxis_title='Mean Top Speed km/h',
                  font=dict(family='Aspira'),
                  xaxis=dict(range=[1920, 2024]),
                  xaxis_rangeslider_visible=True)

# Layout with dropdowns


layout = html.Div(id='page-content', style={'font-family': 'Palatino', 'margin-top': '50px'}, children=[
    html.Div([
        html.H4('Top Speed Evolution by Year and Brand'),
        dcc.Graph(id="graph", figure=fig),
        dcc.Dropdown(
            id='brand-dropdown',
            options=[{'label': brand, 'value': brand} for brand in evolution_top_speed['Company'].unique()],
            multi=True,
            value=brands_filter,  # Set default to brands_filter
            style={'width': '100%', 'margin-top': '20px'},  # Adjust style as needed
            clearable=False,  # Disable clear option
            persistence=True,  # Persist the selected values
            persistence_type='local'  # Persist the selected values locally
        ),
    ],
    style={'border': '2px solid #ccc', 'padding': '10px', 'width': '650px', 'height': '500px'})
])


@callback(
    Output('graph', 'figure'),
    Input('brand-dropdown', 'value')
)
def update_graph(selected_brands):
    if selected_brands is None or len(selected_brands) == 0:
        # If no brands selected, return empty figure
        return px.line(width=600, height=400)

    # Filter the dataframe based on selected brands
    filtered_data = evolution_top_speed[evolution_top_speed['Company'].isin(selected_brands)]

    # Create the updated figure
    updated_fig = px.line(filtered_data,
                          x='Year',
                          y='Mean Top Speed km/h',
                          color='Company',
                          color_discrete_sequence=line_colors,
                          width=600,
                          height=400)
    
    # Change line width
    updated_fig.update_traces(line=dict(width=4))

    # Add a slider to select the year
    updated_fig.update_layout(xaxis_title='Year',
                               yaxis_title='Mean Top Speed km/h',
                               font=dict(family='Aspira'),
                               xaxis=dict(range=[1920, 2024]),
                               xaxis_rangeslider_visible=True)
    
    return updated_fig


