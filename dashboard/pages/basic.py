import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, callback

dash.register_page(__name__, path='/basic')

# Sample data
evolution_top_speed = pd.read_csv('dataset/evolution_top_speed.csv')
cars = pd.read_csv('./dataset/cars-dataset.csv')
complete = pd.read_csv('./dataset/complete_cars.csv')
custom_colors = ['#1865A5', '#76C1EF','#DE3F47','#950E3F']
unique_series = complete.groupby('Company')['Serie'].nunique().reset_index()
unique_series.to_csv('unique_series_by_brand.csv', index=False)
top_10_brands = unique_series.nlargest(10, 'Serie')
unique_series = complete.groupby('Company')['Serie'].nunique().reset_index()
unique_series.to_csv('unique_series_by_brand.csv', index=False)

# Define the colors for the lines
line_colors = ['#1865A5', '#76C1EF', '#f9d29f', '#EBA74C', '#DE3F47']

# Define the initial 5 brands
brands_filter = ['BMW', 'AUDI', 'MERCEDES BENZ', 'TOYOTA', 'FERRARI']

# Filter the dataframe based on the initial brands
filtered_evolution_top_speed = evolution_top_speed[evolution_top_speed['Company'].isin(brands_filter)]

top_manufacturers = pd.DataFrame()

for i in range(1899, 2025):
    year_selected = i
    #print(i)
    aux_top = pd.DataFrame()
    aux_top = cars[cars['Production years'].str.contains(str(year_selected))].groupby('Company')['Serie'].nunique()
    # change name of column
    aux_top = aux_top.reset_index()
    aux_top.columns = ['Company', 'Serie']
    # add year column
    aux_top['Year'] = year_selected
    top_manufacturers = pd.concat([top_manufacturers, aux_top])
# Assuming you have already defined top_manufacturers and top_10_brands

# Filter the top manufacturers to include only the top 10 brands
top_manufacturers = top_manufacturers[top_manufacturers['Company'].isin(top_10_brands['Company'])]

# Create the initial figure
fig1 = px.line(filtered_evolution_top_speed,
              x='Year',
              y='Mean Top Speed km/h',
              color='Company',
              color_discrete_sequence=line_colors,
              width=600,
              height=400)

# Change line width
fig1.update_traces(line=dict(width=4))

# Add a slider to select the year
fig1.update_layout(xaxis_title='Year',
                  yaxis_title='Mean Top Speed km/h',
                  font=dict(family='Aspira'),
                  xaxis=dict(range=[1920, 2024]),
                  xaxis_rangeslider_visible=True)

# Create the horizontal bar plot
fig2 = px.bar(top_manufacturers,
             x='Serie',
             y='Company',
             title='Top 10 manufacturers with the most unique series',
             color='Serie',
             color_continuous_scale=custom_colors,
             width=1200,
             height=600,
             hover_name='Company',
             animation_frame='Year',
             animation_group='Company'
            )


# Update layout to order the bars
fig2.update_layout(yaxis={'categoryorder': 'total ascending'})  # Sort bars by the number of series

# Layout with dropdowns
layout = html.Div(id='page-content', style={'font-family': 'Palatino', 'margin-top': '50px'}, children=[
    html.Div([
        html.H4('Top Speed Evolution by Year and Brand'),
        dcc.Graph(id="graph1", figure=fig1),
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
    style={'border': '2px solid #ccc', 'padding': '10px', 'width': '650px', 'height': '500px'}),
    html.Div([
        dcc.Graph(figure=fig2)
    ], style={'display': 'inline-block', 'width': '50%'})
])


############################# Callbacks
@callback(
    Output('graph1', 'figure'),
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
