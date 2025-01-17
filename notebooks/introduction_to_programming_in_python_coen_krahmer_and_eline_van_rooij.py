# -*- coding: utf-8 -*-
"""Introduction to Programming in Python Coen Krahmer and Eline van Rooij

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N0OTzmEj_9bA5oYy9feAgDLWSlOLbzFZ

**Take Home Exam Introduction to Programming in Python**

Coen Krahmer - i6280698

Eline van Rooij - i6269707

**Introduction**


Based on the given dataset, we decided to explore the data regarding developing countries, we specifically explored measles and its affect on infant death.


---



Research question: How does measles influence infant death rate in different developing countries?
  
  Step 1. What is the effect of measles on the infant death rate in Ecuador?
  
  Step 2. How does this effect in Ecuador compare to other developing countries?

**Data preparation**

First we loaded the dataset and took a global look at the dataset as a whole, as can be seen below.
"""

import pandas as pd

CountryHealthFactors = pd.read_csv('https://raw.githubusercontent.com/NHameleers/dtz2025-datasets/master/CountryHealthFactors.csv')
CountryHealthFactors = CountryHealthFactors.rename(columns=str.strip)
CountryHealthFactors

# Checking whether the 'status' column has been recorded in the exact same words, otherwise we might miss countries when we only select the rows with developing countries.
CountryHealthFactors['Status'].value_counts()

# Selecting only the developing countries.
DevelopingCountryHealthFactors = CountryHealthFactors.loc[CountryHealthFactors.Status == 'Developing']

"""We then started cleaning the dataset, selecting only developing countries and also only keeping relevant columns."""

# Selecting the columns we are interested in.
# We selected the column 'country' to know which countries we are working with.
# We selected the column 'year' to know what data is from what year.
# We selected the columns 'infant deaths' and 'measles' since these are the data we want to research.
DevelopingCountryHealthFactors = DevelopingCountryHealthFactors.loc[:, ['Country', 'Year', 'infant deaths', 'Measles']]
DevelopingCountryHealthFactors

"""We then took a look at the different countries that were seen as 'Developing', and quickly found countries which are in fact not developing countries, like France and Finland. We then decided to limit our dataset to SouthAmerican countries.



"""

# Checking what countries are in our list.
DevelopingCountryHealthFactors.Country.unique()

# Because we found a lot of developing countries and some of them are not developing in our opinion, we are going to look at just South American countries.
SouthAmericanHealthFactors = DevelopingCountryHealthFactors.loc[DevelopingCountryHealthFactors.Country.isin(['Ecuador', 'Peru', 'Colombia', 'Brazil', 'Venezuela (Bolivarian Republic of)', 'Suriname', 'Bolivia (Plurinational State of)', 'Chile', 'Paraguay', 'Argentina', 'Guyana']), :]

"""**Explore and clean data**

Here we looked at all the data in our set and searched for any outliers. We cleaned up any outliers we found. We also checked if we were missing any data.
"""

# Making sure every column is beginning with a capital letter
SouthAmericanHealthFactors = SouthAmericanHealthFactors.rename(columns={'infant deaths': 'Infant_deaths'})

# We checked if there are any years that are not logical (so too far in the past or future), here we looked specifically to the min and max. Nothing seems to be out of order.
# We did this with "SouthAmericanHealthFactors['Year'].describe()"
# We checked if the number of Infant Deaths per 1000 population has any irregular numbers (>1000 for example). We see no numbers above 1000, so we do not need to clean this up.
# We did this with "SouthAmericanHealthFactors['Infant_deaths'].describe()"
# We also checked if the number of Measles per 1000 population has any irregular numbers (>1000 for example).
# We did this with "SouthAmericanHealthFactors['Measles'].describe()"

# We found a number of measles that is not possible so we need to filter out the numbers above 1000 for this column.
SouthAmericanHealthFactors = SouthAmericanHealthFactors.loc[SouthAmericanHealthFactors.Measles < 1000, ]

# Checking again if everything works
# We did this with "SouthAmericanHealthFactors.describe()"

# We checked for missing data, but everything seems in order.
# We did this with "SouthAmericanHealthFactors.isnull().sum()"

