import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback
from plotly.subplots import make_subplots

dash.register_page(__name__, path='/car-comparison')

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
