import pandas as pd
import warnings  # To handle DtypeWarning
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import os
from wordcloud import WordCloud
import base64
import io  # For Solution 1
from PIL import Image  # For Solution 2
import tempfile  # For Solution 2

app = Dash(__name__)

# Suppress DtypeWarning (optional)
warnings.filterwarnings("ignore")

# Sample data (assuming data paths are correct)
cars = pd.read_csv('../dataset/cars-dataset.csv', dtype={'Country': str})  # Specify dtype for Country
countries = pd.read_csv('../dataset/brands_countries.csv')

custom_colors = ['#1865A5', '#76C1EF', '#DE3F47', '#950E3F']

country_counts = countries['Country'].value_counts()
# Create a DataFrame from the counts
df_counts = pd.DataFrame({'Country': country_counts.index, 'Count': country_counts.values})

fig = px.choropleth(df_counts,
                    locations='Country',
                    locationmode='country names',
                    color='Count',
                    hover_name='Country',
                    color_continuous_scale=custom_colors,
                    labels={'Count': 'Number of Manufacturers'},
                    projection='natural earth',
                    scope='world')

text = {
    'font_family': 'Aspira'
}

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, coloraxis_showscale=False)

app.layout = html.Div(
    style={'display': 'flex', 'width': '100%', 'height': '100vh'},
    children=[
        html.Div(className='sidenav',
                 children=[
                     html.Div(className='sidenav-header',
                              children=[
                                  html.Img(src='../assets/components/Mini Logo branco.png', alt='Logo', className='logo'),
                                  html.H1('Wordcloud', className='wordcloud-title')
                              ]),
                     dcc.Graph(id="graph", figure=fig, className='world-map'),
                     html.Div(id='wordcloud-container', className='wordcloud-container')
                 ])
    ]
)


@app.callback(
    Output('wordcloud-container', 'children'),
    Input('graph', 'clickData')
)
def update_wordcloud(clickData):
    if clickData is not None:
        country = clickData['points'][0]['location']
        manufacturers = countries[countries['Country'] == country]['Company'].values
        manufacturers = ' '.join(manufacturers)
        
        # Generate the WordCloud with custom colors and white background
        wordcloud = WordCloud(width=400, height=800, colormap='viridis', background_color='white').generate(manufacturers)
        
        # Convert the WordCloud object to an image
        img = wordcloud.to_image()

        # Convert the image to base64 format
        img_buffer = io.BytesIO()
        img.save(img_buffer, format="PNG")
        img_str = "data:image/png;base64," + base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        # Create an HTML img element to display the word cloud
        wordcloud_image = html.Img(src=img_str, className='wordcloud-img')

        return wordcloud_image
    else:
        return None  # Hide word cloud container if no country is clicked


if __name__ == '__main__':
    app.run_server(debug=True)
