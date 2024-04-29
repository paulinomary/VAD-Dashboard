import pandas as pd
import warnings  # To handle DtypeWarning
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

custom_css = """
/* Hardcoded CSS styles */
body {
  background-color: #f5f5f5;
  font-family: Arial, sans-serif;
}

.flex {
  display: flex;
}

.map-container {
  flex: 50%;
  padding: 20px;
}

h4 {
  margin-bottom: 10px;
}

#graph {
  width: 100%;
  height: 400px;
}
"""

app = Dash(__name__)

# ... rest of your code ...

# Layout with hardcoded CSS
app.layout = html.Div(
    style={'display': 'flex', 'width': '100%', 'height': '100vh'},
    children=[
        # World map container
        html.Div(
            className="map-container",  # Added class for CSS targeting
            children=[
                html.H4('World Map'),
                dcc.Graph(id="graph", figure=fig)
            ]
        ),
        # Word cloud container
        html.Div(
            id='wordcloud-container',
            style={'flex': '50%', 'padding': '20px'},
            children=[
                html.H4('Word Cloud')
            ]
        )
    ],
    **{'style': custom_css}  # Apply custom CSS string
)


# ... rest of your code ...

if __name__ == '__main__':
    app.run_server(debug=True)
