import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, callback
import os

# Path to your CSS file (relative or absolute)
stylesheet_path = os.path.join("assets", "css", "styles.css")

dash.register_page(__name__, path='/about-us')

# Layout with centered logo
layout = html.Div(
    children=[
        # Include your navbar or sidebar component here (if applicable)
        html.Div(className='content',  # Main content area
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
            children=[
                html.Img(src='./assets/components/Logo.png', className='big-logo')
        ])])