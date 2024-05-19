#Show this graphic in a dash page
import plotly.express as px
import pandas as pd

#Filter the top 10 brands with the most unique series
cars = pd.read_csv('../dataset/cars-dataset.csv')
complete = pd.read_csv('../dataset/complete_cars.csv')
custom_colors = ['#1865A5', '#76C1EF','#DE3F47','#950E3F']

unique_series = complete.groupby('Company')['Serie'].nunique().reset_index()

unique_series.to_csv('unique_series_by_brand.csv', index=False)

top_10_brands = unique_series.nlargest(10, 'Serie')

unique_series = complete.groupby('Company')['Serie'].nunique().reset_index()

unique_series.to_csv('unique_series_by_brand.csv', index=False)

#Plot the number of unique series by brand

fig = px.bar(unique_series,
                x='Company',
                y='Serie',
                title='Number of unique series by brand',
                color='Serie',
                color_continuous_scale=custom_colors,
                width=1200,
                height=600)

fig.update_layout(xaxis={'categoryorder':'total descending'})
top_manufacturers = pd.DataFrame()

for i in range(1899, 2025):
    year_selected = i
    #print(i)
    aux_top = pd.DataFrame()
    aux_top = cars[cars['Production years'].str.contains(str(year_selected))].groupby('Company')['Serie'].nunique()
    # change name of column
    aux_top = aux_top.reset_index()
    aux_top.columns = ['Company', 'Serie']
    # add year column
    aux_top['Year'] = year_selected
    top_manufacturers = pd.concat([top_manufacturers, aux_top])
# Assuming you have already defined top_manufacturers and top_10_brands

# Filter the top manufacturers to include only the top 10 brands
top_manufacturers = top_manufacturers[top_manufacturers['Company'].isin(top_10_brands['Company'])]

# Create the horizontal bar plot
fig = px.bar(top_manufacturers,
             x='Serie',
             y='Company',
             title='Top 10 manufacturers with the most unique series',
             color='Serie',
             color_continuous_scale=custom_colors,
             width=1200,
             height=600,
             hover_name='Company',
             animation_frame='Year',
             animation_group='Company'
            )

# Update layout to order the bars
fig.update_layout(yaxis={'categoryorder': 'total ascending'})  # Sort bars by the number of series

fig.show()
