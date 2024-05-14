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
                html.Div(className="container", children=[
                    html.Div(className="front-Mary", children=[
                        html.Img(id='img-Mariana', src='./assets/components/Mariana.jpeg', className='img-Mariana'),
                        html.Div(className="back-text-Mary", children= [
                            html.P('Mariana Paulino, 2020190448'),
                            html.A(href='https://github.com/paulinomary', className='github', target='_blank', children=[
                                html.Img(src='./assets/components/git-logo.png', className='github-logo')
                            ]),
                        ]),
                        html.Div(className="container", children=[
                            html.P('This project was developed for the Curricular Unit of Advanced Data Visualization in the 2nd Semester of the 1st Year of the Engineering and Data Science Degree.'),
                            html.P('The main objective was the creation of a dashboard that allows all users to visualize data in a simple and intuitive way.'),
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
]),
])
