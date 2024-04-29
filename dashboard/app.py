import dash
from dash import Dash, html, dcc
import dash_core_components as dcc
import dash_html_components as html

app = Dash(__name__, use_pages=True)

app.layout = html.Div(
	[
		
        dash.page_container
    
])

if __name__ == '__main__':
	app.run_server(debug=True)
	