"""**Describe and visualise**

Below, you will find a description of the population, the relevant data is found in the columns, and the correlation shows the computed correlation between Measles and Infant deaths. As you can see, the correlation is already all over the place.

"""

Describe_Measles = SouthAmericanHealthFactors.groupby('Country')['Measles'].mean()
Describe_Infant_deaths = SouthAmericanHealthFactors.groupby('Country')['Infant_deaths'].mean()
Describe_Measles_df = Describe_Measles.reset_index(name='Mean_Measles')
Describe_Infant_deaths_df = Describe_Infant_deaths.reset_index(name='Mean_Infant_deaths')

# Calculate correlation and handle missing values
correlation_df = SouthAmericanHealthFactors.groupby('Country').apply(lambda group: group['Measles'].corr(group['Infant_deaths'])).reset_index(name='Correlation')
Describe_correlation_df = correlation_df.dropna()  # Remove rows with NaN values

# Merge the DataFrames
Merged_describe_df = pd.merge(Describe_Measles_df, Describe_Infant_deaths_df, on='Country')
Merged_describe_df = pd.merge(Merged_describe_df, Describe_correlation_df, on='Country')

Merged_describe_df

"""
Now it is time to start investigating the correlation. Let's start with the first research question:
Question 1: What is the effect of measles on the infant death rate in Ecuador?"""

Selected = 'Ecuador'

Data_Ecuador = SouthAmericanHealthFactors[SouthAmericanHealthFactors['Country'] == 'Ecuador']
Data_Ecuador

import altair as alt
Chart_Ecuador = alt.Chart(Data_Ecuador).mark_point().encode(
    x=alt.X('Infant_deaths'),
    y=alt.Y('Measles')
).properties(title='Relation between measles and Infant deaths')

Chart_Ecuador.display()

"""Now for the second question: How does this effect in Ecuador compare to other developing countries? Below, an interactive graph can be found where we can compare Ecuador to other South American countries.

"""

import ipywidgets as widgets
from ipywidgets import interact
import altair as alt

# Assuming you have already imported altair and defined SouthAmericanHealthFactors and Data_Ecuador

Dropdown = SouthAmericanHealthFactors.drop(SouthAmericanHealthFactors[SouthAmericanHealthFactors['Country'] == 'Ecuador'].index)

def select(country):
    selected_country_data = Dropdown[Dropdown['Country'] == country]

    selected_country_chart = alt.Chart(selected_country_data).mark_circle().encode(
        x='Infant_deaths',
        y='Measles',
        color=alt.condition(
            alt.datum['Country'] == country,
            alt.value('red'),  # Color for the selected country
            alt.value('blue')  # Color for Ecuador
        ),
        tooltip=['Country', 'Measles', 'Infant_deaths']).properties(width=600, height=400)

# I made a new object called "Cart_Ecuador1" since when I used the original "Chart_Ecuador" the title did not change and kept the old title which was formulated in the cell below
    Chart_Ecuador1 = alt.Chart(Data_Ecuador).mark_point().encode(
        x=alt.X('Infant_deaths'),
        y=alt.Y('Measles')
    ).properties(title=f'The relation between Measles and Infant deaths compared between Ecuador and {country}')

    final_chart = Chart_Ecuador1 + selected_country_chart
    final_chart = final_chart.encode(
        color=alt.Color('Country:N', legend=alt.Legend(title='Country')))

    final_chart.display()

countries = Dropdown['Country'].unique()

interact(select, country=countries);

"""**Conclusion**

As can be seen in the description table of relevant data for Ecuador, the correlation between measles and infant deaths has been very inconsistent from the start. When also looking at the graph of Ecuador specifically, it can be seen that the scatterplot shows no correlation. When we tried to add a correlation line, this also did not make any sense, which is logical with this data, since there is no correlation to be found.

When looking at other South American countries, the same was found: There seems to be no correlation between measles infections and infant deaths. This can also be seen in the measure outlier data: Some years had up to 260 Measles infections per 1000 children, but still had the same amount of Infant deaths in comparison to years where the Measles infections were less than 10/1000 children.
"""