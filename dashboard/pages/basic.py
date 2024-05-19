import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, callback
from plotly.subplots import make_subplots
import os
from wordcloud import WordCloud
import base64
import io  # For Solution 1
from PIL import Image  # For Solution 2
import tempfile  # For Solution 2

# Register Dash page
dash.register_page(__name__, path='/basic')

aspira_font_path = 'assets/fonts/Aspira Heavy.otf'
palatino_font_path = 'assets/fonts/Palatino.ttf'

# Sample data
evolution_top_speed = pd.read_csv('dataset/evolution_top_speed.csv')
cars = pd.read_csv('./dataset/cars-dataset.csv')
complete = pd.read_csv('./dataset/complete_cars.csv')
countries = pd.read_csv('./dataset/brands_countries.csv', dtype={'Country': str})

# Define the colors for the lines
line_colors = ['#1865A5', '#76C1EF', '#f9d29f', '#EBA74C', '#DE3F47', '#950E3F']
custom_colors = ['#1865A5', '#76C1EF', '#DE3F47', '#950E3F']

# Define the initial 5 brands
brands_filter = ['BMW', 'AUDI', 'MERCEDES BENZ', 'TOYOTA', 'FERRARI']

# Filter the top 10 brands with the most unique series
unique_series = complete.groupby('Company')['Serie'].nunique().reset_index()
unique_series.to_csv('unique_series_by_brand.csv', index=False)
top_10_brands = unique_series.nlargest(10, 'Serie')

# Average power by brand by year
# Create a new column that only has the power(hp) value only up to the first space
cars['HP'] = cars['Power(HP)'].str.split(' ').str[0]
cars['HP'] = cars['HP'].astype(float)

evolution_power_per_brand = pd.DataFrame()

for i in range(1899, 2025):
    year_selected = i
    aux_evolution_power_per_brand = pd.DataFrame()
    aux_evolution_power_per_brand = cars[cars['Production years'].str.contains(str(year_selected))].groupby('Company')['HP'].mean()
    aux_evolution_power_per_brand = aux_evolution_power_per_brand.reset_index()
    aux_evolution_power_per_brand.columns = ['Company', 'Mean HP']
    aux_evolution_power_per_brand['Year'] = year_selected
    evolution_power_per_brand = pd.concat([evolution_power_per_brand, aux_evolution_power_per_brand])

# Prepare data for top manufacturers plot
top_manufacturers = pd.DataFrame()
for i in range(1899, 2025):
    year_selected = i
    aux_top = cars[cars['Production years'].str.contains(str(year_selected))].groupby('Company')['Serie'].nunique()
    aux_top = aux_top.reset_index()
    aux_top.columns = ['Company', 'Serie']
    aux_top['Year'] = year_selected
    top_manufacturers = pd.concat([top_manufacturers, aux_top])

# Filter the top manufacturers to include only the top 10 brands
top_manufacturers = top_manufacturers[top_manufacturers['Company'].isin(top_10_brands['Company'])]

# Create the initial figure for Mean Top Speed by Year and Brand
filtered_evolution_top_speed = evolution_top_speed[evolution_top_speed['Company'].isin(brands_filter)]
fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=filtered_evolution_top_speed['Year'],
    y=filtered_evolution_top_speed['Mean Top Speed km/h'],
    mode='lines',
    line=dict(color=line_colors[0], width=4),
))
fig1.update_layout(
    xaxis_title='Year',
    yaxis_title='Mean Top Speed km/h',
    font=dict(family='Aspira'),  # Set font to Aspira
    xaxis=dict(range=[1920, 2024]),
    xaxis_rangeslider_visible=True,
    height=400,
)

top_manufacturers.rename(columns={'Serie': 'Models Produced'}, inplace=True)
# Create the horizontal bar plot for Top 10 Manufacturers by Year
fig2 = px.bar(top_manufacturers,
              x='Models Produced',
              y='Company',
              title='Top 10 manufacturers with the most unique series',
              color='Models Produced',
              color_continuous_scale=custom_colors,
              animation_frame='Year',
              animation_group='Company')
fig2.update_layout(
    yaxis={'categoryorder': 'total ascending'},  # Sort bars by the number of series
    height=600,
    font=dict(family='Aspira')  # Set font to Aspira
)

