import dash
from dash import dcc, html  # Corrected imports for Dash 2.0 and above

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css', 'assets/css/styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Nav(className='navbar', children=[
        html.A(html.Img(src='./assets/components/Mini Logo branco.png', className='logo'), href='/'),
        html.A('General Knowledge', href='/general-knowledge'),
        html.A('Car Comparison', href='/car-comparison'),
        html.A('Car Finder', href='/car-finder'),
        html.A('About Us', href='/about-us'),
    ]),
    html.Div(className='content', children=dash.page_container)
])

if __name__ == '__main__':
    app.run_server(debug=True)
