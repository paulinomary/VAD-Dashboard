import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import os

app = Dash(__name__)

# Sample data
evolution_top_speed = pd.read_csv('../dataset/evolution_top_speed.csv')

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


brands_filter = ['BMW', 'AUDI', 'MERCEDES BENZ', 'TOYOTA']

filtered_evolution_top_speed = evolution_top_speed[evolution_top_speed['Company'].isin(brands_filter)]

fig = px.line(filtered_evolution_top_speed,
                x='Year',
                y='Mean Top Speed km/h',
                title='Mean top speed by brand',
                color='Company',
                color_discrete_sequence=line_colors,
                width=1200,
                height=900,
                )

#Change line width
fig.update_traces(line=dict(width=4))

#Add a slider to select the year
fig.update_layout(xaxis_title='Year',
                  yaxis_title='Mean Top Speed km/h',
                  title='Mean top speed by brand',
                  xaxis=dict(range=[1920, 2024]),
                  xaxis_rangeslider_visible=True)


text = {
    'font_family': 'Aspira'
}

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)

app.layout = html.Div(id='page-content', style={'font-family': text['font_family']}, children=[
    html.H4('Top Speed Evolution by Year and Brand'),
    dcc.Graph(id="graph", figure=fig)
])

page1_layout = html.Div(id='page-content', style={'font-family': text['font_family']}, children=[
    html.H4('Top Speed Evolution by Year and Brand'),
    dcc.Graph(id="graph", figure=fig)
])

# if __name__ == '__main__':
#     app.run_server(debug=True)