# Create choropleth figure for number of manufacturers per country
country_counts = countries['Country'].value_counts()
# Create a DataFrame from the counts
df_counts = pd.DataFrame({'Country': country_counts.index, 'Count': country_counts.values})

choropleth_fig = px.choropleth(df_counts,
                    locations='Country',
                    locationmode='country names',
                    color='Count',
                    hover_name='Country',
                    color_continuous_scale=custom_colors,
                    labels={'Count': 'Number of Manufacturers'},
                    projection='natural earth',
                    scope='world')
choropleth_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False, font=dict(family='Aspira'))  # Set font to Aspira

# line plot by year of the mean power by brand by year
brands = ['TOYOTA', 'BUGATTI', 'FERRARI', 'BMW', 'AUDI', 'PORSCHE']

filtered_evolution_power = evolution_power_per_brand[evolution_power_per_brand['Company'].isin(brands)]

fig5 = px.line(filtered_evolution_power,
                x='Year',
                y='Mean HP',
                title='Mean HP by brand',
                color='Company',
                height=400,
                color_discrete_sequence=line_colors
                )

# Change line width
fig5.update_traces(line=dict(width=4))
fig5.update_layout(xaxis_title='Year',
                  yaxis_title='Mean HP',
                  title='Mean HP by brand',
                  xaxis=dict(range=[1920, 2024]),
                  xaxis_rangeslider_visible=True,
                  font=dict(family='Aspira')  # Set font to Aspira
                  )

fuel_options = [
    {'label': 'Gasoline', 'value': 'Gasoline'},
    {'label': 'Hybrid', 'value': 'Hybrid'},
    {'label': 'Electric', 'value': 'Electric'},
    {'label': 'Diesel', 'value': 'Diesel'},
    {'label': 'Natural Gas', 'value': 'Natural Gas'},
    {'label': 'Hybrid Gasoline', 'value': 'Hybrid Gasoline'},
    {'label': 'Mild Hybrid', 'value': 'Mild Hybrid'},
    {'label': 'Mild Hybrid Diesel', 'value': 'Mild Hybrid Diesel'},
    {'label': 'Plug-in Hybrid', 'value': 'Plug-in Hybrid'},
    {'label': 'Ethanol', 'value': 'Ethanol'},
    {'label': 'Hybrid Diesel', 'value': 'Hybrid Diesel'},
    {'label': 'Liquefied Petroleum Gas (LPG)', 'value': 'Liquefied Petroleum Gas (LPG)'},
]

fuel_dropdown = dcc.Dropdown(
    id='fuel-dropdown',
    options=fuel_options,
    value='Gasoline',  # Default value
    clearable=False,  # Disable clear option
    persistence=True,  # Persist the selected values
    persistence_type='local'  # Persist the selected values locally
)

# Define the power vs displacement graph
cars['Displacement'] = cars['Displacement'].str.extract(r'(\d+)').astype(float)
def generate_power_displacement_graph(selected_brands, selected_fuel):
    if selected_brands is None or len(selected_brands) == 0:
        return go.Figure()

    # Filter the dataframe based on selected brands and fuel
    cars_filtered = cars[(cars['Fuel'] == selected_fuel) & (cars['Company'].isin(selected_brands))]
    
    # Update fig6 (Power vs Displacement)
    fig6 = px.scatter(cars_filtered,
                      x='Displacement',
                      y='HP',
                      title='Power vs Displacement',
                      color='Company',
                      color_discrete_sequence=line_colors,
                      hover_name="Model",
                      hover_data=['Company', 'Production years', 'Specification summary'],
                      height=400)

    return fig6

