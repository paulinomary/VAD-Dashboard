import dash
from dash import dcc, html
import os

# Path to your CSS file (relative or absolute)
stylesheet_path = os.path.join("assets", "css", "styles.css")

app = dash.Dash(__name__, external_stylesheets=[stylesheet_path])

# Layout with centered logo
app.layout = html.Div(
    children=[
        # Include your navbar or sidebar component here (if applicable)
        html.Div(className='content',  # Main content area
            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'},
            children=[
                html.Img(src='./assets/components/Logo.png', className='big-logo')
            ]])
])


if __name__ == '__main__':
    app.run_server(debug=True)
