# Python Dash Page
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os

# Path to your CSS file (relative or absolute)
stylesheet_path = os.path.join("assets", "css", "styles.css")

dash.register_page(__name__, path='/about-us')

# Layout with centered logo
layout = html.Div(
    children=[
        # Insert a text box with the text "About Us"
        html.Div(className='text',  # Main content area
            children=[
                html.H1('About Us', className='about-us-title'),
            ]),
        html.Div(className='content',
            children=[
                html.P('This project was developed for the Curricular Unit of Advanced Data Visualization which is on the 2nd Semester of the 1st Year of the Engineering and Data Science Master´s Degree.' , className='about-us-text'),
                html.P('For this project we chose a Dataset that has a lot of information about Manufacturers, its specific Cars and their details.', className='about-us-text'),
                html.P(' ', className='about-us-text'),
                html.P(' ', className='about-us-text'),
                html.Div(className="container", children=[
                    html.Section(className="Mariana", children=[
                        html.Div(className="front-Mary", children=[
                            html.Img(id='img-Mariana', src='./assets/components/Mariana.jpeg', className='img-Mariana'),
                            html.Div(className="back-text-Mary", children= [
                                html.P('Mariana Paulino, 2020190448'),
                                html.A(href='https://github.com/paulinomary', className='github', target='_blank', children=[
                                    html.Img(src='./assets/components/git-logo.png', className='github-logo'),
                                ]),
                            ]),
                            html.P(' '),
                            html.P(''),
                        ]),
                        
                    ]),
                    html.Div(className="front-Alex", children=[
                        html.Img(id='img-Alex', src='./assets/components/Alex.jpeg', className='img-Alex'),
                        html.Div(className="back-text-Alex", children= [
                            html.P('Alexandre Tapadinhas, 2018283200'),
                            html.A(href='https://github.com/AlexandreTapadinhas', className='github', target='_blank', children=[
                                html.Img(src='./assets/components/git-white.png', className='github-logo')
                            ]),
                        ]),
                    ]),
                ])
            ]),
])