# Create the initial layout
layout = html.Div(id='page-content', style={'font-family': 'Palatino', 'margin-top': '50px'}, children=[
    html.Div([
        dcc.Dropdown(
            id='brand-dropdown',
            options=[{'label': brand, 'value': brand} for brand in sorted(evolution_top_speed['Company'].unique())],
            multi=True,
            value=brands_filter,  # Set default to brands_filter
            clearable=False,
            persistence=True,
            persistence_type='local'
        ),
    ]),
    html.Div([
        html.H4('Top Speed Evolution by Year and Brand'),
        dcc.Graph(id="graph1", figure=fig1),
    ]),
    html.Div([
        html.H4('Top Manufacturers'),
        dcc.Graph(id="graph2", figure=fig2)
    ]),
    html.Div([
        html.H4('Choropleth Map of Manufacturers'),
        html.Div([
            dcc.Graph(id='choropleth-map', figure=choropleth_fig),
            html.Div(id='wordcloud-container', className='wordcloud-container')
        ], style={'display': 'flex'})
    ]),
    html.Div([
        html.H4('Mean HP by Brand'),
        dcc.Graph(id='mean-hp-graph', figure=fig5)
    ]),
    html.Div([
        html.H4('Power vs Displacement'),
        dcc.Dropdown(id='fuel-dropdown', options=fuel_options, value='Gasoline', clearable=False),
        dcc.Graph(id='power-displacement-graph', figure=generate_power_displacement_graph(brands_filter, 'Gasoline'))
    ]),
])

# Callbacks
@callback(
    Output('wordcloud-container', 'children'),
    [Input('choropleth-map', 'clickData')]
)

def update_wordcloud(clickData):
    if clickData:
        country = clickData['points'][0]['hovertext']
        manufacturers = countries[countries['Country'] == country]['Company'].tolist()
        if manufacturers:
            text = ' '.join(manufacturers)
            wordcloud = WordCloud(width=800, height=400, colormap='RdBu', background_color='white', font_path=aspira_font_path).generate(text)
            fig = make_subplots(rows=1, cols=1)
            fig.add_trace(go.Image(z=wordcloud.to_array(), hoverinfo='skip'), row=1, col=1)
            fig.update_layout(
                margin=dict(l=0, r=0, t=0, b=0),
                height=400,
                width=800,
                showlegend=False,
                xaxis=dict(
                    tickvals=[],  # Hide tick values on x-axis
                    ticktext=[]   # Hide tick labels on x-axis
                ),
                yaxis=dict(
                    tickvals=[],  # Hide tick values on y-axis
                    ticktext=[]   # Hide tick labels on y-axis
                )
            )
            return dcc.Graph(figure=fig)

    return html.Div()

# Callbacks
@callback(
    [Output('graph1', 'figure'),
     Output('mean-hp-graph', 'figure')],
    [Input('brand-dropdown', 'value')]
)
def update_graph(selected_brands):
    if selected_brands is None or len(selected_brands) == 0:
        # If no brands selected, return empty figure
        return go.Figure(), go.Figure()

    # Filter the dataframe based on selected brands
    filtered_data = evolution_top_speed[evolution_top_speed['Company'].isin(selected_brands)]

    # Update fig1 (Top Speed Evolution by Year and Brand)
    updated_fig1 = go.Figure()
    for brand, color in zip(filtered_data['Company'].unique(), line_colors):
        data = filtered_data[filtered_data['Company'] == brand]
        updated_fig1.add_trace(go.Scatter(
            x=data['Year'],
            y=data['Mean Top Speed km/h'],
            mode='lines',
            name=brand,
            line=dict(color=color, width=4),
        ))
    updated_fig1.update_layout(
        xaxis_title='Year',
        yaxis_title='Mean Top Speed km/h',
        font=dict(family='Aspira'),
        xaxis=dict(range=[1920, 2024]),
        xaxis_rangeslider_visible=True,
        height=400,
    )

    # Update fig5 (Mean HP by Brand)
    filtered_evolution_power = evolution_power_per_brand[evolution_power_per_brand['Company'].isin(selected_brands)]
    updated_fig5 = px.line(filtered_evolution_power,
                           x='Year',
                           y='Mean HP',
                           title='Mean HP by brand',
                           color='Company',
                           height=400,
                           color_discrete_sequence=line_colors
                           )
    updated_fig5.update_traces(line=dict(width=4))
    updated_fig5.update_layout(xaxis_title='Year',
                               yaxis_title='Mean HP',
                               title='Mean HP by brand',
                               xaxis=dict(range=[1920, 2024]),
                               xaxis_rangeslider_visible=True)

    return updated_fig1, updated_fig5

@callback(
    Output('power-displacement-graph', 'figure'),
    [Input('brand-dropdown', 'value'),
     Input('fuel-dropdown', 'value')]
)
def update_power_displacement_graph(selected_brands, selected_fuel):
    return generate_power_displacement_graph(selected_brands, selected_fuel)
