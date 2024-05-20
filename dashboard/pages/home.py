import dash
from dash import dcc, html
import os

# Path to your CSS file (relative or absolute)
stylesheet_path = os.path.join("assets", "css", "styles.css")

dash.register_page(__name__, path='/')

# Layout with centered logo
layout = html.Div(
    children=[
        # Include your navbar or sidebar component here (if applicable)
        html.Div(className='home',  # Main content area
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
            children=[
                html.Img(src='./assets/components/Logo.png', className='big-logo')
        ])])
