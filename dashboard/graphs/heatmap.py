import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import os
import geopandas as gpd

app = Dash(__name__)

# Sample data
cars = pd.read_csv('../dataset/cars-dataset.csv')
countries = pd.read_csv('../dataset/brands_countries.csv')

custom_colors = ['#1865A5', '#76C1EF', '#DE3F47', '#950E3F']

country_counts = countries['Country'].value_counts()
# Create a DataFrame from the counts
df_counts = pd.DataFrame({'Country': country_counts.index, 'Count': country_counts.values})

fig = px.choropleth(df_counts,
                    locations='Country',
                    locationmode='country names',
                    color='Count',
                    hover_name='Country',
                    color_continuous_scale=custom_colors,
                    labels={'Count': 'Number of Manufacturers'},
                    projection='natural earth',
                    scope='world')

text = {
    'font_family': 'Aspira'
}

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)

app.layout = html.Div(style={'font-family': text['font_family']}, children=[
    html.H4('Top Manufacturers in the World'),
    dcc.Graph(id="graph", figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
