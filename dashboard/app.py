import dash
from dash import dcc
from dash import html
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css', 'assets/css/styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)

app.layout = html.Div([
    html.Nav(className='sidenav', children=[
        html.A(html.Img(src='./assets/components/Mini Logo branco.png', className='logo'), href='/'),
        html.A('Basic', href='basic'),
        html.A('Advanced', href='advanced'),
        html.A('Evolution Top Speed', href='evolution_top_speed'),
        html.A('About Us', href='about-us'),
    ]),
    dash.page_container,
])


if __name__ == '__main__':
    app.run_server(debug=True)
