import dash
from dash import dcc, html, Input, Output, callback_context
import os  # Added for file path manipulation

# Function to read and render page layouts from folder
def get_page_layout(page_name):
  layout_path = os.path.join("pages", f"{page_name}.py")  # Construct file path
  if os.path.exists(layout_path):  # Check if file exists
    with open(layout_path, 'r') as f:
      layout_content = f.read()  # Read file content
    # You can potentially process the layout content here (optional)
    return html.Div(dangerously_set_inner_HTML=layout_content)  # Render layout
  else:
    return html.Div(children="Page not found")  # Default for missing page

# Define app layout structure
app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.Div(className='sidenav', children=[
            html.Div(className='sidenav-header', children=[
                # Your logo or title here (replace with content)
                html.Img(src='./assets/components/Mini Logo branco.png', className='logo')
            ]),
            html.A('Home', href='/', className='active'),
            html.A('Basic', href='/basic'),
            html.A('Advanced', href='/advanced'),
            html.A('About Us', href='/about-us'),
        ]),
        html.Div(id='page-content', children=[])  # Placeholder for page content
    ]
)

# Callback to dynamically update page content based on URL
@app.callback(
    Output(component_id='page-content', component_property='children'),
    Input(component_id=URL_pathname, component_property='pathname')
)
def update_page_content(pathname):
  if pathname:  # Check if pathname exists
    page_name = pathname.strip("/")  # Extract page name from URL
    return get_page_layout(page_name)  # Load layout for the page
  return html.Div(children="Page not found")  # Default for invalid URL

# ... (Replace with your page layout imports from pages folder)
from pages import page1_layout, page2_layout, etc.  # Replace with actual imports

# Additional app initialization (if any)

if __name__ == '__main__':
    app.run_server(debug=True)
