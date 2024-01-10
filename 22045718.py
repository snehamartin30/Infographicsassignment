# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 01:34:40 2024

@author: sm22alb
"""

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw,ImageFont
import textwrap 

# Read the dataset into a Pandas DataFrame
df = pd.read_csv('world food production.csv')

# Grouping by 'Country' and 'Year', then selecting four columns for a specific country during the year 2012
grouped_data = df[(df['Year'].isin([2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021])) &
                  (df['Entity'].isin(['Japan', 'South Korea', 'India', 'Germany', 'Canada','Africa','Afghanistan','Algeria','Argentina','Australia','Bangladesh']))].groupby(['Entity', 'Year'])[
    ['Wheat Production (tonnes)', 'Maize Production (tonnes)', 'Rice  Production ( tonnes)',
     'Tea  Production ( tonnes )', 'Palm oil  Production (tonnes)','Yams  Production (tonnes)','Tomatoes Production (tonnes)','Sweet potatoes  Production (tonnes)','Sunflower seed  Production (tonnes)','Sugar cane Production (tonnes)','Soybeans  Production (tonnes)','Rye  Production (tonnes)','Potatoes  Production (tonnes)','Oranges  Production (tonnes)','Peas, dry Production ( tonnes)','Grapes  Production (tonnes)','Coffee, green Production ( tonnes)','Cocoa beans Production (tonnes)','Bananas  Production ( tonnes)','Avocados Production (tonnes)','Apples Production (tonnes)']].sum()


print(grouped_data)

# Assuming 'grouped_data' contains the grouped and summed data
countries = ['Japan', 'India', 'Germany','Canada']  # List of countries to plot

plt.figure(figsize=(9, 6))

for country in countries:
    # Filter data for each country and select 'Maize Production' column
    country_data = grouped_data.loc[country]['Maize Production (tonnes)']
    plt.plot(country_data.index.get_level_values('Year'), country_data,\
             label=country, marker='o')

plt.title('Maize Production Trends (2012-2021)', fontsize=20)
plt.xlabel('Year')
plt.ylabel('Maize Production (tonnes)')
plt.legend()
#plt.grid(True)
plt.savefig('maize_production_plot.png')

# Assuming 'grouped_data' contains the grouped and summed data
india_rice_production = grouped_data.loc['Canada']['Wheat Production (tonnes)']

plt.figure(figsize=(9,6))
plt.bar(india_rice_production.index.get_level_values('Year'),\
        india_rice_production, color='Green', edgecolor='black',width=0.5)
plt.title('Rice Production in India (2012-2021)', fontsize=20)
plt.xlabel('Year')
plt.ylabel('Rice Production (tonnes)')
plt.xticks(india_rice_production.index.get_level_values('Year'), rotation=45)
#plt.grid(axis='y')
plt.tight_layout()
plt.savefig('rice_production_plot.png')

# Filter data for India in 2021
india_production_2021 = grouped_data.loc[('India', 2021)]

# Select specific productions for the pie chart
sizes = [
    india_production_2021['Oranges  Production (tonnes)'],
    india_production_2021['Apples Production (tonnes)'],
    india_production_2021['Peas, dry Production ( tonnes)'],
    india_production_2021['Potatoes  Production (tonnes)'],
    india_production_2021['Rye  Production (tonnes)']
]

labels = ['Oranges', 'Apples', 'peas', 'Potatoes', 'Rye']
colors = ['#FFA500', 'green', '#FFD700', 'darkblue', '#A52A2A']  # Orange, Tomato, Gold, Purple, Brown, Teal
explode = (0.1, 0., 0.01, 0, 0)  # Exploding the 'Oranges' slice

plt.figure(figsize=(10, 8))
plt.pie(sizes, labels=labels, colors=colors, explode=explode,\
        autopct='%1.1f%%', startangle=140, wedgeprops={'edgecolor': 'black'})
plt.gca().add_artist(plt.Circle((0, 0), 0.6, fc='white'))
plt.title('Crop Distribution Of India (2021)', fontsize=20)
plt.savefig('crop_distribution_india_plot.png')

# Comparing Palm Oil Production between India and Canada (2012-2021)
india_canada_oil_production = grouped_data.loc[(['India', 'Canada']), \
                                               'Palm oil  Production (tonnes)']
india_canada_oil_production = india_canada_oil_production.unstack(level=0)
plt.figure(figsize=(30, 15))  # Adjust the width and height values as needed
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (10, 8)  # Set default figure size

colors = ['#173f5f', '#20639b']  # Dark blue, light blue
india_canada_oil_production.plot(kind='barh', stacked=True, color=colors)
plt.xlabel('Year')
plt.ylabel('Palm Oil Production (tonnes)')
plt.title('Palm Oil Production of India and Canada (2012-2021)', fontsize=20)
plt.legend(title='Country')
plt.savefig('oil_production_plot.png')


# Combine the individual plots into a single image
combined_img = Image.new('RGB', (1800, 1200), color='white')  # Adjusted size
draw = ImageDraw.Draw(combined_img)
font = ImageFont.load_default()

# Add heading
heading = "EXPLORING AGRICULTURAL PRODUCTION (2012-2021)"

heading_font = ImageFont.truetype("arial.ttf", 36)  # Adjust font size and style as needed
heading_width, heading_height = draw.textsize(heading, font=heading_font)
heading_position = ((combined_img.width - heading_width) // 2, 10)
draw.text(heading_position, heading, font=heading_font, fill='black')

# Add the renewable energy plot
Maize_production_plot = Image.open('maize_production_plot.png')
combined_img.paste(Maize_production_plot, (10, 100))  # Adjusted position

# Add the electricity generation mix plot
Rice_production_plot = Image.open('rice_production_plot.png')
combined_img.paste(Rice_production_plot, (600, 130))  # Adjusted position

# Add the carbon intensity plot
Crop_distribution_india_plot = Image.open('crop_distribution_india_plot.png')
combined_img.paste(Crop_distribution_india_plot, (2, 550))  # Adjusted position

# Add the GDP over time plot
Oil_production_plot = Image.open('oil_production_plot.png')
combined_img.paste(Oil_production_plot, (600, 600))  # Adjusted position

textbox_width = 300
textbox_height = 200
textbox_position = ((combined_img.width - textbox_width) // 1.18, \
                    (combined_img.height - textbox_height) // 9)

draw.rectangle([textbox_position, (textbox_position[0] + textbox_width,\
                                   textbox_position[1] + textbox_height)], \
               fill='#FFFFFF')

textbox_text = "India's consistent top ranking in maize production among these nations throughout this period was the result of several factors, including favorable growing conditions, advanced farming methods, high demand, encouraging policies, intensive research and development, and abundant market opportunities. Although India experienced a downward trend in 2016, it rebound with a positive trend afterward. Germany, Canada, and Japan, on the other hand, kept their values comparatively steady over this period.The data shows a considerable surge in rice production between 2012 and 2015, succeeded by fluctuations in the  years that followed. The substantial increase from 2012 to 2015 indicates a noteworthy upturn in rice yield. Despite fluctuations thereafter, the production levels generally maintain an elevated status compared to the pre-2012 period.The cultivation of crops including oranges, apples, peas, rye, and potatoes was probably impacted by the notable increase in rice output in India in 2021. The production dynamics of these crops may have been impacted by increased competition for resources, changes in market needs, alternative planting decisions, interrupted crop rotation strategies, and potential effects from laws and regulations.In overall, India's production varies more widely than Canada's, and the trend points to a large decline in palm oil production by 2021, whereas Canada has maintained a very consistent, although modest, production level throughout time."


textbox_font = ImageFont.truetype("times.ttf", 24)
textbox_bg_color = 'skyblue'
# Wrap the text to fit within the textbox width
wrapped_text = textwrap.fill(textbox_text, width=40)  # Adjust width as needed
lines = wrapped_text.split('\n')

# If the wrapped text is longer than the textbox height, append ellipsis
if textbox_font.getsize(wrapped_text)[1] > textbox_height - 40:
    wrapped_text = textwrap.fill(textbox_text, width=35) + "..."  # Reduce width for ellipsis

draw.multiline_text((textbox_position[0] + 20, textbox_position[1] + 20),\
                    wrapped_text, font=textbox_font, fill='#000000')
    
name = "NAME : SNEHA MARTIN"
student_id = "STUDENT ID: 22045718"
text_font = ImageFont.truetype("arial.ttf", 16)
text_bg_color = 'lightgrey'
text_box_width = 200
text_box_height = 60
text_box_position = (10, combined_img.height - text_box_height - 10)  # Adjust position as needed

# Create the text box
draw.rectangle([text_box_position, (text_box_position[0] + text_box_width,
                                    text_box_position[1] + text_box_height)],
               fill=text_bg_color)

# Format the text content
text_content = f"{name}\n{student_id}"

# Add the text to the image
wrapped_text = textwrap.fill(text_content, width=25)  # Adjust width as needed
draw.multiline_text((text_box_position[0] + 10, text_box_position[1] + 10),
                    wrapped_text, font=text_font, fill='black')

    
    
    
# Save the combined image
plt.figure(figsize=(15,10))
plt.imshow(combined_img)
plt.axis('off')
plt.savefig('22045718.png', dpi=300)
