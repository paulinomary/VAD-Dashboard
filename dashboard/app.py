import dash
from dash import dcc, html
import os

# Path to your CSS file (relative or absolute)
stylesheet_path = os.path.join("assets", "css", "styles.css")

app = dash.Dash(__name__, external_stylesheets=[stylesheet_path])

# Function to generate the logo as a clickable link
def logo_link():
  return html.A(
      # Replace with your logo image details
      children=[html.Img(src="./assets/components/Mini Logo branco.png", className="logo")],
      href="/"  # Set href to "/" for home page
  )

# App layout
app.layout = html.Div(
    style={'display': 'flex'},
    children=[
        html.Div(className="sidenav", children=[
            html.Div(className="sidenav-header", children=[
                # Use the logo_link function to create clickable logo
                logo_link(),
            ]),
            html.A("Basic", className="sidenav-link", href="/basic"),  # Replace href with appropriate URL
            html.A("Advanced", className="sidenav-link", href="/advanced"),  # Replace href with appropriate URL
            html.A("About", className="sidenav-link", href="/about")  # Replace href with appropriate URL
        ]),
        html.Div(className="content", children=[
            # Your main app content here (replace with your Dash components)
            html.H1("Welcome to your Dash App!"),
            dcc.Graph(id="example-graph", figure={})  # Replace with your graph
        ])
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
